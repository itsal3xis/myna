import os
import subprocess
import platform
import sys
from utils import load_config, load_aliases, save_aliases, run_shell_command, configparser
import atexit

# Only import readline if not on Windows
if platform.system() != "Windows":
    import readline  # macOS/Linux

# For tab completion of commands and filenames (Linux)
def completer(text, state):
    line = readline.get_line_buffer().split()
    if not line or len(line) == 1:
        completions = [cmd for cmd in os.listdir('.') if cmd.startswith(text)]
        completions += [cmd for cmd in os.environ.get("PATH", "").split(os.pathsep)
                        for cmd in (os.listdir(cmd) if os.path.isdir(cmd) else [])
                        if cmd.startswith(text)]
    else:
        completions = []
    return completions[state] if state < len(completions) else None

def linux_shell(aliases, config, username, hostname, color_code):
    # Check if auto_complete is enabled in config
    auto_complete = config.getboolean("settings", "auto_complete", fallback=True)
    if auto_complete:
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
    
    while True:
        try:
            cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
            prompt = f"\033[{color_code}m{username}@{hostname}:{cwd} 🐦>\033[0m"
            cmd_input = input(prompt).strip()
            
            if not cmd_input:
                continue
            
            if cmd_input in ['exit', 'quit']:
                print("👋 Exiting shell.")
                break
            
            if cmd_input.startswith("cd "):
                target = cmd_input[3:].strip()
                try:
                    os.chdir(os.path.expanduser(target))
                except FileNotFoundError:
                    print("📁 Folder not found.")
                continue
            
            if cmd_input in aliases:
                real_cmd = aliases[cmd_input]
                print(f"🔁 Alias: {cmd_input} → {real_cmd}")
                run_shell_command(real_cmd)
                continue
            
            result = subprocess.run(cmd_input, shell=True)
            
            if result.returncode != 0:
                response = input(f"❓ Unknown command '{cmd_input}'. Create alias? (y/N): ").strip().lower()
                if response == 'y':
                    new_cmd = input(f"📝 Real command for '{cmd_input}': ").strip()
                    aliases[cmd_input] = new_cmd
                    save_aliases(aliases)
                    print(f"✅ Alias saved: {cmd_input} → {new_cmd}")
                    run_shell_command(new_cmd)
                    HISTFILE = os.path.expanduser("~/.myna_shell_history")
                    try:
                        readline.read_history_file(HISTFILE)
                    except FileNotFoundError:
                        pass
                    atexit.register(readline.write_history_file, HISTFILE)
                    
        except KeyboardInterrupt:
            print("\n🚫 Use 'exit' to quit.")
        except EOFError:
            print("\n👋 Goodbye!")
            break

def windows_shell(aliases, config, username, hostname, color_code):
    # Windows: ANSI colors work on newer versions.
    # Windows does not have readline built-in so we skip tab completion.
    while True:
        try:
            cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
            prompt = f"\033[{color_code}m{username}@{hostname}:{cwd} 🐦>\033[0m"
            cmd_input = input(prompt).strip()
            
            if not cmd_input:
                continue
            
            if cmd_input in ['exit', 'quit']:
                print("👋 Exiting shell.")
                break
            
            if cmd_input.startswith("cd "):
                target = cmd_input[3:].strip()
                try:
                    os.chdir(os.path.expanduser(target))
                except FileNotFoundError:
                    print("📁 Folder not found.")
                continue
            
            if cmd_input in aliases:
                real_cmd = aliases[cmd_input]
                print(f"🔁 Alias: {cmd_input} → {real_cmd}")
                run_shell_command(real_cmd)
                continue
            
            result = subprocess.run(cmd_input, shell=True)
            
            if result.returncode != 0:
                response = input(f"❓ Unknown command '{cmd_input}'. Create alias? (y/N): ").strip().lower()
                if response == 'y':
                    new_cmd = input(f"📝 Real command for '{cmd_input}': ").strip()
                    aliases[cmd_input] = new_cmd
                    save_aliases(aliases)
                    print(f"✅ Alias saved: {cmd_input} → {new_cmd}")
                    run_shell_command(new_cmd)
                    
        except KeyboardInterrupt:
            print("\n🚫 Use 'exit' to quit.")
        except EOFError:
            print("\n👋 Goodbye!")
            break

def main():
    aliases = load_aliases()
    config = load_config()
    username = os.getlogin()
    hostname = platform.node()
    
    # Get prompt color with fallback
    try:
        color_code = config.getint("appearance", "prompt_color")
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
        print("Error: Invalid or missing 'prompt_color'. Using default (37).")
        color_code = 37  # Default to white

    # Switch functions based on OS
    if platform.system() == "Windows":
        windows_shell(aliases, config, username, hostname, color_code)
    else:
        linux_shell(aliases, config, username, hostname, color_code)

if __name__ == "__main__":
    main()
