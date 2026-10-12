from dataclasses import dataclass

from dashboard.application.dto import DashboardDataRowDTO
from dashboard.application.ports import DashboardDataReader


@dataclass(frozen=True)
class InMemoryDashboardDataRecord:
    month: str
    sales: int
    customers: int
    region: str


@dataclass
class InMemoryDashboardDataReader(DashboardDataReader):
    records: tuple[InMemoryDashboardDataRecord, ...]

    def list_rows(self) -> tuple[DashboardDataRowDTO, ...]:
        return tuple(
            DashboardDataRowDTO(
                month=record.month,
                sales=record.sales,
                customers=record.customers,
                region=record.region,
            )
            for record in self.records
        )


def build_default_dashboard_data_reader() -> InMemoryDashboardDataReader:
    return InMemoryDashboardDataReader(
        records=(
            InMemoryDashboardDataRecord(
                month="Enero",
                sales=45000,
                customers=120,
                region="Norte",
            ),
            InMemoryDashboardDataRecord(
                month="Febrero",
                sales=52000,
                customers=145,
                region="Sur",
            ),
            InMemoryDashboardDataRecord(
                month="Marzo",
                sales=48000,
                customers=133,
                region="Norte",
            ),
            InMemoryDashboardDataRecord(
                month="Abril",
                sales=61000,
                customers=167,
                region="Centro",
            ),
            InMemoryDashboardDataRecord(
                month="Mayo",
                sales=58000,
                customers=156,
                region="Sur",
            ),
            InMemoryDashboardDataRecord(
                month="Junio",
                sales=67000,
                customers=189,
                region="Norte",
            ),
        ),
    )
