from abc import ABC, abstractmethod


class SessionCreator(ABC):
    @abstractmethod
    def create_session(self, db_uri: str):
        raise NotImplementedError()
