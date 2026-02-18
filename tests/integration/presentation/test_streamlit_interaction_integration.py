from decimal import Decimal

import pytest

from dashboard.application.dto import SalesDashboardDTO, SalesLineDTO
from dashboard.presentation.streamlit import app as streamlit_app_module
from dashboard.presentation.streamlit.pages import (
    sales_page as sales_page_module,
)


def test_run_streamlit_app_renders_dashboard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_config: dict[str, object] = {}
    rendered: list[SalesDashboardDTO] = []

    def fake_set_page_config(**kwargs: object) -> None:
        captured_config.update(kwargs)

    def fake_render_sales_page(dto: SalesDashboardDTO) -> None:
        rendered.append(dto)

    monkeypatch.setattr(
        streamlit_app_module.st,
        "set_page_config",
        fake_set_page_config,
    )
    monkeypatch.setattr(
        streamlit_app_module,
        "render_sales_page",
        fake_render_sales_page,
    )

    streamlit_app_module.run_streamlit_app()

    assert captured_config["page_title"] == "Dashboard Backend Streamlit Python"
    assert captured_config["layout"] == "wide"
    assert len(rendered) == 1
    assert rendered[0].aggregate_id == "sales-overview"
    assert rendered[0].total_units == 245
    assert rendered[0].total_revenue == Decimal("6435")


class FakeMetricColumn:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def metric(self, label: str, value: object) -> None:
        self.calls.append((label, value))


def test_sales_page_sends_metrics_and_chart(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    left = FakeMetricColumn()
    right = FakeMetricColumn()
    chart_calls: list[tuple[SalesLineDTO, ...]] = []

    dto = SalesDashboardDTO(
        aggregate_id="sales-overview",
        currency="USD",
        total_units=8,
        total_revenue=Decimal("99.50"),
        lines=(SalesLineDTO(sku="SKU-100", units=8, revenue=Decimal("99.50")),),
    )

    monkeypatch.setattr(sales_page_module.st, "title", lambda _text: None)
    monkeypatch.setattr(sales_page_module.st, "caption", lambda _text: None)
    monkeypatch.setattr(
        sales_page_module.st,
        "columns",
        lambda _count: (left, right),
    )
    monkeypatch.setattr(
        sales_page_module,
        "render_sales_chart",
        lambda lines: chart_calls.append(lines),
    )

    sales_page_module.render_sales_page(dto)

    assert left.calls == [("Total Units", 8)]
    assert right.calls == [("Total Revenue", "USD 99.50")]
    assert chart_calls == [dto.lines]
