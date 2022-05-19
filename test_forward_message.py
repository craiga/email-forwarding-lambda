"""Test forwarding a message."""

import os
from unittest import mock

import boto3
import moto

import email_forwarding


@moto.mock_s3  # type: ignore
@moto.mock_ses  # type: ignore
def test_forward_message() -> None:
    """Test forwarding a message."""
    # Set up message in S3.
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="my-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
    )
    s3.put_object(
        Bucket="my-bucket",
        Key="message-key",
        Body=b"""Date: Tue, 17 May 2022 20:49:29 +0000
To: recipient@example.com
From: Amazon Web Services <no-reply-aws@amazon.com>
Subject: Amazon SES Setup Notification

Hello,

You received this message because you attempted to set up Amazon SES to deliver emails to this S3 bucket.

Please note that the rule that you configured to deliver emails to this S3 bucket is only valid if the entire setup process is successful. For more information about
setting up email-receiving rules, see the Amazon SES Developer Guide at http://docs.aws.amazon.com/ses/latest/DeveloperGuide/Welcome.html .

Thank you for using Amazon SES!

The Amazon SES Team
""",
    )

    # Verify email identity
    ses = boto3.client("ses")
    ses.verify_email_identity(EmailAddress="forwarder@example.com")

    with mock.patch.dict(os.environ, {"FORWARDER": "forwarder@example.com"}):
        email_forwarding.lambda_handler(
            {
                "Records": [
                    {
                        "eventSource": "aws:s3",
                        "eventName": "ObjectCreated:Put",
                        "s3": {
                            "bucket": {"name": "my-bucket"},
                            "object": {"key": "message-key"},
                        },
                    }
                ]
            },
            None,
        )

    send_stats = ses.get_send_statistics()
    assert len(send_stats["SendDataPoints"]) == 1
