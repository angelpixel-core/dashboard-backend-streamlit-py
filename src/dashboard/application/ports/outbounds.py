from typing import Protocol

from dashboard.domain.sales import SalesAggregate


class SalesAggregateReader(Protocol):
    def get_sales_aggregate(self, aggregate_id: str) -> SalesAggregate: ...
