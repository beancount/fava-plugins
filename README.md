# fava-plugins
a collection of Beancount plugins

### Display 'todo'-metadata-entries as errors

When enabling the `todo_as_error`-plugin, transactions with the
`todo`-metadata-key will be added as Beancount errors, displaying the value of
the `todo`-metadata-entry as the error description.

    plugin "fava_plugins.todo_as_error"

    2017-12-27 * "" "Groceries"
      todo: "Put the milk into the fridge"
      Expenses:Groceries   150.00 USD
      Assets:Cash
