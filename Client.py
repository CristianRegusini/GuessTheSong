import socket

def main():
    host = '10.0.46.2'  # IP del server a cui collegarsi
    port = 12345         # Porta del server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP/IP
    try:
        client_socket.connect((host, port))  # Connessione al server
        print(f"Connesso a {host}:{port}")

        while True:
            # Leggi un messaggio da inviare
            message = input("Inserisci il messaggio (digita 'exit' per uscire): ")
            client_socket.sendall(message.encode())  # Invia il messaggio al server

            if message.lower() == 'exit':  # Se l'utente scrive 'exit', esce dal ciclo
                print("Chiusura della connessione.")
                break

            # Riceve la risposta dal server
            response = client_socket.recv(1024)  # Riceve fino a 1024 byte
            print(f"Risposta del server: {response.decode()}")

    except Exception as e:
        print(f"Errore: {e}")  # In caso di errore, lo stampa

    finally:
        client_socket.close()  # Chiude il socket (connessione)

if __name__ == "__main__":
    main()
