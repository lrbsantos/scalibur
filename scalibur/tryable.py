from abc import abstractmethod, ABC
from typing import Callable, Generic, TypeVar, Union

from scalibur.option import Option, Some, Nothing

T = TypeVar('T')


class Tryable(ABC, Generic[T]):
    """
    The `Tryable` type represents a computation that may either result in an exception,
    or return a successfully computed value. 
 
    Instances of `Tryable[T]`, are either an instance of Success[T] or Failure[T].

    For example, `Try` can be used to perform division on a user-defined input, without
    the need to do explicit exception-handling in all of the places that an exception
    might occur.
    
    Example:
    >>> from scalibur.tryable import Try, Success, Failure
    >>> from operator import truediv
    >>>
    >>> def divide():
    >>>   def div(dividend: str, divisor: str):
    >>>     return truediv(int(dividend), int(divisor))
    >>>
    >>>   dividend = input("Enter an Int that you'd like to divide:\n")
    >>>   divisor = input("Enter an Int that you'd like to divide by:\n")
    >>>   problem = Try(div)(dividend, divisor)
    >>>
    >>>   match problem:
    >>>     case Success(v):
    >>>       print(f"Result of {dividend} / {divisor}  is {v}")
    >>>     case Failure(e):
    >>>       print("You must've divided by zero or entered something that's not an Int. Try again!")
    >>>       print(f"Info from the exception: {e}")
    >>>
    >>> divide()
    """
    __slots__ = ("_value",)

    def __init__(self, value) -> None:
        super().__init__()
        self._value = value

    @property
    def is_failure(self) -> bool:
        """Returns `true` if the `Try` is a `Failure`, `false` otherwise.

        :return: `true` if the `Try` is a `Failure`, `false` otherwise.
        """
        return isinstance(self, Failure)

    @property
    def is_success(self) -> bool:
        """Returns `true` if the `Try` is a `Success`, `false` otherwise.

        :return: `true` if the `Try` is a `Success`, `false` otherwise.
        """
        return isinstance(self, Success)

    @abstractmethod
    def get(self) -> T:
        """Returns the value from this `Success` or throws the exception if this is a `Failure`.

        :return: the value from this `Success` or throws the exception if this is a `Failure`.
        """
        raise NotImplementedError

    def failed(self) -> Union["Success", "Failure"]:
        """Inverts this `Tryable`. If this is a `Failure`, returns its exception wrapped in a `Success`.
        If this is a `Success`, returns a `Failure` containing an `UnsupportedOperationException`.

        :return:
        """
        return Success(self._value) if self.is_failure else Failure(UnsupportedOperationException("Success.failed"))

    def get_or_else(self, default_value: T) -> T:
        """Returns the value from this `Success` or the given `default_value` argument if this is a `Failure`.

        *Note:*: This will throw an exception if it is not a success and default throws an exception.

        :param default_value: the value to be returned if this is a `Failure`.

        :return:  the value from this `Success` or the given `default_value` argument if this is a `Failure`.
        """
        return default_value if self.is_failure else self.get()

    def to_option(self) -> Option[T]:
        """Returns `Nothing` if this is a `Failure` or a `Some` containing the value if this is a `Success`.

        :return: `Nothing` if this is a `Failure` or a `Some` containing the value if this is a `Success`.
        """
        return Nothing() if self.is_failure else Some(self.get())

    def __iter__(self) -> "Tryable[T]":
        return self


class Success(Tryable[T]):
    __slots__ = ("_has_next",)
    __match_args__ = ("_value",)

    def __init__(self, value: T) -> None:
        super().__init__(value)
        self._has_next = True

    def get(self) -> T:
        return self._value

    def __next__(self) -> T:
        if self._has_next:
            self._has_next = False
            return self._value
        self._has_next = True
        raise StopIteration

    def __repr__(self) -> str:
        return "Success({})".format(str(self._value))

    def __str__(self) -> str:
        return str(self._value)


class Failure(Tryable[Exception]):
    __slots__ = ()
    __match_args__ = ("_value",)

    def __init__(self, exception: Exception) -> None:
        super().__init__(exception)

    def get(self) -> Exception:
        raise self._value

    def __next__(self) -> Exception:
        raise StopIteration

    def __repr__(self) -> str:
        return "Failure({})".format(str(self._value))

    def __str__(self) -> str:
        return str(self._value)


class UnsupportedOperationException(Exception):
    pass


def Try(f: Callable[..., T]) -> Callable[..., Tryable[T]]:
    """Factory method of a Tryable object.

    :param f: callable to be tried to execute.

    :return: a callable as a Tryable object.
    """
    def wrapper(*args, **kwargs) -> Tryable:
        try:
            return Success(f(*args, **kwargs))
        except Exception as e:
            return Failure(e)

    return wrapper
