---
title: Vintage
date: 2024-04-27
description: Detailed walkthrough of the Vintage room on HackTheBox platform, covering initial enumeration, exploiting vulnerabilities, and obtaining user and root flags.
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
categories:
  - HackTheBox
  - HackTheBox/Windows
  - HackTheBox/Windows/AD
image: images/Vintage/banner.jpeg
---

| Title       | [Vintage](https://app.hackthebox.com/machines/Vintage)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description | Vintage is a hard difficulty Windows machine designed around an assumed breach scenario, where the attacker is provided with low-privileged user credentials. The machine features an Active Directory environment without ADCS installed, and NTLM authentication is disabled. There is a &quot;Pre-Created computer account,&quot; meaning the password is the same as the sAMAccountName of the machine account. The &quot;Domain Computer&quot; organisational unit (OU) has a configuration allowing attackers to read the service account password, which has gMSA configured. After obtaining the password, the service account can add itself to a privileged group. The group has complete control over a disabled user. The attacker is supposed to restore the disabled user and set a Service Principal Name (SPN) to perform Kerberoasting. After recovering the password, the user account has reused the same password. The newly compromised user has a password stored in the Credential Manager. The user can add itself to another privileged group configured for Resource-Based Constrained Delegation (RBCD) on the Domain Controller, allowing the attacker to compromise it. |
| Difficulty  | Hard                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Maker       | [Geiseric](https://app.hackthebox.com/users/184611)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

## Initial Credentials

| Username | Password      |
| -------- | ------------- |
| P.Rosa   | Rosaisbest123 |

## Nmap

```bash
└─$ nmap -sC -sV -oA nmap/vintage 10.10.11.45
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-27 19:31 EDT
Nmap scan report for 10.10.11.45
Host is up (0.098s latency).
Not shown: 988 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-04-27 23:31:31Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: vintage.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: vintage.htb0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode:
|   3:1:1:
|_    Message signing enabled and required
|_clock-skew: -1s
| smb2-time:
|   date: 2025-04-27T23:31:38
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 60.63 seconds
```

From nmap results

- we can see on the domain is `vintage.htb`, `dc01.vintage.htb`, and `dc01` -> adding that to `/etc/hosts`.
- smb port is also open
- there is LDAP service running on port 3268
  I have tried logging with `smbclient` - but didn't got anything.

```bash
└─$ smbclient -L \\10.10.11.45 -U p.rosa
session setup failed: NT_STATUS_NOT_SUPPORTED
```

Next, I have tried to use `enum4linux-ng` - but didn't found anything useful from this. Let's try to dig more using `rpcclient`

```bash
└─$ enum4linux-ng 10.10.11.45 -u p.rosa -p Rosaisbest123
```

I have tried checking the creds using `netexec` and I have found NTLM auth is disabled.
![[Pasted image 20250427195450.png]]
I have checked shares using `netexec` but nothing seems to be interesting here. Let's see if we can get anything out of bloodhound using `nxc`
![[Pasted image 20250427195940.png]]
Bloodhound using `nxc`

```
$ nxc ldap dc01.vintage.htb -u P.Rosa -p Rosaisbest123 -k --bloodhound --collection All --dns-server 10.10.11.45
```

Got all bloodhound data, let's upload to bloodhound and analyze it!
