### 1. Lab: Exploiting an API endpoint using documentation
> To solve the lab, find the exposed API documentation and delete `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.

When we update the email it requests `PATCH /api/user/wiener`, so the base endpoint must be `/api`.
![[Pasted image 20250816183025.png]]
Click on `DELETE` and toolkit will popup, an entering username carlos and sending request will solve the lab.
![[Pasted image 20250816183104.png]]
> Solution: Finding API endpoint using change email

### 2. Lab: Finding and exploiting an unused API endpoint
> To solve the lab, exploit a hidden API endpoint to buy a **Lightweight l33t Leather Jacket**. You can log in to your own account using the following credentials: `wiener:peter`.

After mapping the application, we can see there is `/api/products/1/price` endpoint, where `GET` and `PATCH` is allowed. But we have to change content type to `application/json`
![[Pasted image 20250816185205.png]]
Next, it says price parameter is missing from body, we will add price `0`.
![[Pasted image 20250816185325.png]]
The price for jacket is `0` now, add it to the cart and do checkout.
![[Pasted image 20250816185437.png]]
> Solution: check other methods to change data.

### 3. Lab: Exploiting a mass assignment vulnerability
> To solve the lab, find and exploit a mass assignment vulnerability to buy a **Lightweight l33t Leather Jacket**. You can log in to your own account using the following credentials: `wiener:peter`.

In this application there is `GET /api/checkout` where it giving JSON response with percentage discount, price and other details, what if we change the request to POST?
![[Pasted image 20250816195658.png]]
It worked, but we got error. In the backend, it is expected some JSON response.
![[Pasted image 20250816195711.png]]
Sending the data from GET request into POST body with `100` percentage discount, will place the order.
![[Pasted image 20250816195735.png]]
> Solution: Change GET to POST and change the body to update data.

### 4. Lab: Exploiting server-side parameter pollution in a query string
> To solve the lab, log in as the `administrator` and delete `carlos`.

If we check the source code of application, we will get this line where it is resetting the password using `reset_token` parameter. Let's try to add that and see what we are getting!
![[Pasted image 20250817091252.png]]
![[Pasted image 20250817091357.png]]
Invalid Token! Let's analyze POST request of forgot password
![[Pasted image 20250817091433.png]]
If we use `administratorx` then we will get invalid username. So we will use `administrator#foo=bar` (url encoded) and it says field is not specified.
![[Pasted image 20250817091522.png]]
We will use intruder to fuzz `foo` with server side parameter variable names with `administrator&FUZZ=bar`, we got username as field. But from the previous source code analysis we also got one more param that is `reset_token`, let's try that too (`administrator&field=reset_token`)!
![[Pasted image 20250817092041.png]]
Using that token, we can change password for administrator. Deleting carlos will solve the lab
![[Pasted image 20250817092109.png]]
> Solution: Exploit parameter pollution in the forgot-password request to leak the administrator’s reset token, set a new password, log in as admin, then delete carlos.


### 5. Lab: Exploiting server-side parameter pollution in a REST URL
> To solve the lab, log in as the `administrator` and delete `carlos`.

If we try to do similar thing from last lab, we will get invalid route.
![[Pasted image 20250817092656.png]]
So what I am guessing it, the application making a route based on username. Can we traverse though route using `carlos/../administrator`. It worked! Next I am trying to find the API documentation, and I got it at `carlos/../../../../../openapi.json%23`.
![[Pasted image 20250817104828.png]]
We can see there is an internal user endpoint, we can request password reset token from there. Payload: `carlos/../../../../../api/internal/v1/users/administrator/field/passwordResetToken%23`
![[Pasted image 20250817104846.png]]
> Solution: Walk the path traversal until you leak the API definition, pivot to the `users/{username}/field/{field}` endpoint, swap the field to passwordResetToken on the API, grab the admin's reset token, set a new password, log in as admin, and delete carlos. 