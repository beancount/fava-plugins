from __future__ import annotations

from typing import TYPE_CHECKING

from fava_plugins.todo_as_error import TodoError

if TYPE_CHECKING:
    from .conftest import LoaderResult


def test_todo_as_error(load_doc: LoaderResult) -> None:
    """
    plugin "fava_plugins.todo_as_error"
    plugin "beancount.plugins.auto_accounts"

    2016-11-01 * "Foo" "Bar"
        todo: "This will become an error"
        Expenses:Foo                100 EUR
        Assets:Cash
    """
    _, errors, __ = load_doc

    assert len(errors) == 1
    error = errors[0]
    assert isinstance(error, TodoError)
    assert error.message == "This will become an error"
