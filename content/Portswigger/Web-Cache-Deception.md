### 1. Lab: Exploiting path mapping for web cache deception
> To solve the lab, find the API key for the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.

Here's how Web Cache Deception Works
1. When we login into our account (`wiener`), the application will not add any cache header. ![[Pasted image 20250817120723.png]]
2. We we add `/test` into the route, then too, it will not add cache header ![[Pasted image 20250817120800.png]]
3. Now, let's try to add `/test.js`, we can see cache in response header, meaning, it is caching `test.js` with the `max-age` of `30`. In simple words it will store the response on cache server for 30 seconds. ![[Pasted image 20250817120840.png]]
4. If we try to send the cache link to the victim, it will load the response with victim's data with a cache miss, and when we visit that cached URL it will hit the case (meaning, it will give us the cached victim data). Now sending the URL to victim. ![[Pasted image 20250817121034.png]]
5. Now if we reload the cached URL on our browser, we will see carlos's API Key ![[Pasted image 20250817121200.png]]
> Solution: Simple Web cache deception with `/my-account` page.

### 2. Lab: Exploiting path delimiters for web cache deception
> To solve the lab, find the API key for the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.
We have provided a list of possible delimiter characters to help you solve the lab: [Web cache deception lab delimiter list](https://portswigger.net/web-security/web-cache-deception/wcd-lab-delimiter-list).

Similar to previous lab, but in this lab, if we add `/test` the application will say "not found". So we have to use delimiter. We can use Intruder to find it. (Make sure to turn off URL encoding).
![[Pasted image 20250817124905.png]]
We found 2 delimiters. `?` and `;`
![[Pasted image 20250817124940.png]]
Next, we will use `;test.js` to check if the response is getting cached. In this case, yes, it's cached!
![[Pasted image 20250817125022.png]]
Now we will send the link to carlos and use caching to get the API key.
> Solution: Find the delimiter to end the URL

### 3. Lab:  Exploiting origin server normalization for web cache deception
> To solve the lab, find the API key for the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.
We have provided a list of possible delimiter characters to help you solve the lab: [Web cache deception lab delimiter list](https://portswigger.net/web-security/web-cache-deception/wcd-lab-delimiter-list).

![[Pasted image 20250818193925.png]]
Now as we found the response with Cache header, we will move forward with delimiter. I tested path delimiters and found that only `?` worked. Then I checked normalization by adding encoded dot-segments like `..%2f`, and the server resolved them while the cache didn’t. The `/resources` prefix turned out to have a static directory cache rule, so I combined that with the dot-segment trick to serve sensitive content from cache. Finally, I built an exploit that redirected the victim to a crafted URL, which cached their API key. After that, I just grabbed the key and submitted it to finish the lab.
Payload: `<script>document.location="https://0a9e002a048706f980de173800b50059.web-security-academy.net/resources/..%2fmy-account?test"</script>`
> Solution: Exploited path and cache handling quirks with `..%2f` to trick the cache and steal the victim’s API key.

