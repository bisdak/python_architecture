from domain import model
from typing import Protocol


class AbstractRepository(Protocol):
    def add(self, batch: model.Batch):
        ...

    def get(self, reference: str) -> model.Batch:
        ...


class SqlAlchemyRepository():
    def __init__(self, session):
        self.session = session

    def add(self, batch: model.Batch):
        self.session.add(batch)

    def get(self, reference: str):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()
