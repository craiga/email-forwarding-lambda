"""Global test fixtures."""

import os
from typing import Generator
from unittest import mock

import pytest


@pytest.fixture(autouse=True)
def mock_recipients() -> Generator[None, None, None]:
    """Recipients configuration."""
    with mock.patch.dict(
        os.environ,
        {"RECIPIENTS": "Craig Anderson <craiga@craiga.id.au>, <craig@uhf62.co.uk>"},
    ):
        yield


@pytest.fixture(autouse=True)
def mock_forwarder() -> Generator[None, None, None]:
    """Email address configuration."""
    with mock.patch.dict(
        os.environ, {"FORWARDER": "Craig Anderson <craiga@craiga.id.au>"}
    ):
        yield
