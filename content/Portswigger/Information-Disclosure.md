### 1. Lab: Information disclosure in error messages
> This lab's verbose error messages reveal that it is using a vulnerable version of a third-party framework. To solve the lab, obtain and submit the version number of this framework.

When I tried to submit `'` instead of productId `1` at (`/product?productId='`). The website gave me error with Apache Strusts Version Number.
![[Pasted image 20250730121214.png]]
> Solution: `Apache Struts 2 2.3.31`

### 2. Lab: Information disclosure on debug page
> This lab contains a debug page that discloses sensitive information about the application. To solve the lab, obtain and submit the `SECRET_KEY` environment variable.

Always check the source code! In the source code, I found this route `/cgi-bin/phpinfo.php` and in that route it is exposing environment variables.
![[Pasted image 20250730121522.png]]
> Solution:  Check the source code: `5sgicqphazpo5jwo0ut08xzdx0xarmwy`

### 3. Lab: Source code disclosure via backup files
> This lab leaks its source code via backup files in a hidden directory. To solve the lab, identify and submit the database password, which is hard-coded in the leaked source code.

While I was browsing the website and checking the source codes, I didn't found anything, then `robots.txt` file strike up in my mind and in that file, it is exposing `/backup` directory, which contains a file (`ProductTemplate.java.bak`). File contains password for postgres database, submitting a password will solve the lab.
![[Pasted image 20250730122235.png]]
> Solution: `63cx26zjauj0z2swh6rhujp4as3w2w4d`

### 4. Lab: Authentication bypass via information disclosure
> This lab's administration interface has an authentication bypass vulnerability, but it is impractical to exploit without knowledge of a custom HTTP header used by the front-end.
To solve the lab, obtain the header name then use it to bypass the lab's authentication. Access the admin interface and delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

If we try to login and then try to access admin interface at `admin`, we will get `Admin interface only available to local users`. So, I have tried to use `TRACE` in `/login` to see what headers are passed in proxy.
![[Pasted image 20250730123224.png]]
We got this header: `X-Custom-IP-Authorization`
If it says admin interface only available to local users, we can infer that the IP must of of localhost, so adding that in Match and replace will add it for us.
![[Pasted image 20250730123338.png]]
Now, if we request `/admin` we can able to access it. Deleting carlos user will solve the lab.
> Solution: Use `TRACE` to find the hidden headers.

### 5. Lab: Information disclosure in version control history
> This lab discloses sensitive information via its version control history. To solve the lab, obtain the password for the `administrator` user then log in and delete the user `carlos`.

This application is exposing `/.git` directory, so we will use `git-dumper` or we can download files using `wget -r url` and then check logs in order to find sensitive data.
![[Pasted image 20250730123835.png]]
Use this password to login with administrator and delete carlos account in order to solve the lab.
> Solution: `pyaawa1jmb5297u8ansb`