import os
import subprocess
import platform
import readline  # macOS/Linux
from utils import load_config, load_aliases, save_aliases, run_shell_command

# For tab completion of commands and filenames
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

def get_colored_prompt(username, hostname, cwd, color_code):
    RESET = "\033[0m"
    COLOR = f"\033[{color_code}m"
    return f"{COLOR}{username}@{hostname}:{cwd} 🐦>{RESET} "

def main():
    aliases = load_aliases()
    settings = load_config()
    username = os.getlogin()
    hostname = platform.node()

    # Setup tab completion
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    # Get color code from config (default green = 32)
    config = load_config()
    color_code = config.getint("settings", "color_code", fallback=32)

    while True:
        try:
            cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
            prompt = get_colored_prompt(username, hostname, cwd, color_code)
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

if __name__ == "__main__":
    main()
