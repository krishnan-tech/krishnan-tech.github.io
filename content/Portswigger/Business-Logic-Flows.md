### 1. Lab: Excessive trust in client-side controls
> This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".
You can log in to your own account using the following credentials: `wiener:peter`

In this application, when we add items to cart, it is also sending the price as a parameter and consider that as the actual price instead of original price. So we will change the price from burpsuite and place an order.
![[Pasted image 20250731111424.png]]
> Solution: Change the price parameter

### 2. Lab: 2FA broken logic
> This lab's two-factor authentication is vulnerable due to its flawed logic. To solve the lab, access Carlos's account page.
 Your credentials: `wiener:peter`
 Victim's username: `carlos`
You also have access to the email server to receive your 2FA verification code.

Login with `wiener:peter`, then on `/login2` we have to bruteforce the password and change the verify cookie to carlos. Once we will get the code, we can able to enter it.
![[Pasted image 20250731112815.png]]
In `GET /login2` we will make sure the code will be sent to carlos by changing the cookie. Then we will send the `POST /login2` to intruder in order to bruteforce the code.
![[Pasted image 20250731112907.png]]
Again, by sending the code, we will make sure the cookie is set to carlos instead of wiener and boom, we will solve the lab.
> Solution: Cookie handling flow.

### 3. Lab: High-level logic vulnerability
> This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".
You can log in to your own account using the following credentials: `wiener:peter`

In this application, we can add quantity to -1.
![[Pasted image 20250731114010.png]]
But it says, total price cannot be less than zero, so we will add other items and make price between 0-100.
![[Pasted image 20250731114424.png]]
We will add jacket and adjust price with negative other items.
> Solution: Accepting negative value in quantity.

### 4. Lab: Low-level logic flaw
> This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".
You can log in to your own account using the following credentials: `wiener:peter`

Notetaking thing from this lab is, when the total is very large, it will turn into negative value and then we just have to normalize the total below 100.
![[Pasted image 20250731145853.png]]
> Solution: Pass a very large number to get negative total

### 5. Lab: Inconsistent handling of exceptional input
> This lab doesn't adequately validate user input. You can exploit a logic flaw in its account registration process to gain access to administrative functionality. To solve the lab, access the admin panel and delete the user `carlos`.

In this application, we we try to enter a very large email, it truncates last characters, and only allowing certain characters. For example, if we try to register with 200 A with exploit server email, we will see this behaviour.
![[Pasted image 20250731151619.png]]
So, it only took 255 characters. On top of that, there is an admin route which is only allowed for DontWannaCry user, so we have to use that email.
![[Pasted image 20250731151726.png]]
What we will do is, we will add `AAAA...@dontwannacry.com.<exploitserveremail>`. So after calculating characters we will use 238 A's .
![[Pasted image 20250731152130.png]]
Now, we have dontwannacry email, going to admin panel and deleting carlos account will solve the lab.
> Solution: Sometimes characters are truncated from backend which leads to unexpected behaviours.

### 6. Lab: Inconsistent security controls
> This lab's flawed logic allows arbitrary users to access administrative functionality that should only be available to company employees. To solve the lab, access the admin panel and delete the user `carlos`.

In this application, register using attacker's email and verify the user, and once we go to my account, we can see change email functionality, if we use dontwannacry email to change it, it doesn't require verification and we can able to access admin portal. Deleting carlos account will solve the lab.
![[Pasted image 20250731153111.png]]
> Solution: change email to access admin portal

### 7. Lab: Weak isolation on dual-use endpoint
> This lab makes a flawed assumption about the user's privilege level based on their input. As a result, you can exploit the logic of its account management features to gain access to arbitrary users' accounts. To solve the lab, access the `administrator` account and delete the user `carlos`.
> You can log in to your own account using the following credentials: `wiener:peter`

If we remove `current-password` parameter, we can simply be able to change the password, also, there is username parameter, let's try to change the username to administrator and check if we can able to change it. 
![[Pasted image 20250731153920.png]]
The new password for administrator account is test. Login with that account and deleting carlos account will solve the lab.
> Solution: Sometimes removing parameters will give unexpected results!
### 8. Lab: Insufficient workflow validation
> This lab makes flawed assumptions about the sequence of events in the purchasing workflow. To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".
You can log in to your own account using the following credentials: `wiener:peter`

After every successful order, we will see the order confirmation page
![[Pasted image 20250806120443.png]]
What if we add jacket to the cart and then send this request. Will it confirm the order? Yes, it will. This is how we can solve the lab.
> Solution: Without placing the order, we will send order confirmation request.

### 9. Lab: Infinite money logic flaw 
> This lab has a logic flaw in its purchasing workflow. To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".
You can log in to your own account using the following credentials: `wiener:peter`

When we signup to the newsletter, we will see this popup that says - use this coupon SIGNUP30 at checkout.
![[Pasted image 20250806121001.png]]
Now if we buy giftcard of $10, and use this coupon, it will turn into $7 and then when we redeem the giftcard it will get $10, so our total money will be increased by $3. We will repeat this process using Macros in order to solve this lab.
To automate the whole flow, open Burp and go to the Settings tab. Under Sessions, create a new session handling rule. Set the scope to include all URLs, then under Rule Actions, choose to run a macro. You’ll need to record the following sequence of requests: `POST /cart`, `POST /cart/coupon`, `POST /cart/checkout`, `GET /cart/order-confirmation?order-confirmed=true`, and `POST /gift-card`.
![[Pasted image 20250806123803.png]]
Once recorded, edit the macro. In the `GET /cart/order-confirmation` response, extract the gift card code from the bottom of the response body. Name the parameter `gift-card`. Then go to the `POST /gift-card` request and set its `gift-card` parameter to use the value from the confirmation response. Test the macro and make sure it actually redeems the generated code by checking for a 302 response on the last step.

Now switch to Burp Intruder. Send the `GET /my-account` request to Intruder and use Sniper attack type. For payloads, choose Null payloads and generate 412 of them. Open the Resource Pool settings and set the concurrency to 1—this keeps things stable while Burp handles session cookies and timing. Start the attack and let it run.

Once the attack finishes, you’ll have enough credit to buy the jacket and solve the lab. The whole point here is exploiting a broken money logic with a simple coupon and turning it into an automated profit loop.
> Solution: Using giftcard and coupon will compromise the actual price

### 10. Lab: Authentication bypass via encryption oracle
> This lab contains a logic flaw that exposes an encryption oracle to users. To solve the lab, exploit this flaw to gain access to the admin panel and delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

description