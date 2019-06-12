# PyCompose
_A simple way to inject composition through inheritance syntax._

## Inspirations
The following links served as inpiration during the writing of this, and as a in-depth explanation of what actually is composition and its benefits and drawbacks versus inheritance.
* [Ariel Ortiz's 2019 PyCon talk](https://www.youtube.com/watch?v=YXiaWtc0cgE)
* [forwardable](https://github.com/5long/forwardable)

## Explanation
From the inspirations one can easily see that an older implementation of compositional forwarding exists ([forwardable](https://github.com/5long/forwardable)) so why would I do this to myself? In short, I didn't like the syntax introduced by it. I find the syntax provided by this implementation a bit easier to understand as I find adding things that related to properties of a class inside the brackets in the class statement the most logical.

## Usage
```python
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


c = C()
print(c.test1 + c.test2)  # > 123456
c.helloA()                # > A
c.helloB()                # > B
print(c._a, c.b_object)   # > <A> <B>
```

## Disclaimer
Please do note that this project is but a small abstraction for something that can easily be achieved only a few more lines of hand written code. As such I am aware of the fact that this may seem pretty useless to some people.