import streamlit as st

from dashboard.application.dto import SalesDashboardDTO
from dashboard.presentation.streamlit.components import render_sales_chart


def render_sales_page(dto: SalesDashboardDTO) -> None:
    st.title("Dashboard Backend Streamlit Python")
    st.caption("Presentation adapter wired to application use case.")

    c1, c2 = st.columns(2)
    c1.metric(label="Total Units", value=dto.total_units)
    c2.metric(
        label="Total Revenue",
        value=f"{dto.currency} {dto.total_revenue}",
    )

    render_sales_chart(dto.lines)
