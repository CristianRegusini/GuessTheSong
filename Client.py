import socket

def recv_until_prompt(sock):
    buffer = ""
    while not buffer.endswith(": ") and not buffer.endswith("): "):
        data = sock.recv(1024).decode('utf-8')
        if not data:
            break
        buffer += data
    print(buffer, end="")
    return buffer

def recv_full_block(sock):
    data = sock.recv(4096).decode('utf-8')
    if data:
        print(data)
    return data

def main():
    host = '127.0.0.1'
    port = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))

        recv_until_prompt(client_socket)
        username = input()
        client_socket.sendall(username.encode('utf-8'))

        while True:
            recv_until_prompt(client_socket)  # strofa + primo prompt
            client_socket.sendall(input().encode('utf-8'))

            recv_until_prompt(client_socket)  # artista
            client_socket.sendall(input().encode('utf-8'))

            recv_until_prompt(client_socket)  # anno
            client_socket.sendall(input().encode('utf-8'))

            recv_until_prompt(client_socket)  # featuring
            client_socket.sendall(input().encode('utf-8'))

            recv_full_block(client_socket)  # risultati

            recv_until_prompt(client_socket)  # vuoi continuare?
            risposta = input()
            client_socket.sendall(risposta.encode('utf-8'))

            if risposta.lower() == 'no':
                recv_full_block(client_socket)  # messaggio finale
                print("Gioco terminato.")
                break

    except Exception as e:
        print(f"Errore: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
