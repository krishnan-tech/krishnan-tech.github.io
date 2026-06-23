### 1. Lab: File path traversal, simple case
> This lab contains a path traversal vulnerability in the display of product images.
To solve the lab, retrieve the contents of the `/etc/passwd` file.

As we can see it in the burpsuite response, images are getting retrieved using `/image?filename=26.jpg`, so instead of `26.jpg` we will use `../../../etc/passwd` to solve the lab.
![[Pasted image 20250729182719.png]]
> Solution: `../../../etc/passwd`
### 2. Lab: File path traversal, traversal sequences blocked with absolute path bypass
> This lab contains a path traversal vulnerability in the display of product images.
The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory.
To solve the lab, retrieve the contents of the `/etc/passwd` file.

Similar to previous lab, the only difference is we have to use absolute path from root.
> Solution: `/etc/passwd`
### 3 Lab: File path traversal, traversal sequences stripped non-recursively
> This lab contains a path traversal vulnerability in the display of product images.
The application strips path traversal sequences from the user-supplied filename before using it.
To solve the lab, retrieve the contents of the /etc/passwd file.

Sometimes `../` is getting stripped, so we have to use `....//` so the inner value will be stripped and we will get the results we want.
> Solution: `....//....//....//etc/passwd`
### 4. Lab: File path traversal, traversal sequences stripped with superfluous URL-decode
> This lab contains a path traversal vulnerability in the display of product images.
The application blocks input containing path traversal sequences. It then performs a URL-decode of the input before using it.
To solve the lab, retrieve the contents of the `/etc/passwd` file.

This lab can be solved by double URL encoding.
`../../../etc/passwd` -> `%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64` -> `%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%36%35%25%37%34%25%36%33%25%32%66%25%37%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%34`
![[Pasted image 20250729183709.png]]
> Solution: Double URL encoding payload
### 5. Lab:  Lab: File path traversal, validation of start of path
> This lab contains a path traversal vulnerability in the display of product images.
The application transmits the full file path via a request parameter, and validates that the supplied path starts with the expected folder.
To solve the lab, retrieve the contents of the `/etc/passwd` file.

As the description says, it should start from a particular folder, so we will add our payload after images folder.
> Solution: `filename=/var/www/images/../../../etc/passwd`

### 6. Lab: File path traversal, validation of file extension with null byte bypass
> This lab contains a path traversal vulnerability in the display of product images.
The application validates that the supplied filename ends with the expected file extension.
To solve the lab, retrieve the contents of the `/etc/passwd` file.

The application checks for the extension, so we will use null byte `%00` to comment out the characters following the null byte.
> Solution: `../../../etc/passwd%00.png`