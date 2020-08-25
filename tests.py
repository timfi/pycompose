import pytest

from pycompose import Compose


class A:
    test1 = "123"

    def hello(self):
        print("A")

    def __repr__(self):
        return "<A>"


class B:
    test2 = "456"

    def hello(self):
        print("B")

    def __repr__(self):
        return "<B>"


class C(
    Compose(A, "test1", ("hello", "helloA")),
    Compose(B, "test2", ("hello", "helloB"), name="b_object"),
):
    ...


class D:
    def __init__(self, test):
        self.test = test


class E(Compose(D, "test", "test2", args=("this is a test",))):
    ...


class F(Compose(D, "test", args=("this is a test",))):
    ...


def test_basic_function():
    c = C()
    assert c.test1 + c.test2 == "123456"
    assert hasattr(c, "helloA")
    assert hasattr(c, "helloB")
    assert isinstance(c._a, A)
    assert isinstance(c.b_object, B)

    with pytest.raises(TypeError):
        E()

    f = F()
    assert f.test == "this is a test"
    f.test = "this is a different test"
    del f.test
