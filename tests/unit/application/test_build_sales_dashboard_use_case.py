from decimal import Decimal

import pytest

from dashboard.application import (
    BuildSalesDashboardRequest,
    BuildSalesDashboardUseCase,
)
from dashboard.domain.sales import (
    CurrencyCode,
    Money,
    SalesAggregate,
    SalesLine,
)


class FakeSalesAggregateReader:
    def __init__(self, aggregate: SalesAggregate) -> None:
        self.aggregate = aggregate
        self.requested_ids: list[str] = []

    def get_sales_aggregate(self, aggregate_id: str) -> SalesAggregate:
        self.requested_ids.append(aggregate_id)
        return self.aggregate


def _sample_aggregate() -> SalesAggregate:
    usd = CurrencyCode("USD")
    return SalesAggregate(
        aggregate_id="sales-overview",
        currency=usd,
        lines=[
            SalesLine(
                sku="SKU-001",
                units=4,
                revenue=Money(amount=Decimal("120"), currency=usd),
            ),
            SalesLine(
                sku="SKU-002",
                units=2,
                revenue=Money(amount=Decimal("150"), currency=usd),
            ),
        ],
    )


def test_build_sales_dashboard_maps_domain_to_dto() -> None:
    reader = FakeSalesAggregateReader(aggregate=_sample_aggregate())
    use_case = BuildSalesDashboardUseCase(reader=reader)

    dto = use_case.execute(
        BuildSalesDashboardRequest(aggregate_id=" sales-overview "),
    )

    assert reader.requested_ids == ["sales-overview"]
    assert dto.aggregate_id == "sales-overview"
    assert dto.currency == "USD"
    assert dto.total_units == 6
    assert dto.total_revenue == Decimal("270")
    assert dto.lines[0].sku == "SKU-001"
    assert dto.lines[0].units == 4


def test_build_sales_dashboard_rejects_empty_request_id() -> None:
    reader = FakeSalesAggregateReader(aggregate=_sample_aggregate())
    use_case = BuildSalesDashboardUseCase(reader=reader)

    with pytest.raises(ValueError, match="cannot be empty"):
        use_case.execute(BuildSalesDashboardRequest(aggregate_id="   "))
