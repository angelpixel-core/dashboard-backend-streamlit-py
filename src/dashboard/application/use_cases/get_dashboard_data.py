from dataclasses import dataclass

from dashboard.application.dto import DashboardDataDTO
from dashboard.application.ports import (
    DashboardDataReader,
    GetDashboardDataPort,
    GetDashboardDataRequest,
)


@dataclass
class GetDashboardDataUseCase(GetDashboardDataPort):
    reader: DashboardDataReader

    def execute(
        self,
        request: GetDashboardDataRequest,
    ) -> DashboardDataDTO:
        selected_month = _normalize_month(request.month)
        selected_regions = tuple(
            region.strip()
            for region in (request.regions or ())
            if region and region.strip()
        )

        rows = self.reader.list_rows()
        filtered_rows = tuple(
            row
            for row in rows
            if (
                (selected_month is None or row.month == selected_month)
                and (
                    not selected_regions
                    or row.region in selected_regions
                )
            )
        )
        return DashboardDataDTO(rows=filtered_rows)


def _normalize_month(raw_month: str | None) -> str | None:
    if raw_month is None:
        return None

    month = raw_month.strip()
    if not month or month.casefold() == "todos":
        return None

    return month
