"""Forward email."""

import email
import json
import logging
import os
from tempfile import TemporaryFile
from typing import Any, Mapping

import boto3

logging.captureWarnings(True)
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def lambda_handler(event: Mapping[str, Any], context: object) -> None:
    logger.debug("recieved event: %s", json.dumps(event))
    s3 = boto3.client("s3")
    ses = boto3.client("ses")

    subject_prefix = os.environ.get("SUBJECT_PREFIX", "Fwd by λ🤖: ")
    try:
        recipients = os.environ["RECIPIENTS"]
    except KeyError as err:
        raise RuntimeError(
            "No recipients defined. Make sure a RECIPIENTS environment variable is set"
            ' in the format "Recipient a <a@example.com>; <b@example.com>"'
        ) from err

    try:
        forwarder = os.environ["FORWARDER"]
    except KeyError as err:
        raise RuntimeError(
            "No forwarder defined. Make sure a FORWARDER environment variable is set"
            ' in the format "Forwarding 🤖 <bot@example.com>"'
        ) from err

    for record in event["Records"]:
        if (
            record["eventSource"] == "aws:s3"
            and record["eventName"] == "ObjectCreated:Put"
        ):

            with TemporaryFile() as message_file:
                s3.download_fileobj(
                    record["s3"]["bucket"]["name"],
                    record["s3"]["object"]["key"],
                    message_file,
                )
                message_file.seek(0)
                message = email.message_from_binary_file(message_file)

                logger.debug("Read message keys: %s", json.dumps(message.keys()))

                message.replace_header("Subject", subject_prefix + message["Subject"])
                message.replace_header("To", recipients)

                if not "Reply-To" in message:
                    message.add_header("Reply-To", message["From"])

                message.replace_header("From", forwarder)
                del message["DKIM-Signature"]

                logger.debug("Sending message: %s", json.dumps(str(message)))

                ses.send_raw_email(RawMessage={"Data": bytes(message)})

        else:
            logger.warning("Unknown event: %s", json.dumps(event))
