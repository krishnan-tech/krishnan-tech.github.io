### 1. Lab: Remote code execution via web shell upload
> This lab contains a vulnerable image upload function. It doesn't perform any validation on the files users upload before storing them on the server's filesystem.
To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: `wiener:peter`

When we login into the application, we have upload file option and the image will be viewed at `/files/avatars/L.jpg`. In order to read the secret file, we will use `<?php echo file_get_contents('/home/carlos/secret'); ?>` payload.
Or we could have used `<?php echo system($_GET['command']); ?>`
![[Pasted image 20250818202413.png]]
> Solution: Using `file_get_contents` we can able to read the file

### 2. Lab: Web shell upload via Content-Type restriction bypass
> This lab contains a vulnerable image upload function. It attempts to prevent users from uploading unexpected file types, but relies on checking user-controllable input to verify this.
To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: `wiener:peter`

Same previous solution worked here too! The only thing to take care is mime type. If mime type is image but name is `.php` and the content is `shell` then it will execute!
![[Pasted image 20250818203037.png]]
> Solution: Mime type bypass with name and content

### 3. Lab: Web shell upload via path traversal
> This lab contains a vulnerable image upload function. The server is configured to prevent execution of user-supplied files, but this restriction can be bypassed by exploiting a [secondary vulnerability](https://portswigger.net/web-security/file-path-traversal).
To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: `wiener:peter`

Firstly we will try to upload the shell using simple file upload technique, but for some reason, we are getting content of the file instead of executing that php content. `/files/avatars/L.php`
![[Pasted image 20250818204307.png]]
What we will do is, instead of uploading to `files` directory instead of `avatars` by directory traversal `filename="..%2fL.php"` -> `/files/L.php` (without url encoding `/`, it will not work)
![[Pasted image 20250818204325.png]]
And yes, we got the secret value.
> Solution: Using LFI, we can upload images to different location

### 4. Lab: Web shell upload via extension blacklist bypass
> This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed due to a fundamental flaw in the configuration of this blacklist.
To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: `wiener:peter`

In this application, I have tried to upload shell with different file extensions, but nothing seems to be working. As the server is apache, we will try to upload `.htaccess` and change the configuration of php executables. 
With this line, `AddType application/x-httpd-php .test`, we can configure another php extension to `.test`, so if we upload the shell as `L.test`, it will execute php code. Set content type to `plain/text`, filename to `.htaccess`
![[Pasted image 20250819063425.png]]
Next, we will upload the shell using name `L.test` and view it in browser.
![[Pasted image 20250819063605.png]]
> Solution: Always check if we can able to rewrite configuration files.
### 5. Lab: Web shell upload via obfuscated file extension
> This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed using a classic obfuscation technique.
To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: `wiener:peter`

Using NULL Byte we can able to bypass the restriction.
`L.php%00.jpg` -> `avatars/L.php`.
More techniques here: https://portswigger.net/web-security/file-upload#obfuscating-file-extensions
![[Pasted image 20250819064548.png]]
> Solution: Using NULL Byte we can bypass restriction.

### 6. Lab: Remote code execution via polyglot web shell upload
> This lab contains a vulnerable image upload function. Although it checks the contents of the file to verify that it is a genuine image, it is still possible to upload and execute server-side code.
To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: `wiener:peter`

We can solve this lab using magic bytes. For example, JPEG files always begin with the bytes `FF D8 FF`. But instead of that mess, we can simply use `GIF8` to bypass that (which acts similar way)
![[Pasted image 20250819065152.png]]
> Solution: Use magic bytes

### 7. Lab: Web shell upload via race condition
> This lab contains a vulnerable image upload function. Although it performs robust validation on any files that are uploaded, it is possible to bypass this validation entirely by exploiting a race condition in the way it processes them.
To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: `wiener:peter`

In this application, only jpg and png images are allowed, but for fraction of second it stores the image temporarily on file system and then do validation. If there is validation failure then it will delete the file, so for a small interval the file is in the system, so we can send parallel connection that uploads the shell and executes it.
![[Pasted image 20250819205455.png]]
![[Pasted image 20250819205504.png]]
> Solution: With race condition, we can able to get the secret.