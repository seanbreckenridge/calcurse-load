from abc import ABC, abstractmethod


class Extension(ABC):
    def __init__(self, config) -> None:  # type: ignore[no-untyped-def]
        self.config = config

    @abstractmethod
    def pre_load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def post_save(self) -> None:
        raise NotImplementedError
