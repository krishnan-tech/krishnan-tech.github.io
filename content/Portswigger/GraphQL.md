### 1. Lab: Accessing private GraphQL posts
> The blog page for this lab contains a hidden blog post that has a secret password. To solve the lab, find the hidden blog post and enter the password.
Learn more about [Working with GraphQL in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/working-with-graphql).

If right click and open in graphql voyager, we can see we have other parameters which is `isPrivate` and `postPassword`.
![[Pasted image 20250901155338.png]]
If we change the ID to 3 we can able to see the password.
![[Pasted image 20250901155412.png]]
### 2. Lab: Accidental exposure of private GraphQL fields
> The user management functions for this lab are powered by a GraphQL endpoint. The lab contains an access control vulnerability whereby you can induce the API to reveal user credential fields.
To solve the lab, sign in as the administrator and delete the username `carlos`.
Learn more about [Working with GraphQL in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/working-with-graphql).

If we open Inql tab and open the query in graphql, on the left side, we can see there is `getUser` query and in that query at ID `1` we can able to get administrator password.
![[Pasted image 20250901160031.png]]
Login with these credentials, we can able to access admin panel and then delete carlos user.

### 3. Lab: Finding a hidden GraphQL endpoint
> The user management functions for this lab are powered by a hidden GraphQL endpoint. You won't be able to find this endpoint by simply clicking pages in the site. The endpoint also has some defenses against introspection.
To solve the lab, find the hidden endpoint and delete `carlos`.
Learn more about [Working with GraphQL in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/working-with-graphql).

In this application, the graphql endpoint is hidden so I have done a quick scan and found the endpoint at `/api` and the introspection query will not work, so we have to add `%0a` in schema in order to bypass that protection. (`__schema%0A`). Now we can able to get the graphql schema.
![[Pasted image 20250901161755.png]]
Next thing I have done is downloaded that schema and uploaded to INQL extension and then I got the queries and mutations.
![[Pasted image 20250901161810.png]]
![[Pasted image 20250901161834.png]]
From the query we got the ID of carlos which is `3` and from the mutation we can able to delete it. Use same mutation with URL encoding and pass it to `/api?query=<mutation>`.
### 4. Lab: Bypassing GraphQL brute force protections
> The user login mechanism for this lab is powered by a GraphQL API. The API endpoint has a rate limiter that returns an error if it receives too many requests from the same origin in a short space of time.
To solve the lab, brute force the login mechanism to sign in as `carlos`. Use the list of [authentication lab passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords) as your password source.
Learn more about [Working with GraphQL in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/working-with-graphql).

In this application we have to brute force carlos password, but rate limiting is there in the website, so we cannot send request separately. So we have to use batch query and then bruteforce the password.
![[Pasted image 20250901162432.png]]
```
mutation { 
	bruteforce0:login(input:{password: "123456", username: "carlos"}) { token success } 
	bruteforce1:login(input:{password: "password", username: "carlos"}) { token success } 
	... 
	bruteforce99:login(input:{password: "12345678", username: "carlos"}) { token success } }
```
Use the search bar below the response to search for the string `true`. This indicates which of the aliased mutations was able to successfully log in as `carlos`.