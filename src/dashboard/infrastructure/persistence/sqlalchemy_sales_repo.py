from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from dashboard.application.ports import SalesAggregateReader
from dashboard.domain.sales import (
    CurrencyCode,
    Money,
    SalesAggregate,
    SalesLine,
)


class MappingsResult(Protocol):
    def mappings(self) -> list[dict[str, object]]: ...


class SqlAlchemySessionLike(Protocol):
    def execute(
        self,
        statement: str,
        params: dict[str, object],
    ) -> MappingsResult: ...


@dataclass
class SqlAlchemySalesAggregateReader(SalesAggregateReader):
    session: SqlAlchemySessionLike
    currency: str

    def get_sales_aggregate(self, aggregate_id: str) -> SalesAggregate:
        statement = (
            "select sku, units, revenue "
            "from sales_lines "
            "where aggregate_id = :aggregate_id"
        )
        rows = self.session.execute(
            statement,
            {"aggregate_id": aggregate_id},
        ).mappings()

        currency = CurrencyCode(self.currency)
        lines = [
            SalesLine(
                sku=_as_str(row["sku"], "sku"),
                units=_as_int(row["units"], "units"),
                revenue=Money(
                    amount=_as_decimal(row["revenue"], "revenue"),
                    currency=currency,
                ),
            )
            for row in rows
        ]
        return SalesAggregate(
            aggregate_id=aggregate_id,
            currency=currency,
            lines=lines,
        )


def _as_str(value: object, field_name: str) -> str:
    if isinstance(value, str):
        return value
    raise TypeError(f"{field_name} must be str")


def _as_int(value: object, field_name: str) -> int:
    if isinstance(value, int):
        return value
    raise TypeError(f"{field_name} must be int")


def _as_decimal(value: object, field_name: str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, str):
        return Decimal(value)
    raise TypeError(f"{field_name} must be decimal-compatible")
