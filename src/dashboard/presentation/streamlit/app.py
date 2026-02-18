from decimal import Decimal

import streamlit as st

from dashboard.application import (
    BuildSalesDashboardRequest,
    BuildSalesDashboardUseCase,
)
from dashboard.infrastructure.persistence import (
    InMemorySalesAggregateReader,
    InMemorySalesRecord,
)
from dashboard.presentation.streamlit.pages import render_sales_page
from dashboard.presentation.streamlit.state import DashboardState


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
