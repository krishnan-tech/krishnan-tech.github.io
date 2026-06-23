### 1. Lab: Unprotected admin functionality
> This lab has an unprotected admin panel.
Solve the lab by deleting the user `carlos`.

On `/robots.txt` we got the admin portal
![[Pasted image 20250807074024.png]]
On deleting the carlos user from admin portal will solve the lab
> Solution: check `robots.txt` file

### 2. Lab: Unprotected admin functionality with unpredictable URL
> This lab has an unprotected admin panel. It's located at an unpredictable location, but the location is disclosed somewhere in the application.
Solve the lab by accessing the admin panel, and using it to delete the user `carlos`.

If we check the source code, we will see the admin portal URL.
![[Pasted image 20250807074154.png]]
On visiting that, we can able to get the panel
> Solution: Check source code to find hidden URL

### 3. Lab: User role controlled by request parameter
> This lab has an admin panel at `/admin`, which identifies administrators using a forgeable cookie.
Solve the lab by accessing the admin panel and using it to delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

When we visit `/admin` it says `Admin interface only available if logged in as an administrator`, so we will log into our account and then check the cookies.
![[Pasted image 20250807074403.png]]
Changing the cookie value of `Admin` to `true` will give us access to admin portal.
> Solution: Check cookies

### 4. Lab: User role can be modified in user profile
> This lab has an admin panel at `/admin`. It's only accessible to logged-in users with a `roleid` of 2.
Solve the lab by accessing the admin panel and using it to delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

When we login as `wiener` and then change the email, we see there is a roleid reflected in response, so what if we try to add roleid parameter in the frontend and then change the email, will that change the roleid as well? It's see
![[Pasted image 20250807074935.png]]
Yes, it does! Now if we login to `/admin` we can able to delete `carlos` user.
![[Pasted image 20250807075024.png]]
> Solution: Always check what other parameters you can change!

### 5. Lab: URL-based access control can be circumvented
> This website has an unauthenticated admin panel at `/admin`, but a front-end system has been configured to block external access to that path. However, the back-end application is built on a framework that supports the `X-Original-URL` header.
To solve the lab, access the admin panel and delete the user `carlos`.

We cannot be able to access `/admin`, but if we add `X-Original-Url` header, we can able to access the admin.
![[Pasted image 20250807125410.png]]
In order to delete carlos user, we have to use `?username=carlos` in query and `/admin/delete` in `X-Original-Url` header.
![[Pasted image 20250807130445.png]]
> Solution: Use `X-Original-Url` in order to bypass the restriction

### 6. Lab: Method-based access control can be circumvented 
> This lab implements access controls based partly on the HTTP method of requests. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.
To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed access controls to promote yourself to become an administrator.

After logging from admin account, we can see it is sending POST request to `/admin-roles` in order to change the access. Now we will login as wiener and send the same POST request with wiener's account and I am getting unauthorized.
![[Pasted image 20250807131617.png]]
On changing the request to GET I can able to bypass that restriction.
![[Pasted image 20250807131633.png]]
> Solution: Changing request from POST to GET can lead us to solution.

### 7. Lab: User ID controlled by request parameter
> This lab has a horizontal privilege escalation vulnerability on the user account page.
To solve the lab, obtain the API key for the user `carlos` and submit it as the solution.
You can log in to your own account using the following credentials: `wiener:peter`

After we login, if we change the username from wiener to carlos in URL, then we can able to access carlos API key.
![[Pasted image 20250807133547.png]]
> Solution: Change username in URL

### 8. Lab: User ID controlled by request parameter, with unpredictable user IDs 
> This lab has a horizontal privilege escalation vulnerability on the user account page, but identifies users with GUIDs.
To solve the lab, find the GUID for `carlos`, then submit his API key as the solution.
You can log in to your own account using the following credentials: `wiener:peter`

In this application, we have to enter the userId of carlos, which is GUID, so we can't predict it. But fortunately, we found the ID from the blog.
![[Pasted image 20250807133903.png]]
> Solution: Using that GUID in URL will give us the API Key of carlos

### 9. Lab: User ID controlled by request parameter with data leakage in redirect 
> This lab contains an access control vulnerability where sensitive information is leaked in the body of a redirect response.
To solve the lab, obtain the API key for the user `carlos` and submit it as the solution.
You can log in to your own account using the following credentials: `wiener:peter`

If we change the URL from wiener to carlos after login, it will redirect us to login, but if we see the request, we can observe that, before redirecting, the website renders carlos page.
![[Pasted image 20250807134200.png]]
> Solution: Rendering before redirecting

### 10. Lab: User ID controlled by request parameter with password disclosure 
> This lab has user account page that contains the current user's existing password, prefilled in a masked input.
To solve the lab, retrieve the administrator's password, then use it to delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

If we change the username from the URL to carlos, and check the source code, we will see that the password is already there in the form, entering that password will solve the lab.
![[Pasted image 20250807134852.png]]
> Solution: Check the source code!


### 11. Lab: Insecure direct object references 
> This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs.
Solve the lab by finding the password for the user `carlos`, and logging into their account.

On downloading the transcript, it gave us the data. On changing the file name to `1.txt` we got the transcript where there is a password for carlos.
![[Pasted image 20250807135204.png]]
> Solution: Change the value of parameter

### 12. Lab: Multi-step process with no access control on one step
> This lab has an admin panel with a flawed multi-step process for changing a user's role. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.
To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed access controls to promote yourself to become an administrator.

There were 2 steps in order to upgrade user from normal to admin. In the second request, there is an additional parameter called `confirmed=true`. So I have tried this request from weiner's session and it worked. So the website is thinking that in order to reach 2nd step, user must have been through first step. But if we directly send request to 2nd step, it will work and upgrade the user.
![[Pasted image 20250807150445.png]]
> Solution: Not all things are hardened in flow. Sometimes, a website will implement rigorous access controls over some of these steps, but ignore others.

### 13. Lab: Referer-based access control
> This lab controls access to certain admin functionality based on the Referer header. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.
To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed access controls to promote yourself to become an administrator.

Log in as admin, go to the admin panel, promote Carlos, and send that request to Burp Repeater. Then, in a private window, log in with a non-admin account and try accessing `/admin-roles?username=carlos&action=upgrade`—you’ll see it’s blocked because there’s no Referer header. Now, take the non-admin session cookie, paste it into the Burp Repeater request, change the username to yours, and resend it.
![[Pasted image 20250807151220.png]]
> Solution: Add Referer header

