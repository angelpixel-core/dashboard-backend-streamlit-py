import streamlit as st

from dashboard.application.dto import SalesLineDTO


def render_sales_chart(lines: tuple[SalesLineDTO, ...]) -> None:
    chart_data = [{"sku": line.sku, "units": line.units} for line in lines]
    st.subheader("Units by SKU")
    st.bar_chart(chart_data, x="sku", y="units")
