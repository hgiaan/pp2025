import subprocess
import os

def run_shell():
    while True:
        try:
            command = input("my-shell$ ").strip()
            
            if not command:
                continue
            
            if command == "exit":
                break

            if "|" in command:
                parts = command.split("|")
                cmd1 = parts[0].strip().split()
                cmd2 = parts[1].strip().split()

                p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
                p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
                
                p1.stdout.close()
                output, _ = p2.communicate()
                print(output.decode())

            elif ">" in command:
                parts = command.split(">")
                cmd = parts[0].strip().split()
                filename = parts[1].strip()
                
                with open(filename, "w") as f:
                    subprocess.run(cmd, stdout=f)

            elif "<" in command:
                parts = command.split("<")
                cmd = parts[0].strip().split()
                filename = parts[1].strip()
                
                try:
                    with open(filename, "r") as f:
                        subprocess.run(cmd, stdin=f)
                except FileNotFoundError:
                    print(f"File '{filename}' not found.")

            else:
                parts = command.split()
                if parts[0] == "cd":
                    try:
                        os.chdir(parts[1])
                    except FileNotFoundError:
                        print(f"cd: no such file or directory: {parts[1]}")
                else:
                    subprocess.run(parts)

        except FileNotFoundError:
            print("Command not found.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_shell()