## Write Up for Erit Securus I

#### Task 1
Just connect to your VPN and deploy the machine

#### Reconnaissance

So you can use any scanning tool you like but I prefer to use Nmap and I will just do a normal aggressive scan by using the flags -A -p-
```
nmap -T4 -A -p- $IP
```
and then the results I got are these :
```
Nmap scan report for 10.10.102.12
Host is up (0.048s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
| ssh-hostkey:
|   1024 b1:ac:a9:92:d3:2a:69:91:68:b4:6a:ac:45:43:fb:ed (DSA)
|   2048 3a:3f:9f:59:29:c8:20:d7:3a:c5:04:aa:82:36:68:3f (RSA)
|   256 f9:2f:bb:e3:ab:95:ee:9e:78:7c:91:18:7d:95:84:ab (ECDSA)
|_  256 49:0e:6f:cb:ec:6c:a5:97:67:cc:3c:31:ad:94:a4:54 (ED25519)
80/tcp open  http    nginx 1.6.2
|_http-generator: Bolt
|_http-server-header: nginx/1.6.2
|_http-title: Graece donan, Latine voluptatem vocant. | Erit Securus 1
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).

```
So here we can see that there are two ports open one for SSH and the other one is for the web server. And they are on 22 and 80 respectively .

Ans1) 2
Ans2) 22,80


#### Web server
 This one is pretty easy to find just look at the nmap report and there it shows the http-generator for us was Bolt and that's the CMS used .

Ans) Bolt

#### Exploit

So now we have to look and find for an exploit luckily for us they have already provided one for us which is the link on the exploit text and it will lead us to this GitHub page.
https://github.com/r3m0t3nu11/Boltcms-Auth-rce-py
And now this is our exploit so lets read a little more about it first and see what its all about. So here we can see this exploit takes in 3 arguments and is written in Python and what it does after taking those inputs is try to get a CSRF token for us and do session injection and give us back a shell.

So lets git clone this first to our folder and then leave it until we find the credentials and also try directory busting now to find the log in page which we can try brute force or spray default credentials into and for that my go to tool is dirbuster which is gui tool that you can open by just typing dirbuster into your terminal but i like to open it with & and it end because then its multithreaded and its faster so lets start:
```
dirbuster&
```
So here in the GUI we first have to put the IP of the machine in the way its written above with the port and everything and then i like to click on the go faster button so the process is faster and then we have to pass a wordlist to it which we can find by default in Kali at /usr/share/wordlist/ and in here i like to use the dirbuster small one you can also use one small one which is in the durb folder called common.txt and then we specify the file extensions we wanna brute force in those directories don't put to many though cause the more they are the more time the dirbuster is gonna take.
