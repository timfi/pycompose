"""A simple way to inject composition through inheritance syntax

Example:
>>> class A:
...     field = "123"
>>> class B(Compose(A, "field")):
...     ...
>>> b = B()
>>> print(b.a)
<__main__.A object at ...>
>>> print(b.field)
123
>>> class C(Compose(A, ("field", "attr"))):
...     ...
>>> c = C()
>>> print(b.attr)
123
"""
from operator import attrgetter
import sys
from typing import Union, Tuple, Any, Dict


def Compose(
    type_: type,
    *fields: Union[str, Tuple[str, str]],
    name: str = None,
    args: Tuple = tuple(),
    kwargs: Dict[str, Any] = dict(),
) -> type:
    """Generate a new type that encompasses the forwarding of the given fields
    
    :param type_: the type to composee
    :param *fields: the fields to forward
    :param name: the name to give the composee, defaults to f"_{type_.__name__.lower()}"
    :param args: the positional arguments to call the constructor of type_ with, defaults to tuple()
    :param kwargs: the keyword arguments to call the constructor of type_ with, defaults to dict()
    :return: the inheritable type
    """
    name_ = name or f"_{type_.__name__.lower()}"

    class InheritableComposition:
        def __init__(self, *_args, **_kwargs):
            setattr(self, name_, kwargs.pop(name, type_(*args, **kwargs)))
            super().__init__(*_args, **_kwargs)

        # Magical frame hack, to add properties...
        frame = sys._getframe()
        for field in fields:
            origin, dest = (field, field) if not isinstance(field, tuple) else field
            frame.f_locals[dest] = build_field(name_, origin)
        del frame, dest, origin, field

    return InheritableComposition


def build_field(name: str, field: str) -> property:
    """Build a single forwarding property to encompass the requested field
    
    :param name: the name given to the composee
    :param field: the field to forward
    :return: the generated property
    """
    obj_getter = attrgetter(name)

    def getter(self):
        return getattr(obj_getter(self), field)

    def setter(self, value):
        return setattr(obj_getter(self), field, value)

    def deleter(self):
        return delattr(obj_getter(self), field)

    return property(getter, setter, deleter)


if __name__ == "__main__":

    class A:
        test1 = "123"

        def hello(self):
            print("A")

    class B:
        test2 = "456"

        def hello(self):
            print("B")

    class C(
        Compose(A, "test1", ("hello", "helloA")),
        Compose(B, "test2", ("hello", "helloB")),
    ):
        ...

    c = C()
    print(c.test1 + c.test2)
    c.helloA()
    c.helloB()
    print(dir(c))
