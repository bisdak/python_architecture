from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, registry

import domain.model as model

mapper_registry = registry()


order_table = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batch_table = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations_table = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    lines_mapper = mapper_registry.map_imperatively(model.OrderLine, order_table)
    mapper_registry.map_imperatively(
        model.Batch,
        batch_table,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations_table, collection_class=set,
            )
        },
    )
