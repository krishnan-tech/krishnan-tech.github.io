### 1. Lab: Limit overrun race conditions
> This lab's purchasing flow contains a race condition that enables you to purchase items for an unintended price.
To solve the lab, successfully purchase a **Lightweight L33t Leather Jacket**.
You can log in to your account with the following credentials: `wiener:peter`.

In this application, we can use PROMO20 coupon in order to get discount, but there is a race condition in the functionality, so we will add 20 tabs, group them and send request parallelly. 
![[Pasted image 20250807151722.png]]
After we send the request, the the total will be below $50. So we can able to buy it.
![[Pasted image 20250807151733.png]]
> Solution: Send multiple request with coupon in order to check for race conditions.

### 2. Lab: Bypassing rate limits via race conditions
> This lab's login mechanism uses rate limiting to defend against brute-force attacks. However, this can be bypassed due to a race condition.
To solve the lab:
1. Work out how to exploit the race condition to bypass the rate limit.
2. Successfully brute-force the password for the user `carlos`.
3. Log in and access the admin panel.
4. Delete the user `carlos`.
You can log in to your account with the following credentials: `wiener:peter`.

In this application, we have rate limit on login functionality, so we will use Turbo Intruder in order to send multiple request parallelly.
![[Pasted image 20250810112604.png]]
```python
def queueRequests(target, wordlists):

    # as the target supports HTTP/2, use engine=Engine.BURP2 and concurrentConnections=1 for a single-packet attack
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )
    
    # assign the list of candidate passwords from your clipboard
    passwords = wordlists.clipboard
    
    # queue a login request using each password from the wordlist
    # the 'gate' argument withholds the final part of each request until engine.openGate() is invoked
    for password in passwords:
        engine.queue(target.req, password, gate='1')
    
    # once every request has been queued
    # invoke engine.openGate() to send all requests in the given gate simultaneously
    engine.openGate('1')


def handleResponse(req, interesting):
    table.add(req)
```
As we can see from the code, we are getting passwords from clipboard and for each password we are queueing requests and then sending it parallelly. If we get Status code 302, then we got the password for carlos, or else we have to remove the incorrect password and then send the other passwords. 
![[Pasted image 20250810110301.png]]
Eventually we will get 302 on one of the password, we will enter that password and login as carlos.
![[Pasted image 20250810112552.png]]
Going to admin panel and deleting the user carlos will solve the lab.
> Solution: Use turbo intruder when we have to send custom requests.

### 3. Lab: Multi-endpoint race conditions
> This lab's purchasing flow contains a race condition that enables you to purchase items for an unintended price.
To solve the lab, successfully purchase a **Lightweight L33t Leather Jacket**.
You can log into your account with the following credentials: `wiener:peter`.

I have tested race on redeem giftcard, but there is no race condition on that endpoint. If we do the add giftcard and place the order, and in just a fraction of second between checkout if we add the jacket we can able to purchase the jacket.
![[Pasted image 20250810123939.png]]
So what I will do is, buy a giftcard and then send jacket and checkout request parallelly. 
![[Pasted image 20250810123749.png]]
> Solution: Race condition in cart while placing the order

### 4. Lab: Single-endpoint race conditions
> This lab's email change feature contains a race condition that enables you to associate an arbitrary email address with your account.
Someone with the address `carlos@ginandjuice.shop` has a pending invite to be an administrator for the site, but they have not yet created an account. Therefore, any user who successfully claims this address will automatically inherit admin privileges.
To solve the lab:
1. Identify a race condition that lets you claim an arbitrary email address.
2. Change your email address to `carlos@ginandjuice.shop`.
3. Access the admin panel.
4. Delete the user `carlos`
> You can log in to your own account with the following credentials: `wiener:peter`.
You also have access to an email client, where you can view all emails sent to `@exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net` addresses.

When we try to update the account, it says,
![[Pasted image 20250810125129.png]]In order to change it, this is the URL we got in email: `/confirm-email?user=wiener&token=EuBHjPRiAXqBNpFk` with user and token parameter.
If we use `carlos@ginandjuice.shop` then it will send conformation email to carlos. 
![[Pasted image 20250810125952.png]]
So we can do something like this, parallelly send two update email, and check what is reflected in the page, if we see change email to carlos then we will look at email client and use the link to change our email to carlos.
![[Pasted image 20250810125855.png]]
So we will click on that link, that will change our email to carlos and we will have access to admin panel. Now deleting carlos user will solve the lab.
> Solution: When the user is associated with token, we can able to swap user and token using race condition.

### 5. Lab: Partial construction race conditions 
> This lab contains a user registration mechanism. A race condition enables you to bypass email verification and register with an arbitrary email address that you do not own.
To solve the lab, exploit this race condition to create an account, then log in and delete the user `carlos`.

The registration system only accepts `@ginandjuice.shop` emails, and confirmation links are sent there, making it impossible to register without such an account. Reviewing Burp proxy traffic reveals a users.js file that builds the confirmation form and shows the final confirmation request is a POST to /confirm with a token in the query string. By replicating this request in Burp Repeater, you see different responses depending on the token’s value: arbitrary tokens return `Incorrect`, missing tokens return `Missing parameter`, and empty tokens return `Forbidden`, hinting at a patched vulnerability. The behavior suggests a potential race condition where a null token might be valid before it’s stored in the database. Testing with token parameters set to values equivalent to null—like an empty array (`token[]=`) returns `Invalid token: Array`, confirming the input bypassed the empty token block and could align with an uninitialized token state.
```python
def queueRequests(target, wordlists):

    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=1,
                            engine=Engine.BURP2
                            )
    
    confirmationReq = '''POST /confirm?token[]= HTTP/2
Host: 0ab10056035e12bd80d1dfc700850078.web-security-academy.net
Cookie: phpsessionid=YOUR-SESSION-TOKEN
Content-Length: 0

'''
    for attempt in range(20):
        currentAttempt = str(attempt)
        username = 'User' + currentAttempt
    
        # queue a single registration request
        engine.queue(target.req, username, gate=currentAttempt)
        
        # queue 50 confirmation requests - note that this will probably sent in two separate packets
        for i in range(50):
            engine.queue(confirmationReq, gate=currentAttempt)
        
        # send all the queued requests for this attempt
        engine.openGate(currentAttempt)

def handleResponse(req, interesting):
    table.add(req)
```

![[Pasted image 20250810131551.png]]

### 6. Lab: Exploiting time-sensitive vulnerabilities
> This lab contains a password reset mechanism. Although it doesn't contain a race condition, you can exploit the mechanism's broken cryptography by sending carefully timed requests.
To solve the lab:
1. Identify the vulnerability in the way the website generates password reset tokens.
2. Obtain a valid password reset token for the user `carlos`.
3. Log in as `carlos`.
4. Access the admin panel and delete the user `carlos`.
> You can log into your account with the following credentials: `wiener:peter`.

In this application, the reset password functionality is sending token using timestamp, so if we send both of the request at same time, it will give same token. But in order to send it parallelly, we have to use different phpsession and csrf tokens (as the server is processing it consecutively), we will get new phpsession and csrf from `GET /forgot-password`  endpoint. After we have established parallel requests in wiener, we will change on user to carlos.
![[Pasted image 20250810133600.png]]
Then changing the `POST /forgot-password` to the data we got from wiener will reset the password for carlos.
![[Pasted image 20250810133835.png]]
Login with carlos and deleting the account will solve the lab.
> Solution: Reset password race condition with timestamp as token