import pytest
from domain.model import Batch, OrderLine, allocate, OutOfStock
from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO_CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO_CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO_CLOCK", 10)

    ref = allocate(line, [in_stock_batch, shipment_batch])

    assert ref == 'in-stock-batch'
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earliear_batches():
    earliest = Batch("speedy-batch", "GOLD_SPOON", 100, eta=today)
    medium = Batch("normal-batch", "GOLD_SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "GOLD_SPOON", 100, eta=later)
    line = OrderLine("order1", "GOLD_SPOON", 10)

    ref = allocate(line, [medium, earliest, latest])
    assert ref == "speedy-batch"
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch1", "SMALL_FORK", 10, eta=today)
    allocate(OrderLine("order1", "SMALL_FORK", 10), [batch])

    with pytest.raises(OutOfStock, match='SMALL_FORK'):
        allocate(OrderLine("order1", "SMALL_FORK", 1), [batch])
