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

import collections

from beancount.core.data import Transaction

__plugins__ = [
    'todo_as_error',
]

TodoError = collections.namedtuple('TodoError', 'source message entry')


def todo_as_error(entries, _):
    """Create errors for entries 'todo' metadata."""
    errors = []

    for entry in entries:
        if isinstance(entry, Transaction) and 'todo' in entry.meta:
            errors.append(TodoError(entry.meta, entry.meta['todo'], entry))

    return entries, errors
