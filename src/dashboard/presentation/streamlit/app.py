from decimal import Decimal

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.application import (
    BuildSalesDashboardRequest,
    BuildSalesDashboardUseCase,
    GetDashboardDataRequest,
    GetDashboardDataUseCase,
)
from dashboard.application.dto import DashboardDataRowDTO
from dashboard.infrastructure.persistence import (
    InMemorySalesAggregateReader,
    InMemorySalesRecord,
    build_default_dashboard_data_reader,
)
from dashboard.presentation.streamlit.pages import render_sales_page
from dashboard.presentation.streamlit.state import DashboardState


def _render_executive_header() -> None:
    st.title("📊 Dashboard Ejecutivo Pro")
    st.markdown("### Análisis en Tiempo Real de Performance")


def _rows_to_dataframe(rows: tuple[DashboardDataRowDTO, ...]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Mes": [row.month for row in rows],
            "Ventas": [row.sales for row in rows],
            "Clientes": [row.customers for row in rows],
            "Región": [row.region for row in rows],
        }
    )


def _render_executive_metrics(df: pd.DataFrame) -> None:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Ventas Totales", f"${df['Ventas'].sum():,}", "12%")
    with col2:
        st.metric("Clientes Activos", f"${df['Clientes'].sum():,}", "23")
    with col3:
        st.metric("Promedio Mensual", f"${df['Ventas'].mean():.0f}", "8%")
    with col4:
        st.metric("ROI", "245%", "15%")


def _render_sales_line_chart(df: pd.DataFrame) -> None:
    line_chart = px.line(
        df,
        x="Mes",
        y="Ventas",
        title="Evolución de Ventas Mensuales",
        markers=True,
    )
    line_chart.update_layout(template="plotly_dark")
    st.plotly_chart(line_chart, width="stretch")


def _render_clients_region_pie_chart(df: pd.DataFrame) -> None:
    pie_chart = px.pie(
        df,
        values="Clientes",
        names="Región",
        title="Distribución de Clientes por Región",
    )
    pie_chart.update_layout(template="plotly_dark")
    st.plotly_chart(pie_chart, width="stretch")


def _render_filters(df: pd.DataFrame) -> tuple[str, list[str]]:
    st.sidebar.header("Filtros de Control")
    month_options = ["Todos", *sorted(df["Mes"].unique().tolist())]
    selected_month = st.sidebar.selectbox(
        "Selecciona un mes:",
        month_options,
    )
    selected_regions = st.sidebar.multiselect(
        "Filtrar por región:",
        df["Región"].unique(),
    )
    return selected_month, selected_regions


def _render_filtered_table(
    df: pd.DataFrame,
    selected_month: str,
    selected_regions: list[str],
) -> None:
    active_regions = (
        ", ".join(selected_regions) if selected_regions else "Todas"
    )
    st.caption(
        f"Filtros activos -> Mes: {selected_month} | Región: {active_regions}"
    )

    if df.empty:
        st.info("No hay datos para la combinación de filtros seleccionada.")
        return

    st.dataframe(df, width="stretch")


def run_streamlit_app() -> None:
    st.set_page_config(
        page_title="Dashboard Backend Streamlit Python",
        layout="wide",
        page_icon="📊",
    )

    state = DashboardState()
    reader = InMemorySalesAggregateReader(
        aggregate_id=state.aggregate_id,
        currency="USD",
        records=(
            InMemorySalesRecord(
                sku="SKU-001",
                units=120,
                revenue=Decimal("3540"),
            ),
            InMemorySalesRecord(
                sku="SKU-002",
                units=80,
                revenue=Decimal("1680"),
            ),
            InMemorySalesRecord(
                sku="SKU-003",
                units=45,
                revenue=Decimal("1215"),
            ),
        ),
    )
    use_case = BuildSalesDashboardUseCase(reader=reader)
    dashboard = use_case.execute(
        BuildSalesDashboardRequest(aggregate_id=state.aggregate_id),
    )
    render_sales_page(dashboard)

    dashboard_data_use_case = GetDashboardDataUseCase(
        reader=build_default_dashboard_data_reader(),
    )
    all_dashboard_data = dashboard_data_use_case.execute(
        GetDashboardDataRequest(),
    )
    all_dashboard_df = _rows_to_dataframe(all_dashboard_data.rows)

    _render_executive_header()
    selected_month, selected_regions = _render_filters(all_dashboard_df)
    filtered_dashboard_data = dashboard_data_use_case.execute(
        GetDashboardDataRequest(
            month=selected_month,
            regions=tuple(selected_regions),
        )
    )
    filtered_dashboard_df = _rows_to_dataframe(filtered_dashboard_data.rows)
    _render_executive_metrics(filtered_dashboard_df)
    _render_sales_line_chart(filtered_dashboard_df)
    _render_clients_region_pie_chart(filtered_dashboard_df)
    _render_filtered_table(
        filtered_dashboard_df,
        selected_month,
        selected_regions,
    )
