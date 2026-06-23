### Level 2
> The next level is fairly similar, with a slight twist. You're going to need your own AWS account for this. You just need the [free tier](https://aws.amazon.com/s/dm/optimization/server-side-test/free-tier/free_np/).
For hints, see [Hint 1](http://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud/hint1.html)

For this level, we have to configure our profile with `aws configure` and pass it our AWS access token in command line and then pass that in `--profile` flag.

If you already configured aws cli, and want to use default profile itself, then you dont have to pass `--profile` flag. It will work nevertheless.
```bash
C:\Users\krish>aws configure list-profiles
default

C:\Users\krish>aws s3 ls s3://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud --profile default
2017-02-26 21:02:15      80751 everyone.png
2017-03-02 22:47:17       1433 hint1.html
2017-02-26 21:04:39       1035 hint2.html
2017-02-26 21:02:14       2786 index.html
2017-02-26 21:02:14         26 robots.txt
2017-02-26 21:02:15       1051 secret-e4443fc.html
```
![[Pasted image 20260615174451.png]]
Either download that secret file or open that URL in browser.
URL: http://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud/secret-e4443fc.html
Level 3: http://level3-9afd3927f195e10225021a578e6f78df.flaws.cloud/

### Lesson learned
Similar to opening permissions to "Everyone", people accidentally open permissions to "Any Authenticated AWS User". They might mistakenly think this will only be users of their account, when in fact it means anyone that has an AWS account.
#### Examples of this problem
- Open permissions for authenticated AWS user on Shopify ([link](https://hackerone.com/reports/98819))
### Avoiding the mistake
Only open permissions to specific AWS users.![](http://level3-9afd3927f195e10225021a578e6f78df.flaws.cloud/authenticated_users.png)This screenshot is from the webconsole in 2017. This setting can no longer be set in the webconsole, but the SDK and third-party tools sometimes allow it.