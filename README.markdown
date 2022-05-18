# Email forwarding lambda

Python function to forward emails in AWS. Takes an email written to an S3 bucket, and then forwards it on.

I'm using this to forward emails which are received by SES, and then written to an S3 bucket (FWIW, email notifications received directly from SES don't appear to include the body of the email message).

## Manually releasing

```
make email_forwarding.zip
aws lambda update-function-code --function-name email_forwarding --zip-file fileb://email_forwarding.zip
```
