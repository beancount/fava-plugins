"""Create errors for entries 'todo' metadata."""
import collections

from beancount.core.data import Transaction

__plugins__ = ['todo_as_error', ]

TodoError = collections.namedtuple('TodoError', 'source message entry')


def todo_as_error(entries, _):
    """Create errors for entries 'todo' metadata.

    Go through all Transaction entries that have the 'todo'-metadata-entry
    and creates errors from these entries.
    """
    errors = []

    for entry in entries:
        if isinstance(entry, Transaction) and 'todo' in entry.meta:
            errors.append(TodoError(entry.meta, entry.meta['todo'], entry))

    return entries, errors
