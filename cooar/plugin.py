from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from cooar.utilities.types import AuthType, MediaType


class CooarPluginInfoABC(ABC):
    """
    All the info properties, so they dont bother while working with the acctual plugin class
    """

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def author(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def supported_mediatypes(self) -> Tuple[MediaType, ...]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def supported_authtypes(self) -> Tuple[AuthType, ...]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def supported_qualities(self) -> Dict:
        raise NotImplementedError()

    @property
    @abstractmethod
    def template_strings(self) -> Tuple[str, ...]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def default_template(self) -> str:
        raise NotImplementedError()


class CooarPlugin(CooarPluginInfoABC, ABC):
    @abstractmethod
    def prepare(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def collect(self, part_id=None, **kwargs) -> List:
        raise NotImplementedError()

    @abstractmethod
    def download(self, file, **kwargs):
        raise NotImplementedError()
