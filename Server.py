import socket
import threading

def gestisci_client(connessione, indirizzo):
    print(f"Connessione stabilita con {indirizzo}")
    try:
        while True:
            dati = connessione.recv(1024)
            if not dati:
                break
        messaggio = dati.decode('utf-8')
        print(f"Ricevuto da {indirizzo}: {messaggio}")
        risposta = messaggio.upper()
        connessione.sendall(risposta.encode('utf-8'))
    except Exception as e:
        print(f"Errore nella comunicazione con {indirizzo}: {e}")
    finally:
        connessione.close()
        print(f"Connessione con {indirizzo} chiusa")

def avvia_server(indirizzo_server):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(indirizzo_server)
    socket_server.listen(5)
    print(f"Server in ascolto su {indirizzo_server}")
    try:
        while True:
            connessione, indirizzo_client = socket_server.accept()
            thread_client = threading.Thread(target=gestisci_client, args=(connessione, indirizzo_client))
            thread_client.start()
    except KeyboardInterrupt:
        print("\nServer interrotto dall'utente")
    finally:
        socket_server.close()

if __name__ == "__main__":
    indirizzo_server = ('10.0.46.2', 12345)
    avvia_server(indirizzo_server)
