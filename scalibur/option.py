from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class Option(ABC, Generic[T]):
    @property
    def is_defined(self) -> bool:
        """Returns true if the option is Some, false otherwise.

        This is equivalent to:

        >>> match option:
        >>>     case Some(_):
        >>>         return True
        >>>     case Nothing():
        >>>         return False

        :return: true if the option is Some, false otherwise.
        """
        return isinstance(self, Some)

    @property
    def is_empty(self) -> bool:
        """Returns true if the option is Nothing, false otherwise.

        This is equivalent to:

        >>> match option:
        >>>     case Some(_):
        >>>         return False
        >>>     case Nothing():
        >>>         return True

        :return: true if the option is Nothing, false otherwise.
        """
        return isinstance(self, Nothing)

    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError

    def get_or_else(self, default_value: T) -> T:
        return default_value if self.is_empty else self.get()


class Some(Option[T]):
    __match_args__ = ("_value",)
    __slots__ = ("_value")

    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value

    def __repr__(self) -> str:
        return "Some(value={})".format(str(self._value))

    def __str__(self) -> str:
        return str(self._value)


class Nothing(Option[T]):
    def get(self) -> T:
        raise NotImplementedError
