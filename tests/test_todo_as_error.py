from fava_plugins.todo_as_error import TodoError


def test_todo_as_error(load_doc):
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
    assert isinstance(errors[0], TodoError)
    assert errors[0].message == "This will become an error"
