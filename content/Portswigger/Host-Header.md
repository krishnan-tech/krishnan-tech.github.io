### 1. Lab: Web cache poisoning via ambiguous requests
> This lab is vulnerable to web cache poisoning due to discrepancies in how the cache and the back-end application handle ambiguous requests. An unsuspecting user regularly visits the site's home page.
To solve the lab, poison the cache so the home page executes `alert(document.cookie)` in the victim's browser.

In this application, on homepage, if we add `/?cachebuster=1` we can able to burst cache and if we pass in another host, it will be reflected in the response. So we will make use of that and give alert.
![[Pasted image 20250910202645.png]]
### 2. Lab: Host header authentication bypass
> This lab makes an assumption about the privilege level of the user based on the HTTP Host header.
To solve the lab, access the admin panel and delete the user `carlos`.

I have checked robots.txt and in that page, it says `/admin` is not allowed, we will go to `/admin` and it says only local user can access it.
![[Pasted image 20250910213456.png]]
So I have changed the host to localhost and send the request again, and it worked.
![[Pasted image 20250910213432.png]]
Now, deleting carlos user will solve the lab.
### 3. Lab: Routing-based SSRF
> This lab is vulnerable to routing-based SSRF via the Host header. You can exploit this to access an insecure intranet admin panel located on an internal IP address.
To solve the lab, access the internal admin panel located in the `192.168.0.0/24` range, then delete the user `carlos`.

I have changed the host and sent it to intruder for the last octet and found `206`. So I have access to `/admin`.
![[Pasted image 20250911163358.png]]
Next I have reviewed code for admin and got CSRF token from there, sending the request to delete carlos user will solve the lab.
![[Pasted image 20250911163343.png]]
Here's the request to delete carlos user.
![[Pasted image 20250911163329.png]]
### 4. Lab: SSRF via flawed request parsing
> This lab is vulnerable to routing-based SSRF due to its flawed parsing of the request's intended host. You can exploit this to access an insecure intranet admin panel located at an internal IP address.
To solve the lab, access the internal admin panel located in the `192.168.0.0/24` range, then delete the user `carlos`.

