import socket
import sys
import threading

otheruser = ""

def newcreatesession(newsock, username):
    print("[+] Creating a new session")
    try:
        newsock.bind((socket.gethostbyname(socket.gethostname()), 12345))
        newsock.listen(1)
        
        print("[+] Waiting for an external host to join on port 12345...")
        client_socket, client_address = newsock.accept()
        print(f"[+] Connected Client: {client_address} -> {username.encode()}\n")

        threading.Thread(target=listener, args=(client_socket,)).start()
        threading.Thread(target=sender, args=(client_socket,)).start()

    except socket.error as e:
        print(f"[X] Socket error: {e}")

def joinnewsession(newsock, username, target):
    print(f"[+] Joining {target}")
    try:
        newsock.connect((target, 12345))
        print(f"[+] Success! Joined {target}")
        threading.Thread(target=listener, args=(newsock,)).start()
        threading.Thread(target=sender, args=(newsock,)).start()

    except socket.error as e:
        print(f"[X] Socket error: {e}")

def listener(sock):
    global otheruser  # Use the global variable
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"{message}")
        except socket.error as e:
            print(f"[X] Socket error: {e}")
            break

def sender(sock):
    while True:
        try:
            message = input(f"{username.title()}>> ")
            if message.upper() == "EXIT":
                sys.exit(1)
            sock.send(f"{username.title()}>> {message}".encode())
        except socket.error as e:
            print(f"[X] Error: {e}")
            break

if __name__ == "__main__":
    print("\n------------------\nSTARTING NOPEAK.........\n")
    print(""" _______        __________               __    
 \      \   ____\______   \ ____ _____  |  | __
 /   |   \ /  _ \|     ___// __ \\__  \ |  |/ /
/    |    (  <_> )    |   \  ___/ / __ \|    < 
\____|__  /\____/|____|    \___  >____  /__|_ \\
        \/                     \/     \/     \/""")

    try:
        newsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

    choice = int(input("""\nInput one of the following options\n[1] Create a new session\n[2] Join a new session\n"""))
    username = input("[-] Enter your username: ")
    
    if choice == 1:
        newcreatesession(newsock, username)
    else:
        target = input("[-] Enter the target IP address: ")
        joinnewsession(newsock, username, target)
