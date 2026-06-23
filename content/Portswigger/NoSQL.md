### 1. Lab: Detecting NoSQL injection
> The product category filter for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.
To solve the lab, perform a NoSQL injection attack that causes the application to display unreleased products.

If I use quote `'`, the application will give me this error, so that means quote is breaking the query. Simply using boolean query will solve the lab.
![[Pasted image 20250810161819.png]]
> Solution: `Gifts'||'1'=='1`

### 2. Lab: Exploiting NoSQL operator injection to bypass authentication
> The login functionality for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection using MongoDB operators.
To solve the lab, log into the application as the `administrator` user.
You can log in to your own account using the following credentials: `wiener:peter`.

The exact username is not `administrator`. Indeed it is starting with `admin*`. So we will use `$regex` for that and `$ne` for password.
![[Pasted image 20250810163129.png]]
> Solution: `{"username":{"$regex": "admin.*"},"password":{"$ne": ""}}`
### 3. Lab: Exploiting NoSQL injection to extract data
> The user lookup functionality for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.
To solve the lab, extract the password for the `administrator` user, then log in to their account.
You can log in to your own account using the following credentials: `wiener:peter`.

In this application, there is a user lookup functionality and we have to get administrator password. So we will look into `administrator`, but it didn't gave us the password.
![[Pasted image 20250810164240.png]]
So we will use the query to get the password: `administrator' && this.password[0] == 'a' || 'a'=='b`.
![[Pasted image 20250810164127.png]]
So we have to iterate each character and check if it is giving any response. If the character is right then we will get administrator data otherwise no user found. So we will use cluster bomb intruder to bruteforce it.
![[Pasted image 20250810164105.png]]
> Solution: `administrator' && this.password[0] == 'b' || 'a'=='b`

### 4. Lab: Exploiting NoSQL operator injection to extract unknown fields
> The user lookup functionality for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.
To solve the lab, log in as `carlos`.

If we try to login with user carlos and password not equal to empty, we see that our account is being locked.
![[Pasted image 20250810213147.png]]
If we use `$where` `0` , it says username or password is invalid whereas in `1` it says account is locked, that means we can inject Javascript.
Let's try to guess first field (which will be `_id` in every case, so let's just verify that). If we use `"$where":"Object.keys(this)[0].match('_id')"`, `_id` then it says account is locked, or else with other names it will say "invalid username or password". So we can confirm that the first field is `_id`. Let's test second and third field as username and password.
From index `4` we are getting internal server error. So there are total 4 fields (0-3). The `_id`, `username`, `password`, `<still_have_to_figure_it_out>`.
 > So in order to find the total number of columns use this query: `"$where":"Object.keys(this)[$0$].match('_id')"`

![[Pasted image 20250810213647.png]]
> In order to find the length of the field, we will use this query: `"$where":"Object.keys(this)[3].length == $1$"`

Sending this to intruder will give the length of the column name is `5`.
> Find hidden field name: `"$where":"Object.keys(this)[3].match('^abc$d$')"}`
 
![[Pasted image 20250810215129.png]]
In my case `[3]=email`. Now let's check the value length of email using `.length` query (`{"username":"carlos","password":{"$ne": ""},"$where":"this.email.length == 1"}`). The email length is `25`.

---
Or we can use this query in order to automate all the things, and highlight and sort the payload to get the hidden field.
`"$where":"Object.keys(this)[0].match('^.{0}a.*')"`
> **NOTE: IN ORDER TO ADD NEW FIELD WE HAVE TO SEND RESET PASSWORD TO CARLOS**

![[Pasted image 20250811200331.png]]
![[Pasted image 20250811200304.png]]Hidden field is: `newPwdTkn`. Next we will try to send this new field with `1` and we will see Invalid token in response. That means, we have to grab the token the same way as we got the hidden field.
![[Pasted image 20250811200617.png]]
In order to get the value of new hidden field, we will have to get the length of the value. We will use `.length` query to find it, and we got `16`.
![[Pasted image 20250811201323.png]]
Now, as we have the length, we will use `this.newPwdTkn.match` to get the value with 16 characters.
![[Pasted image 20250811201512.png]]
Alright, as we have token, we will use that to reset the password.
![[Pasted image 20250811201524.png]]
Now, reset the password and then login with carlos to solve the lab.
> Solution: check if we can extract fields using `"$where":"0"`