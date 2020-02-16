import pytest

from noverde_challenge import __version__, configure_sentry, set_remote_debug
from noverde_challenge.utils.helpers import only_numbers
from noverde_challenge.utils.secrets import get_secret
from noverde_challenge.utils.status_code import StatusCode


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.parametrize(
    "name, value",
    [
        ("OK", 200),
        ("BAD_REQUEST", 400),
        ("CREATED", 201),
        ("INTERNAL_ERROR", 500),
        ("NOT_FOUND", 404),
    ],
)
def test_status_code(name, value):
    assert StatusCode[name].value == value


def test_get_secret(monkeypatch):
    monkeypatch.setenv("NOVERDE_API_TOKEN", "FOOBar")
    secret = get_secret("/noverde/api/token")
    assert secret == "FOOBar"


def test_do_not_start_remote_debug(monkeypatch):
    monkeypatch.setenv("IS_LOCAL", True)
    assert not set_remote_debug()


def test_do_not_start_sentry(monkeypatch):
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    assert not configure_sentry()


def test_only_numbers():
    test = ".+@abcd123&45efgh67_=-"
    assert only_numbers(test) == "1234567"
