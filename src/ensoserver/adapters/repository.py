import abc

from ensoserver.domain import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, batch: model.Enso):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Enso:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, enso_value):
        entry = self.session.query(model.Enso).filter_by(ts=enso_value.ts).first()
        if entry:
            entry.meiv2 = enso_value.meiv2
        else:
            self.session.add(enso_value)

    def get(self, ts):
        return self.session.query(model.Enso).filter_by(ts=ts).one()

    def list(self):
        return self.session.query(model.Enso).all()

    def count(self):
        return self.session.query(model.Enso).count()
