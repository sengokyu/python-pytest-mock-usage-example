from .foo import FooClass
from .bar import BarClass


class TargetClass:
    def do_something(self, foo: FooClass) -> None:
        """ """
        bar = BarClass()
        bar.do_bar(foo.do_foo())
