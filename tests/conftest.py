import pytest
from beancount.loader import load_string


@pytest.fixture
def load_doc(request):
    return load_string(request.function.__doc__, dedent=True)
