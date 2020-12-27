import pytest
from exmock import __version__
from exmock.target import TargetClass
from exmock.foo import FooClass
from exmock.bar import BarClass


class TestsTargetClass:
    def test_1(self, mocker):
        """ クラスのモックを作る """
        # Given
        foo_mock = mocker.Mock(spec=FooClass)
        instance = TargetClass()

        # When
        instance.do_something(foo_mock)

        # Then
        foo_mock.do_foo.assert_called_once()

    def test_2(self, mocker):
        """ コンストラクタの戻り値をモックにする """
        # Given
        bar_mock = mocker.Mock(spec=BarClass)
        bar_constructor_mock = mocker.patch(
            'exmock.target.BarClass', return_value=bar_mock)
        instance = TargetClass()

        # When
        instance.do_something(FooClass())

        # Then
        bar_constructor_mock.assert_called_once()
        bar_mock.do_bar.assert_called_once()

    def test_3(self, mocker):
        """ クラスのメソッドをモック化する """
        # Given
        do_bar_mock = mocker.patch.object(BarClass, 'do_bar')
        instance = TargetClass()

        # When
        instance.do_something(FooClass())

        do_bar_mock.assert_called_once()

    def test_4(self, mocker):
        """ 戻り値を設定する """
        # Given
        foo_mock = mocker.Mock(spec=FooClass)
        foo_mock.do_foo.return_value = 'foo result'
        do_bar_mock = mocker.patch.object(BarClass, 'do_bar')
        do_bar_mock.return_value = 'bar result'

        instance = TargetClass()

        # When
        instance.do_something(foo_mock)

        # Then
        foo_mock.do_foo.assert_called_once()
        do_bar_mock.assert_called_once_with('foo result')

    def test_5(self, mocker):
        """ 呼び出された時に例外を発生させる """
        # Given
        foo_mock = mocker.Mock(spec=FooClass)
        foo_mock.do_foo.side_effect = Exception('エラーです')

        instance = TargetClass()

        # Then
        with pytest.raises(Exception):
            # When
            instance.do_something(foo_mock)

    def test_6(self, mocker):
        """ 複数回呼び出されたことをテストする """
        # Given
        do_bar_mock = mocker.patch.object(BarClass, 'do_bar')

        instance = TargetClass()

        # When
        instance.do_something(FooClass())
        instance.do_something(FooClass())

        # Then
        assert do_bar_mock.call_count == 2

    def test_7(self, mocker):
        """ 呼び出されないことをテストする """
        # Given
        do_bar_mock = mocker.patch.object(BarClass, 'do_bar')

        instance = TargetClass()

        # When

        # Then
        do_bar_mock.assert_not_called()

    def test_8(self, mocker):
        """ 複雑な引数をテストする """
        # Given
        do_bar_mock = mocker.patch.object(BarClass, 'do_bar')

        instance = TargetClass()

        # When
        instance.do_something(FooClass())

        # Then
        args, kwargs = do_bar_mock.call_args
        assert len(args) == 1
        assert args[0] is not None
        assert type(args[0]) is str
        assert len(kwargs) == 0
