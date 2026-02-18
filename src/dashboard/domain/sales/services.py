from collections.abc import Sequence

from .entities import SalesAggregate, SalesLine
from .value_objects import CurrencyCode


def build_sales_aggregate(
    aggregate_id: str,
    currency: CurrencyCode,
    lines: Sequence[SalesLine],
) -> SalesAggregate:
    aggregate = SalesAggregate(aggregate_id=aggregate_id, currency=currency)
    for line in lines:
        aggregate.add_line(line)
    return aggregate
