import os
import sys
import time
import threading
from pdf_chatbot.core import ensure_pdf_folder, load_or_build_index, get_query_engine

# Fargekoder via ANSI escape (eller bruk colorama)
try:
    from colorama import init, Fore, Style
    init()  # For Windows støtte
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
    BLUE = Fore.BLUE
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
except ImportError:
    BOLD = "\033[1m"
    RESET = "\033[0m"
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"

# Tenker-animasjon
class Spinner:
    def __init__(self, message="Tenker"):
        self.stop_running = False
        self.thread = threading.Thread(target=self.animate)
        self.message = message

    def animate(self):
        spinner_chars = "|/-\\"
        idx = 0
        while not self.stop_running:
            sys.stdout.write(f"\r{CYAN}{self.message}...{spinner_chars[idx % len(spinner_chars)]}{RESET}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 5) + '\r')  # rydd linjen

    def start(self):
        self.stop_running = False
        self.thread.start()

    def stop(self):
        self.stop_running = True
        self.thread.join()

def main():
    print(f"{BOLD}📚 CLI Chatbot med PDF-kontext (valgfritt){RESET}\n")

    pdf_files = ensure_pdf_folder()

    if pdf_files:
        print(f"{BLUE}[INFO]{RESET} Fant {len(pdf_files)} PDF-fil(er). Laster eller bygger indeks ...")
    else:
        print(f"{CYAN}[INFO]{RESET} Ingen PDF-er funnet. Starter uten PDF-kontekst.")

    index = load_or_build_index(pdf_files)
    query_engine = get_query_engine(index)

    while True:
        try:
            user_input = input(f"{BOLD}{BLUE}Du:{RESET} ")
            if user_input.lower() in ['exit', 'quit']:
                print(f"{CYAN}Avslutter chatten. Ha en fin dag!{RESET}")
                break

            spinner = Spinner()
            spinner.start()

            if index:
                response = query_engine.query(user_input)
                spinner.stop()
                print(f"{BOLD}{GREEN}Bot:{RESET} ", end='', flush=True)
                for token in response.response_gen:
                    print(token, end='', flush=True)
                print()
            else:
                spinner.stop()
                print(f"{BOLD}{GREEN}Bot:{RESET} {CYAN}[INFO]{RESET} Du spurte: '{user_input}', men ingen PDF-kontekst er lastet.")

        except KeyboardInterrupt:
            print(f"\n{CYAN}Avslutter chatten.{RESET}")
            break

if __name__ == "__main__":
    main()