import json
import random
import threading
import socket

def carica_strofe(nome_file):
    with open(nome_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data["canzoni"]

def carica_punteggi(nome_file):
    try:
        with open(nome_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def salva_punteggi(punteggi, nome_file):
    with open(nome_file, 'w', encoding='utf-8') as file:
        json.dump(punteggi, file, indent=4)

def avvia_gioco(connessione, username, punteggi, strofe):
    while True:
        strofa_scelta = random.choice(strofe)
        print(f"Inviando strofa: {strofa_scelta['strofa']}")

        connessione.sendall(f"\nIndovina artista, anno, titolo e featuring (se presente) di questa strofa:\n"
                             f"\"{strofa_scelta['strofa']}\"\n".encode('utf-8'))

        connessione.sendall("Inserisci il titolo: ".encode('utf-8'))
        title_risposta = connessione.recv(1024).decode('utf-8').strip().lower()

        connessione.sendall("Inserisci l'artista: ".encode('utf-8'))
        artista_risposta = connessione.recv(1024).decode('utf-8').strip().lower()

        connessione.sendall("Inserisci l'anno: ".encode('utf-8'))
        anno_risposta = connessione.recv(1024).decode('utf-8').strip().lower()

        connessione.sendall("Inserisci il featuring (scrivi 'no' se non c'è): ".encode('utf-8'))
        featuring_risposta = connessione.recv(1024).decode('utf-8').strip().lower()

        title_corretto = strofa_scelta['titolo'].lower()
        artista_corretta = strofa_scelta['artista'].lower()
        anno_corretta = str(strofa_scelta['anno'])
        featuring_corretta = strofa_scelta['featuring'].lower()

        # Normalizza "no" a stringa vuota
        if featuring_risposta in ['no', 'n', '', 'nessuno']:
            featuring_risposta = ''
        if featuring_corretta == 'no':
            featuring_corretta = ''

        risultati = []
        corrette = 0

        if title_risposta == title_corretto:
            risultati.append("Titolo corretto!")
            corrette += 1
        else:
            risultati.append(f"Titolo sbagliato. Era: {strofa_scelta['titolo']}")

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
            risultati.append(f"Featuring sbagliato. Era: {strofa_scelta['featuring']}")

        connessione.sendall("\n".join(risultati).encode('utf-8'))

        # Aggiorna punteggio
        punteggi[username]['punteggio'] += corrette
        salva_punteggi(punteggi, 'punteggi.json')

        connessione.sendall("Vuoi continuare a giocare? (si/no): ".encode('utf-8'))
        risposta = connessione.recv(1024).decode('utf-8').strip().lower()
        if risposta == 'no':
            break

    connessione.sendall(f"\nGrazie per aver giocato, {username}! Punteggio finale: {punteggi[username]['punteggio']}".encode('utf-8'))
    connessione.close()

def gestisci_client(connessione, indirizzo):
    print(f"Connessione da {indirizzo}")
    connessione.sendall("Benvenuto nel gioco! Inserisci il tuo username: ".encode('utf-8'))
    username = connessione.recv(1024).decode('utf-8').strip().lower()

    try:
        strofe = carica_strofe('song.json')
        punteggi = carica_punteggi('punteggi.json')

        if username not in punteggi:
            punteggi[username] = {"punteggio": 0}
            salva_punteggi(punteggi, 'punteggi.json')

        avvia_gioco(connessione, username, punteggi, strofe)

    except Exception as e:
        print(f"Errore con {indirizzo}: {e}")
    finally:
        connessione.close()
        print(f"Connessione con {indirizzo} chiusa")

def avvia_server():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server in ascolto su {host}:{port}")

        while True:
            connessione, indirizzo = server_socket.accept()
            threading.Thread(target=gestisci_client, args=(connessione, indirizzo)).start()

if __name__ == "__main__":
    avvia_server()
