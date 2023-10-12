import typing
from abc import ABC, abstractmethod
from ..log import logger

if typing.TYPE_CHECKING:
    from ..calcurse import Configuration


class Extension(ABC):
    def __init__(self, config: "Configuration") -> None:  # type: ignore[no-untyped-def]
        self.config: Configuration = config
        self.logger = logger

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.config})"

    __str__ = __repr__

    @abstractmethod
    def pre_load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def post_save(self) -> None:
        raise NotImplementedError
