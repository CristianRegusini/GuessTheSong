def gestisci_client(connessione, indirizzo):
    """Gestisce la comunicazione con un singolo client."""
    print(f"Connessione stabilita con {indirizzo}")
    try:
        while True:
            dati = connessione.recv(1024)  # Riceve fino a 1024 byte di dati
            if not dati:
                break  # Il client ha chiuso la connessione
            messaggio = dati.decode('utf-8')
            print(f"\nRicevuto da {indirizzo}: {messaggio}")

            # Chiedi all'operatore del server una risposta personalizzata
            risposta = input(f"Inserisci la risposta per {indirizzo}: ")

            connessione.sendall(risposta.encode('utf-8'))
    except Exception as e:
        print(f"Errore nella comunicazione con {indirizzo}: {e}")
    finally:
        connessione.close()
        print(f"Connessione con {indirizzo} chiusa")
