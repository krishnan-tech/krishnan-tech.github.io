### 1. Lab: Authentication bypass via OAuth implicit flow
> This lab uses an OAuth service to allow users to log in with their social media account. Flawed validation by the client application makes it possible for an attacker to log in to other users' accounts without knowing their password.
To solve the lab, log in to Carlos's account. His email address is `carlos@carlos-montoya.net`.
You can log in with your own social media account using the following credentials: `wiener:peter`.

This application sends the requests and responses that make up the OAuth flow. This starts from the authorization request `GET /auth?client_id=[...]`. We will see one endpoint named as `/authenticate`. 
![[Pasted image 20250904202703.png]]
By simply sending carlos email and sending the request in browser will set the cookies and solve the lab.
![[Pasted image 20250904202635.png]]
![[Pasted image 20250904202642.png]]
### 2. Lab: Forced OAuth profile linking
> This lab gives you the option to attach a social media profile to your account so that you can log in via OAuth instead of using the normal username and password. Due to the insecure implementation of the OAuth flow by the client application, an attacker can manipulate this functionality to obtain access to other users' accounts.
To solve the lab, use a CSRF attack to attach your own social media profile to the admin user's account on the blog website, then access the admin panel and delete `carlos`.
The admin user will open anything you send from the exploit server and they always have an active session on the blog website.
You can log in to your own accounts using the following credentials:
- Blog website account: `wiener:peter`
- Social media profile: `peter.wiener:hotdog`

While proxying traffic through Burp, I discovered that the blog's social media login flow lacked a `state` parameter, leaving it vulnerable to CSRF. After linking my social media account, I intercepted the OAuth linking request, copied the `GET /oauth-linking?code=[...]` URL, and dropped it to keep the code valid. I then crafted an exploit on the exploit server using an iframe that pointed to the stolen URL. When the victim loaded the page, their account was linked to my social media profile, allowing me to log in as the admin via social media authentication. Finally, I accessed the admin panel and deleted Carlos to complete the lab.
![[Pasted image 20250904211827.png]]
Payload:
```html
<iframe src="https://0a02004d04d27c1b82a8f68a0031005d.web-security-academy.net/oauth-linking?code=zeliVuDv5hBziRD4lYU7uyWyTepzjpUVVev77AJegsw"></iframe>
```
### 3. Lab: OAuth account hijacking via redirect_uri
> This lab uses an OAuth service to allow users to log in with their social media account. A misconfiguration by the OAuth provider makes it possible for an attacker to steal authorization codes associated with other users' accounts.
To solve the lab, steal an authorization code associated with the admin user, then use it to access their account and delete the user `carlos`.
The admin user will open anything you send from the exploit server and they always have an active session with the OAuth service.
You can log in with your own social media account using the following credentials: `wiener:peter`.


While intercepting traffic through Burp, I clicked on **"My account"** and completed the OAuth login process, which redirected me back to the blog website. After logging out and logging back in, I noticed that I was instantly authenticated since my active session with the OAuth provider meant no credentials were required. I then examined the OAuth flow in Burp’s proxy history and found the most recent authorization request beginning with `GET /auth?client_id=[...]`. This request redirected directly to the `redirect_uri` along with the authorization code. Sending this request to Burp Repeater, I discovered that I could supply any arbitrary value as the `redirect_uri` and the server would accept it, reflecting it in the response. By changing the `redirect_uri` to point to my exploit server and following the redirect, I confirmed in the exploit server's access logs that an authorization code was successfully leaked. 
![[Pasted image 20250904214116.png]]
![[Pasted image 20250904214127.png]]
To weaponize this, I hosted an iframe on the exploit server that triggered the vulnerable authorization request with my exploit server as the redirect URI. Viewing the exploit showed that the iframe loaded correctly, and my server logs captured the leaked code. Once I delivered this exploit to the victim, their authorization code was also logged on my server. With that stolen code, I logged out of my own session and navigated to `/oauth-callback?code=STOLEN-CODE`, which completed the OAuth flow and authenticated me as the admin user. From there, I accessed the admin panel and deleted Carlos, successfully solving the lab.
### 4. Lab: Stealing OAuth access tokens via an open redirect
> This lab uses an OAuth service to allow users to log in with their social media account. Flawed validation by the OAuth service makes it possible for an attacker to leak access tokens to arbitrary pages on the client application.
To solve the lab, identify an open redirect on the blog website and use this to steal an access token for the admin user's account. Use the access token to obtain the admin's API key and submit the solution using the button provided in the lab banner.
The admin user will open anything you send from the exploit server and they always have an active session with the OAuth service.
You can log in via your own social media account using the following credentials: `wiener:peter`.

description