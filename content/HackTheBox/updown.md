---
title: UpDown
date: 2024-12-21
description: "Detailed walkthrough of the UpDown\r machine on HackTheBox platform, covering initial enumeration, exploiting vulnerabilities, and obtaining user and root flags."
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - TryHackMe
categories:
  - TryHackMe
  - TryHackMe/Linux
image: images/0day/banner.jpeg
---

# UpDown

| Title       | UpDown                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Description | UpDown is a medium difficulty Linux machine with SSH and Apache servers exposed. On the Apache server a web application is featured that allows users to check if a webpage is up. A directory named `.git` is identified on the server and can be downloaded to reveal the source code of the `dev` subdomain running on the target, which can only be accessed with a special `HTTP` header. Furthermore, the subdomain allows files to be uploaded, leading to remote code execution using the `phar://` PHP wrapper. The Pivot consists of injecting code into a `SUID` `Python` script and obtaining a shell as the `developer` user, who may run `easy_install` with `Sudo`, without a password. This can be leveraged by creating a malicious python script and running `easy_install` on it, as the elevated privileges are not dropped, allowing us to maintain access as `root`. |
| Difficulty  | Medium                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Maker       | [AB2](https://app.hackthebox.com/users/1303)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

## Nmap

```bash
─$ cat nmap/tcp_default.nmap
# Nmap 7.94SVN scan initiated Thu Dec 19 22:25:00 2024 as: /usr/lib/nmap/nmap -sCV -T4 --min-rate 10000 -p- -v -oA nmap/tcp_default 10.129.227.227
Increasing send delay for 10.129.227.227 from 0 to 5 due to 5608 out of 14019 dropped probes since last increase.
Warning: 10.129.227.227 giving up on port because retransmission cap hit (6).
Nmap scan report for updown.htb (10.129.227.227)
Host is up (0.18s latency).
Not shown: 64927 closed tcp ports (reset), 606 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 9e:1f:98:d7:c8:ba:61:db:f1:49:66:9d:70:17:02:e7 (RSA)
|   256 c2:1c:fe:11:52:e3:d7:e5:f7:59:18:6b:68:45:3f:62 (ECDSA)
|_  256 5f:6e:12:67:0a:66:e8:e2:b7:61:be:c4:14:3a:d3:8e (ED25519)
80/tcp open  http    Apache httpd 2.4.41
| http-methods:
|_  Supported Methods: HEAD
Service Info: Host: localhost; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

From the results of nmap, we know there are 2 ports that are open, that is http and ssh.
![[Pasted image 20241221052930.png]]
After adding `updown.htb` to `/etc/hosts` we can access the website. More importantly, we found another domain. Adding this domain to `/etc/hosts` and visiting the website will give us same results.
If we try to pass `http://google.com;ls` then the website will give `Hacking attempy detected` error. Moreover, I have tried different payloads, all giving same results.
![[Pasted image 20241221053348.png]]
Trying to find subdomains from website and we found `dev` subdomain, adding that to `/etc/hosts`.
![[Pasted image 20241221223027.png]]
Moving to the next part, I have tried directory bruteforcing. I have used `gobuster` for directory bruteforce.
![[Pasted image 20241221053537.png]]
Found `/dev` directory, let's try to get content from that directory.
![[Pasted image 20241221221211.png]]
Found `/.git/HEAD`. So git directory is been exposed to users. Let's download the content using `git-dumper` - `git-dumper http://updown.htb/dev/ ./git/`. After downloading the content we have downloaded these files. Let's inspect these files!

```bash
┌─[g4nd1v☺htb-ovo92mui3j]─[~/updown/git]
└──╼ $ls -al
total 40
drwxr-xr-x 3 g4nd1v g4nd1v 4096 Dec 21 21:25 .
drwxr-xr-x 3 g4nd1v g4nd1v 4096 Dec 21 21:11 ..
-rw-r--r-- 1 g4nd1v g4nd1v   59 Dec 21 21:11 admin.php
-rw-r--r-- 1 g4nd1v g4nd1v  147 Dec 21 21:11 changelog.txt
-rw-r--r-- 1 g4nd1v g4nd1v 3145 Dec 21 21:11 checker.php
drwxr-xr-x 7 g4nd1v g4nd1v 4096 Dec 21 21:11 .git
-rw-r--r-- 1 g4nd1v g4nd1v  117 Dec 21 21:11 .htaccess
-rw-r--r-- 1 g4nd1v g4nd1v  273 Dec 21 21:11 index.php
-rw-r--r-- 1 g4nd1v g4nd1v 5531 Dec 21 21:11 stylesheet.css
```
