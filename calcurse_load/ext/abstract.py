from abc import ABC, abstractmethod


class Extension(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def pre_load():
        raise NotImplementedError

    @abstractmethod
    def post_save():
        raise NotImplementedError
