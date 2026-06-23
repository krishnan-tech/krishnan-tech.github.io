## Buckets of Fun
We all know that public buckets are risky. But can you find the flag?
Link: https://bigiamchallenge.com/challenge/1

IAM Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::thebigiamchallenge-storage-9979f4b/*"
        },
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::thebigiamchallenge-storage-9979f4b",
            "Condition": {
                "StringLike": {
                    "s3:prefix": "files/*"
                }
            }
        }
    ]
}
```
Let's break down the policy
### Policy overview
```json
{  
	"Version": "2012-10-17",  
	"Statement": [ ... ]  
}
```
- `"Version"` → policy language version (standard AWS value).
- `"Statement"` → individual permission rules.
## Statement 1: Anyone can download objects

```json
{  
	"Effect": "Allow",  
	"Principal": "*",  
	"Action": "s3:GetObject",  
	"Resource": "arn:aws:s3:::thebigiamchallenge-storage-9979f4b/*"  
}
```
### Meaning:
- `"Effect": "Allow"` → grant access.
- `"Principal": "*"` → **everyone on the internet** (anonymous access allowed).
- `"Action": "s3:GetObject"` → permission to **read/download objects**.
- `"Resource": ".../*"` → applies to **all objects inside the bucket**.
### Result:
If someone already knows the object path, they can fetch it.
Example:
```
https://thebigiamchallenge-storage-9979f4b.s3.amazonaws.com/files/example.txt
```
If `example.txt` exists → downloadable.
But this statement **does not let you discover filenames**.

## Statement 2: Anyone can list only `files/`
```json
{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:ListBucket",
    "Resource": "arn:aws:s3:::thebigiamchallenge-storage-9979f4b",
    "Condition": {
        "StringLike": {
            "s3:prefix": "files/*"
        }
    }
}
```
### Meaning:
- Allows `s3:ListBucket`
- But only when listing with prefix: `files/`
files/
### Result:
Anyone can ask:
```bash
C:\Users\krish>aws s3 ls s3://thebigiamchallenge-storage-9979f4b/files/
2023-06-05 15:13:53         37 flag1.txt
2023-06-08 15:18:24      81889 logo.png
```


## Solution
List the bucket and use `aws s3 cp` to copy file and use `-` to print the content of the file or use `.` to download file locally.
```bash
C:\Users\krish>aws s3 cp s3://thebigiamchallenge-storage-9979f4b/files/flag1.txt -
{wiz:exposed-storage-risky-as-usual}
```
Link to flag: https://thebigiamchallenge-storage-9979f4b.s3.amazonaws.com/files/flag1.txt

> Flag: `{wiz:exposed-storage-risky-as-usual}`