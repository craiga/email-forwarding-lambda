"""Test handling an unknown event."""

import logging

import moto
import pytest

import email_forwarding


@moto.mock_s3  # type: ignore
@moto.mock_ses  # type: ignore
def test_unknown_source(caplog: pytest.LogCaptureFixture) -> None:
    """Test handling an unknown event source."""
    with caplog.at_level(logging.WARNING):
        email_forwarding.lambda_handler(
            {
                "Records": [
                    {
                        "eventSource": "aws:something-else",
                        "eventName": "ObjectCreated:Put",
                    }
                ]
            },
            None,
        )

    assert "Unknown event" in caplog.text


@moto.mock_s3  # type: ignore
@moto.mock_ses  # type: ignore
def test_unknown_name(caplog: pytest.LogCaptureFixture) -> None:
    """Test handling an unknown event name."""
    with caplog.at_level(logging.WARNING):
        email_forwarding.lambda_handler(
            {"Records": [{"eventSource": "aws:s3", "eventName": "something-else"}]},
            None,
        )

    assert "Unknown event" in caplog.text
