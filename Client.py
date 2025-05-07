import socket

def main():
    host = '127.0.0.1'
    port = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(client_socket.recv(1024).decode('utf-8'))

        username = input("Inserisci il tuo username: ")
        client_socket.sendall(username.encode('utf-8'))

        while True:
            print(client_socket.recv(1024).decode('utf-8'))  # Strofa

            # Titolo
            print(client_socket.recv(1024).decode('utf-8'))
            client_socket.sendall(input().encode('utf-8'))

            # Artista
            print(client_socket.recv(1024).decode('utf-8'))
            client_socket.sendall(input().encode('utf-8'))

            # Anno
            print(client_socket.recv(1024).decode('utf-8'))
            client_socket.sendall(input().encode('utf-8'))

            # Featuring
            print(client_socket.recv(1024).decode('utf-8'))
            client_socket.sendall(input().encode('utf-8'))

            # Risultati
            print(client_socket.recv(4096).decode('utf-8'))

            # Continuare
            print(client_socket.recv(1024).decode('utf-8'))
            risposta = input()
            client_socket.sendall(risposta.encode('utf-8'))

            if risposta.lower() == 'no':
                print("Gioco terminato.")
                break

    except Exception as e:
        print(f"Errore: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
