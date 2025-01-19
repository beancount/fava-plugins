from beancount.core import data
from beancount.loader import load_string


def _compare_postings(entry1, entry2):
    amounts = {}
    for pos in entry1.postings:
        amounts[pos.account] = pos.units.number
    for pos in entry2.postings:
        assert amounts[pos.account] == pos.units.number


def test_split_income(load_doc):
    """
    plugin "fava_plugins.split_income" ""
    plugin "beancount.plugins.auto_accounts"

    2018-01-31 * "Employer" "Income"
        Income:Work                  -1000.00 EUR
        Income:Work:Bonus             -100.00 EUR
        Expenses:Taxes                 180.00 EUR
        Expenses:Taxes:Extra            20.00 EUR
        Assets:Account                 900.00 EUR
    """

    entries, errors, __ = load_doc

    entries_after, _, __ = load_string(
        """
    2018-01-31 * "Employer" "Income"
        Income:Net:Work               -800.00 EUR
        Income:Net:Work:Bonus         -100.00 EUR
        Assets:Account                 900.00 EUR

    2018-01-31 * "Employer" "Income" #pretax
        Income:Work                  -1000.00 EUR
        Income:Work:Bonus             -100.00 EUR
        Expenses:Taxes                 180.00 EUR
        Expenses:Taxes:Extra            20.00 EUR
        Income:Net:Work                800.00 EUR
        Income:Net:Work:Bonus          100.00 EUR
    """,
        dedent=True,
    )

    assert not errors
    assert "pretax" in entries[8].tags

    _compare_postings(entries[8], entries_after[1])
    _compare_postings(entries[7], entries_after[0])

    assert len(entries) == 9
    assert len([e for e in entries if isinstance(e, data.Open)]) == 7


def test_split_income_config(load_doc):
    """
    plugin "fava_plugins.split_income" "{
        'income': 'Income:Work',
        'net_income': 'Income:Net-Income',
        'taxes': 'Expenses:Taxes',
        'tag': 'brutto',
    }"
    plugin "beancount.plugins.auto_accounts"

    2018-01-31 * "Employer" "Income"
        Income:Work                  -1000.00 EUR
        Income:Work:Bonus             -100.00 EUR
        Expenses:Taxes                 180.00 EUR
        Expenses:Taxes:Extra            20.00 EUR
        Assets:Account                 900.00 EUR
    """

    entries, errors, __ = load_doc

    entries_after, _, __ = load_string(
        """
    2018-01-31 * "Employer" "Income"
        Income:Net-Income             -800.00 EUR
        Income:Net-Income:Bonus       -100.00 EUR
        Assets:Account                 900.00 EUR

    2018-01-31 * "Employer" "Income" #pretax
        Income:Work                  -1000.00 EUR
        Income:Work:Bonus             -100.00 EUR
        Expenses:Taxes                 180.00 EUR
        Expenses:Taxes:Extra            20.00 EUR
        Income:Net-Income              800.00 EUR
        Income:Net-Income:Bonus        100.00 EUR
    """,
        dedent=True,
    )

    assert not errors
    assert "brutto" in entries[8].tags

    _compare_postings(entries[8], entries_after[1])
    _compare_postings(entries[7], entries_after[0])

    assert len(entries) == 9
    assert len([e for e in entries if isinstance(e, data.Open)]) == 7


def test_split_income_mixed_currency_income(load_doc):
    """
    plugin "fava_plugins.split_income" ""
    plugin "beancount.plugins.auto_accounts"

    2025-01-01 * "Employer" "Income"
        Income:Work                       -10 USD @@ 9 EUR
        Expenses:Taxes                      1 EUR
        Assets:Account                      8 EUR
    """

    entries, errors, __ = load_doc

    entries_after, _, __ = load_string(
        """
    2025-01-01 * "Employer" "Income"
        Assets:Account                      8 EUR
        Income:Net:Work                    -8 EUR

    2025-01-01 * "Employer" "Income" #pretax
        Income:Work                       -10 USD @ 0.9 EUR
        Expenses:Taxes                     1 EUR
        Income:Net:Work                    8 EUR
    """,
        dedent=True,
    )

    assert not errors
    assert "pretax" in entries[5].tags

    _compare_postings(entries[5], entries_after[1])
    _compare_postings(entries[4], entries_after[0])

    assert len(entries) == 6
    assert len([e for e in entries if isinstance(e, data.Open)]) == 4


def test_split_income_mixed_currency_others(load_doc):
    """
    plugin "fava_plugins.split_income" ""
    plugin "beancount.plugins.auto_accounts"

    2025-01-01 * "Employer" "Income"
        Income:Work                       -11 USD
        Expenses:Taxes                      1 EUR @ 1.1 USD
        Assets:Account                      9 EUR @ 1.1 USD
    """

    entries, errors, __ = load_doc

    entries_after, _, __ = load_string(
        """
    2025-01-01 * "Employer" "Income"
        Assets:Account                      9 EUR @ 1.1 USD
        Income:Net:Work                  -9.9 USD

    2025-01-01 * "Employer" "Income" #pretax
        Income:Work                       -11 USD
        Expenses:Taxes                     1 EUR @ 1.1 USD
        Income:Net:Work                    9.9 USD
    """,
        dedent=True,
    )

    assert not errors
    assert "pretax" in entries[5].tags

    _compare_postings(entries[5], entries_after[1])
    _compare_postings(entries[4], entries_after[0])

    assert len(entries) == 6
    assert len([e for e in entries if isinstance(e, data.Open)]) == 4
