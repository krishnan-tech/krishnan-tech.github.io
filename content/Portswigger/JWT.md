### 1. Lab: JWT authentication bypass via unverified signature
> This lab uses a JWT-based mechanism for handling sessions. Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives.
To solve the lab, modify your session token to gain access to the admin panel at `/admin`, then delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

After login, check JWT token and change `sub` value to `administrator` from `wiener` and then replace the cookie and visit `/my-account?id=administrator` to access admin panel.
![[Pasted image 20250905171907.png]]
![[Pasted image 20250905171920.png]]Now, deleting carlos user will solve the lab.
### 2. Lab: JWT authentication bypass via flawed signature verification
> This lab uses a JWT-based mechanism for handling sessions. The server is insecurely configured to accept unsigned JWTs.
To solve the lab, modify your session token to gain access to the admin panel at `/admin`, then delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

Go to `/admin`, we will see that only `administrator` can able to access that page. If we go to JWT Web Token and click "none" signing algorithm, it will remove the last part of JWT (signature) and if we now check admin, we can able to see it!
![[Pasted image 20250905173025.png]]
### 3. Lab: JWT authentication bypass via jwk header injection
> This lab uses a JWT-based mechanism for handling sessions. The server supports the `jwk` parameter in the JWT header. This is sometimes used to embed the correct verification key directly in the token. However, it fails to check whether the provided key came from a trusted source.
To solve the lab, modify and sign a JWT that gives you access to the admin panel at `/admin`, then delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

To solve the lab, I first loaded the JWT Editor extension from the BApp store in Burp. After logging into my own account, I sent the post-login `GET /my-account` request to Burp Repeater and modified the path to `/admin`. This revealed that the admin panel was only accessible when logged in as the administrator. Next, I navigated to the JWT Editor Keys tab in Burp, generated a new RSA key pair, and saved it. Returning to the `GET /admin` request in Repeater, I switched to the JSON Web Token tab, modified the `sub` claim in the payload to `administrator`, and launched an embedded JWK attack using the generated RSA key. This added a `jwk` parameter containing my public key to the JWT header. Sending the modified request granted me access to the admin panel. Finally, in the response, I located the endpoint `/admin/delete?username=carlos` and sent the request to successfully delete Carlos and complete the lab.
![[Pasted image 20250907174448.png]]
### 4. Lab: JWT authentication bypass via jku header injection
> This lab uses a JWT-based mechanism for handling sessions. The server supports the `jku` parameter in the JWT header. However, it fails to check whether the provided URL belongs to a trusted domain before fetching the key.
To solve the lab, forge a JWT that gives you access to the admin panel at `/admin`, then delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

To solve the lab, I began by loading the JWT Editor extension from the BApp store in Burp. After logging into my own account, I sent the post-login `GET /my-account` request to Burp Repeater and modified the path to `/admin`, confirming that the admin panel was only accessible to the administrator. I then generated a new RSA key pair from the JWT Editor Keys tab and saved it. Moving to the exploit server in the browser, I replaced the body with an empty JWK Set and then copied the public key of my generated RSA key as JWK from Burp. I pasted this into the `keys` array on the exploit server and stored the exploit, resulting in a valid hosted JWK Set.
![[Pasted image 20250907185719.png]]

Next, I returned to the `GET /admin` request in Burp Repeater and opened the JSON Web Token tab. In the JWT header, I replaced the `kid` value with the one from my uploaded JWK and added a new `jku` parameter pointing to the URL of my hosted JWK Set. In the payload, I modified the `sub` claim to `administrator`. I then re-signed the token using my generated RSA key, making sure to keep the header unmodified. 
![[Pasted image 20250907185742.png]]
With the new valid signature, I sent the request and successfully gained access to the admin panel. Finally, I located the `/admin/delete?username=carlos` endpoint in the response and sent the request, which deleted Carlos and completed the lab.
### 5. Lab: JWT authentication bypass via kid header path traversal
> This lab uses a JWT-based mechanism for handling sessions. In order to verify the signature, the server uses the `kid` parameter in JWT header to fetch the relevant key from its filesystem.
To solve the lab, forge a JWT that gives you access to the admin panel at `/admin`, then delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

To solve the lab, I first loaded the JWT Editor extension from the BApp store in Burp. After logging into my own account, I sent the post-login `GET /my-account` request to Burp Repeater and modified the path to `/admin`, where I confirmed that the admin panel was restricted to the administrator user. I then went to the JWT Editor Keys tab, created a new symmetric key, and generated it in JWK format. To bypass the restriction on using an empty string, I replaced the generated `k` property with a Base64-encoded null byte (`AA==`) before saving the key.
![[Pasted image 20250907190313.png]]Next, I returned to the `GET /admin` request in Burp Repeater and switched to the JSON Web Token tab. In the header, I modified the `kid` parameter to a path traversal string pointing to `/dev/null` (`../../../../../../../dev/null`). In the payload, I changed the `sub` claim to `administrator`. At the bottom of the tab, I signed the token using the null-byte symmetric key I had created, making sure the “Don’t modify header” option was selected. This produced a valid signed token. Sending the request granted me access to the admin panel. Finally, I found the `/admin/delete?username=carlos` endpoint in the response and sent the request, which successfully deleted Carlos and solved the lab.
### 6. Lab: JWT authentication bypass via algorithm confusion
> This lab uses a JWT-based mechanism for handling sessions. It uses a robust RSA key pair to sign and verify tokens. However, due to implementation flaws, this mechanism is vulnerable to algorithm confusion attacks.
To solve the lab, first obtain the server's public key. This is exposed via a standard endpoint. Use this key to sign a modified session token that gives you access to the admin panel at `/admin`, then delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

To solve the lab, I began by loading the JWT Editor extension from the BApp store in Burp. After logging into my account, I sent the post-login `GET /my-account` request to Burp Repeater and modified the path to `/admin`, confirming that the admin panel could only be accessed by the administrator. I then navigated to the `/jwks.json` endpoint in the browser and found that the server exposed a JWK Set containing a single public key. I copied the JWK object from inside the `keys` array for use in the next step.
![[Pasted image 20250907191607.png]]
Next, in Burp’s JWT Editor Keys tab, I created a new RSA key using the JWK option and pasted the copied JWK into it before saving. I then right-clicked the key entry and selected **Copy Public Key as PEM**. Using the Decoder tab, I Base64-encoded the PEM key and copied the resulting string. After that, I created a new symmetric key in the JWT Editor Keys tab, replaced the generated `k` value with the Base64-encoded PEM string, and saved this new key.
![[Pasted image 20250907191559.png]]
Finally, I went back to the `GET /admin` request in Repeater and switched to the JSON Web Token tab. In the JWT header, I changed the `alg` parameter to `HS256`. In the payload, I modified the `sub` claim to `administrator`. I then re-signed the token using the symmetric key created earlier, ensuring the “Don’t modify header” option was selected. Sending this request successfully granted me access to the admin panel. From there, I found the `/admin/delete?username=carlos` endpoint in the response and sent the request, which deleted Carlos and solved the lab.