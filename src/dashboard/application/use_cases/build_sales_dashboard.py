from dataclasses import dataclass

from dashboard.application.dto import SalesDashboardDTO, SalesLineDTO
from dashboard.application.ports import (
    BuildSalesDashboardPort,
    BuildSalesDashboardRequest,
    SalesAggregateReader,
)


@dataclass
class BuildSalesDashboardUseCase(BuildSalesDashboardPort):
    reader: SalesAggregateReader

    def execute(
        self,
        request: BuildSalesDashboardRequest,
    ) -> SalesDashboardDTO:
        aggregate_id = request.aggregate_id.strip()
        if not aggregate_id:
            raise ValueError("aggregate_id cannot be empty")

        aggregate = self.reader.get_sales_aggregate(aggregate_id)
        lines = tuple(
            SalesLineDTO(
                sku=line.sku,
                units=line.units,
                revenue=line.revenue.amount,
            )
            for line in aggregate.lines
        )
        return SalesDashboardDTO(
            aggregate_id=aggregate.aggregate_id,
            currency=aggregate.currency.code,
            total_units=aggregate.total_units(),
            total_revenue=aggregate.total_revenue().amount,
            lines=lines,
        )
