### Level 1
> This level is *buckets* of fun. See if you can find the first sub-domain.
Need a hint? Visit [Hint 1](http://flaws.cloud/hint1.html)

Let's try to check the domain using nslookup
`nslookup flaws.cloud`
![[Pasted image 20260615172130.png]]

Let's see what this IP is and where it is hosted.
`nslookup 52.92.179.131`
![[Pasted image 20260615172141.png]]
From nslookup, we can deduce that flaws.cloud is hosted on amazon aws platform.
As the level description suggests, this level is **buckets**. So let's try to list bucket
```bash
C:\Users\krish>aws s3 ls s3://flaws.cloud
2017-03-13 23:00:38       2575 hint1.html
2017-03-02 23:05:17       1707 hint2.html
2017-03-02 23:05:11       1101 hint3.html
2024-02-21 21:32:41       2861 index.html
2018-07-10 12:47:16      15979 logo.png
2017-02-26 20:59:28         46 robots.txt
2017-02-26 20:59:30       1051 secret-dd02c7c.html
```
![[Pasted image 20260615172153.png]]
There is a secret file called `secret-dd02c7c.html`. Let's download it and see what we have in that.
`aws s3 cp s3://flaws.cloud/secret-dd02c7c.html .`
![[Pasted image 20260615172209.png]]
`type secret-dd02c7c.html`
![[Pasted image 20260615172219.png]]
We found the URL for level 2, meaning this lab is solved!!

Solution at: http://flaws.cloud/secret-dd02c7c.html
![[Pasted image 20260615172718.png]]
Level2: http://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud/

### Lesson learned
On AWS you can set up S3 buckets with all sorts of permissions and functionality including using them to host static files. A number of people accidentally open them up with permissions that are too loose. Just like how you shouldn't allow directory listings of web servers, you shouldn't allow bucket listings.
#### Examples of this problem
- Directory listing of S3 bucket of Legal Robot ([link](https://hackerone.com/reports/163476)) and Shopify ([link](https://hackerone.com/reports/57505)).
- Read and write permissions to S3 bucket for Shopify again ([link](https://hackerone.com/reports/111643)) and Udemy ([link](https://hackerone.com/reports/131468)). This challenge did not have read and write permissions, as that would destroy the challenge for other players, but it is a common problem.
### Avoiding the mistake
By default, S3 buckets are private and secure when they are created. To allow it to be accessed as a web page, I had turn on "Static Website Hosting" and changed the bucket policy to allow everyone "s3:GetObject" privileges, which is fine if you plan to publicly host the bucket as a web page. But then to introduce the flaw, I changed the permissions to add "Everyone" to have "List" permissions.![](http://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud/everyone.png)"Everyone" means everyone on the Internet. You can also list the files simply by going to [http://flaws.cloud.s3.amazonaws.com/](http://flaws.cloud.s3.amazonaws.com/) due to that List permission.