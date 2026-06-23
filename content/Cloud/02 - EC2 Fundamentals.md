- EC2 is one of the most popular of AWS offering
- EC2 = Elastic Compute Cloud = Infrastructure as a Service
- It mainly consists in the capability of:
	- Renting virtual machines (EC2)
	- Storing data on virtual drives (EBS)
	- Distributing load across machines (ELB)
	- Scaling the services using an auto-scaling group (ASG)
- Operating system: Linux, Windows or Mac OS
- HOw much compute power & core (CPU)
- How much random-access memory (RAM)
- How much storage space:
	- Network-attached (EBS & EFS)
	- hardware (EC2 Instance Store)
- Network card: speed of the card, Public IP address
- Firewall rules: security group
- Bootstrap script (configure at first launch): EC2 User Data
	- Install updates, softwares, downloading common files from the internet etc
	- Installed with SUDO
- Basic Instance types
	- ![[Pasted image 20260616160109.png]]
## Launching EC2 Instance
`EC2 -> Instances -> Create Instance`
- Write the name of instance -> keep Amazon Linux type -> keep default instance type t2.micro ->  generate key pair (RSA / pem) -> Network Settings (check ssh, http) -> default storage (advanced, check delete on termination - yes)
![[Pasted image 20260616161710.png]]More info about instance type: https://instances.vantage.sh/

***NOTE: Every time we stop and start the instance, IP will change***
### Launch instance from SSH
- `ssh -i key.pem ec2@IP`
	- set key permissions: `chmod 400 key.pem`
	- for windows - the owner of the file should be the user running the command (not admin)
- Or use cloud shell (`go to your instance -> connect` / username `ec2-user`)
## Security Groups
`Instances -> Select our instance -> Security`
- there are 2 rules -> Inbound and Outbound Rules
	- Allow SSH (port 22), HTTP (port 80) etc
	- ![[Pasted image 20260616162249.png]]

## Instance Roles
It's a bad idea to configure `aws configure` and pass creds into EC2 instance, because if the instance got compromised, creds will too!! So that's why we use roles instead. Whatever policy we will use in that role will be automatically applied to that instance, so we dont have to configure creds, it will inherit automatically.
From IAM roles for services ![[01 - IAM & AWS CLI#IAM Roles for Services]]
`Select Instance -> Action -> Security -> IAM Role (choose role)`
## EC2 Dedicated Hosts
• A physical server with EC2 instance capacity fully dedicated to your use
• Allows you address compliance requirements and use your existing server- bound software licenses (per-socket, per-core, pe - VM software licenses)
• Purchasing Options:
• On-demand – pay per second for active Dedicated Host
• Reserved - 1 or 3 years (No Upfront, Partial Upfront, All Upfront)
• The most expensive option
• Useful for software that have complicated licensing model (BYOL – Bring Your Own License)
• Or for companies that have strong regulatory or compliance needs

## Which purchasing option is right for me?
• On demand: coming and staying in resort whenever we like, we pay the full price
• Reserved: like planning ahead and if we plan to stay for a long time, we may get a good discount.
• Savings Plans: pay a certain amount per hour for certain period and stay in any room type (e.g.,
King, Suite, Sea View, …)
• Spot instances: the hotel allows people to bid for the empty rooms and the highest bidder keeps the rooms. You can get kicked out at any time
• Dedicated Hosts: We book an entire building of the resort
• Capacity Reservations: you book a room for a period with full price even you don’t stay in it
![[Pasted image 20260616163340.png]]
