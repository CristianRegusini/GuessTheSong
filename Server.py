import json
import random
import threading
import socket

def carica_strofe(nome_file):
    with open(nome_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data["canzoni"]

def carica_punteggi(nome_file):
    with open(nome_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def salva_punteggi(punteggi, nome_file):
    with open(nome_file, 'w', encoding='utf-8') as file:
        json.dump(punteggi, file, indent=4)

def avvia_gioco(connessione, username, punteggi, strofe):
    while True:
        strofa_scelta = random.choice(strofe)
        print(f"Inviando strofa: {strofa_scelta['strofa']}")  # Debug: vedi quale strofa stiamo inviando

        # Invia la strofa al client
        connessione.sendall(f"\nIndovina artista, anno e featuring (se presente) di questa strofa:\n"
                            f"\"{strofa_scelta['strofa']}\"\n".encode('utf-8'))

        # Chiedi le risposte al client
        connessione.sendall("Inserisci il nome dell'artista: ".encode('utf-8'))
        artista_risposta = connessione.recv(1024).decode('utf-8').strip().lower()
        print(f"Risposta artista ricevuta: {artista_risposta}")  # Debug

        connessione.sendall("Inserisci l'anno: ".encode('utf-8'))
        anno_risposta = connessione.recv(1024).decode('utf-8').strip().lower()
        print(f"Risposta anno ricevuta: {anno_risposta}")  # Debug

        connessione.sendall("Inserisci il featuring (o 'nessuno' se non c'è): ".encode('utf-8'))
        featuring_risposta = connessione.recv(1024).decode('utf-8').strip().lower()
        print(f"Risposta featuring ricevuta: {featuring_risposta}")  # Debug

        # Confronta le risposte con quelle corrette
        artista_corretta = strofa_scelta['artista'].lower()
        anno_corretta = str(strofa_scelta['anno'])
        featuring_corretta = strofa_scelta['featuring'].lower() if strofa_scelta['featuring'] != "no" else "nessuno"

        risultati = []
        corrette = 0

        if artista_risposta == artista_corretta:
            risultati.append("Artista corretto!")
            corrette += 1
        else:
            risultati.append(f"Artista sbagliato. Era: {strofa_scelta['artista']}")

        if anno_risposta == anno_corretta:
            risultati.append("Anno corretto!")
            corrette += 1
        else:
            risultati.append(f"Anno sbagliato. Era: {strofa_scelta['anno']}")

        if featuring_risposta == featuring_corretta:
            risultati.append("Featuring corretto!")
            corrette += 1
        else:
            risultati.append(f"Featuring sbagliato. Era: {strofa_scelta['featuring'] if strofa_scelta['featuring'] != 'no' else 'nessuno'}")

        # Invia i risultati al client
        connessione.sendall("\n".join(risultati).encode('utf-8'))

        # Se tutte le risposte sono corrette, aumenta il punteggio
        if corrette == 3:
            punteggi[username]['punteggio'] += 1
            salva_punteggi(punteggi, 'punteggi.json')

        # Chiedi se vogliono continuare a giocare
        connessione.sendall("Vuoi continuare a giocare? (si/no): ".encode('utf-8'))
        risposta = connessione.recv(1024).decode('utf-8').strip().lower()
        print(f"Risposta continuazione: {risposta}")  # Debug

        if risposta != 'si':
            break

    # Finale del gioco
    connessione.sendall(f"\nGrazie per aver giocato, {username}! Punteggio finale: {punteggi[username]['punteggio']}".encode('utf-8'))

def gestisci_client(connessione, indirizzo):
    print(f"Connessione stabilita con {indirizzo}")
    connessione.sendall("Benvenuto! Iniziamo subito a giocare!\n".encode('utf-8'))

    try:
        strofe = carica_strofe('song.json')  # Carica le strofe da 'song.json'
        punteggi = carica_punteggi('punteggi.json')  # Carica i punteggi

        username = "giocatore"  # Usa un nome predefinito per il giocatore

        if username not in punteggi:
            punteggi[username] = {
                'password': '',  # Non è necessario gestire una password
                'punteggio': 0
            }
            salva_punteggi(punteggi, 'punteggi.json')

        avvia_gioco(connessione, username, punteggi, strofe)

    except Exception as e:
        print(f"Errore nella comunicazione con {indirizzo}: {e}")
    finally:
        connessione.close()
        print(f"Connessione con {indirizzo} chiusa")

def avvia_server():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server in ascolto su {host}:{port}...")

        while True:
            connessione, indirizzo = server_socket.accept()
            threading.Thread(target=gestisci_client, args=(connessione, indirizzo)).start()

if __name__ == "__main__":
    avvia_server()
