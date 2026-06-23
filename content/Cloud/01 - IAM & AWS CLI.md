## IAM: Users & Group

- IAM = Identity and Access Management, Global service
- Root account created by default, shouldn't be used or shared
- Users are people within your org, and can be grouped
- Group only contain users, not other groups
  ![[Pasted image 20260615162318.png]]

## IAM: Permissions

- Users and Group can be assigned JSON documents called policies
  ![[Pasted image 20260615162406.png]]
  `aws console -> IAM -> Users -> Create User` (why we create user? It's not good practice to do stuff with root user). If we want to create Admin IAM user, attach `AdministratorAccess` policy to that user group.

## Create IAM user

Step 1: Specify User details - includes username and checkbox to provide user access to AWS management console
![[Pasted image 20260615163902.png]]
Step 2: Set Permissions - total three options to set permission.

- Add user to group (meaning - it will inherit all the permission from that group)
  - ![[Pasted image 20260615164148.png]]
- Copy Permissions - it will copy exact permission from users
  - ![[Pasted image 20260615164209.png]]
- Attach Policy Directly - it will directly attach policies to that particular user - ![[Pasted image 20260615164229.png]]
  Step 3 onwards: Summary and Review step to verify everything before creating user.

Typical Policy looks like this
![[Pasted image 20260615164526.png]]

## Password Policy

`IAM -> Account Settings -> Password Policy`
![[Pasted image 20260615164842.png]]
For root user MFA -> `Profile -> Security Credentials -> MFA`
![[Pasted image 20260615165018.png]]

## AWS CLI

- Download CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
- go to `IAM Users -> Select User -> Security Credentials -> Access Key`
- in terminal -> `aws configure` (provide creds in command line)
- Verify: `aws sts get-caller-identity`
  ![[Pasted image 20260615170409.png]]

## IAM Roles for Services

Roles are used to attach IAM Policies for Services, for example if we want to give IAM read only policy to an EC2 instance, then we can define a role for it. (but for this, we have to attach this role to our EC2 instance)
![[Pasted image 20260615170611.png]]

## IAM Guidelines & Best Practices

- Don’t use the root account except for AWS account setup
- One physical user = One AWS user
- Assign users to groups and assign permissions to groups
- Create a strong password policy
- Use and enforce the use of Multi Factor Authentication (MFA)
- Create and use Roles for giving permissions to AWS services
- Use Access Keys for Programmatic Access (CLI / SDK)
- Audit permissions of your account using IAM Credentials Report & IAM Access Advisor
- Never share IAM users & Access Keys

## Summary

• Users: mapped to a physical user, has a password for AWS Console
• Groups: contains users only
• Policies: JSON document that outlines permissions for users or groups
• Roles: for EC2 instances or AWS services
• Security: MFA + Password Policy
• AWS CLI: manage your AWS services using the command-line
• AWS SDK: manage your AWS services using a programming language
• Access Keys: access AWS using the CLI or SDK
• Audit: IAM Credential Reports & IAM Access Advisor

## Practice Flaws.Cloud Level 1,2

- ![[cloud/flaws.cloud/level1]]
- ![[cloud/flaws.cloud/level2]]

## Practice BigIAMChallenge Challenge 1,2

- ![[cloud/bigiamchallenge/Challenge 1]]
- ![[cloud/bigiamchallenge/Challenge 2]]
