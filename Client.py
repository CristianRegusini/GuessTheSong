import socket

def main():
    host = '127.0.0.1'  # IP del server a cui collegarsi
    port = 65432         # Porta del server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP/IP
    try:
        client_socket.connect((host, port))  # Connessione al server
        print(f"Connesso a {host}:{port}")



        while True:

            # Riceve la strofa dal server
            strofa = client_socket.recv(1024).decode('utf-8')
            print(strofa)

            # Risposta titolo
            title_question = client_socket.recv(1024).decode('utf-8')
            print(title_question)
            #title = input("inserisci il titolo")
            title = input()

            #invia la risposta
            client_socket.sendall(title.encode('utf-8'))

            # Riceve la richiesta per l'artista
            artist_question = client_socket.recv(1024).decode('utf-8')
            print(artist_question)
            #artista = input("Inserire nome dell'artista: ")
            artista = input()

            # Invia la risposta dell'artista
            client_socket.sendall(artista.encode('utf-8'))

            # Riceve la richiesta per l'anno
            year_question = client_socket.recv(1024).decode('utf-8')
            print(year_question)
            #anno = input("Inserire anno : ")
            anno = input()

            # Invia la risposta dell'anno
            client_socket.sendall(anno.encode('utf-8'))

            # Riceve la richiesta per il featuring
            featuring_question = client_socket.recv(1024).decode('utf-8')
            print(featuring_question)
            featuring = input()

            # Invia la risposta del featuring
            client_socket.sendall(featuring.encode('utf-8'))

            # Riceve i risultati dal server
            results = client_socket.recv(1024).decode('utf-8')
            print(results)

            # Chiede se il giocatore vuole continuare
            continue_game = client_socket.recv(1024).decode('utf-8')
            print(continue_game)
            risposta = input("vuoi continuare? si/no")
            # Invia la risposta per continuare
            client_socket.sendall(risposta.encode('utf-8'))

            if risposta.lower() == 'no':
                print("Gioco terminato.")
                break

    except Exception as e:
        print(f"Errore: {e}")  # In caso di errore, lo stampa

    finally:
        client_socket.close()  # Chiude il socket (connessione)

if __name__ == "__main__":
    main()
