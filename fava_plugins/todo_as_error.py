"""Create errors for entries 'todo' metadata.

When enabling the `todo_as_error`-plugin, transactions with the
`todo`-metadata-key will be added as Beancount errors, displaying the value of
the `todo`-metadata-entry as the error description.

    plugin "fava_plugins.todo_as_error"

    2017-12-27 * "" "Groceries"
      todo: "Put the milk into the fridge"
      Expenses:Groceries   150.00 USD
      Assets:Cash
"""

from __future__ import annotations

from typing import Any
from typing import NamedTuple
from typing import TYPE_CHECKING

from beancount.core.data import Transaction

if TYPE_CHECKING:
    from beancount.core.data import Directive
    from beancount.core.data import Meta

__plugins__ = [
    "todo_as_error",
]


class TodoError(NamedTuple):
    """Error from the split_income plugin."""

    source: Meta
    message: str
    entry: Directive


def todo_as_error(
    entries: list[Directive],
    _: Any,
) -> tuple[list[Directive], list[TodoError]]:
    """Create errors for entries 'todo' metadata."""
    errors = [
        TodoError(entry.meta, entry.meta["todo"], entry)
        for entry in entries
        if isinstance(entry, Transaction) and "todo" in entry.meta
    ]

    return entries, errors
