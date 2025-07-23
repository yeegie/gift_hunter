from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

T = TypeVar("T")


class BaseIOC(ABC):
    """
    ### IoC Container
    Store dependencies by key-value principe

    @example

    Store dependencie
    ``` python
    container.attach("notificator", notificator)
    ```

    Get from container
    ``` python
    notificator = container.get("notificator")
    ```
    """
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set(self, key: Type[T], instance: T) -> None:
        """Attach dependency to container"""
        raise NotImplementedError()

    @abstractmethod
    def get(self, key: Type[T]) -> T:
        """Get dependency in container"""
        raise NotImplementedError()
