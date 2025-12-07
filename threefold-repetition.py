import tkinter as tk
from tkinter import scrolledtext
import chess
import chess.pgn
import io
from collections import defaultdict
import sys, os

# ".ico" dosyası için
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def fen_key(full_fen):
    parts = full_fen.split()
    return " ".join(parts[:4])

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def process_moves():
    moves_str = input_box.get("1.0", tk.END).strip()
    if not moves_str:
        return
  
    try:
        game = chess.pgn.read_game(io.StringIO("[Event \"?\"]\n\n" + moves_str))
        if game is None:
            return
    except:
        return

    board = chess.Board()
    fen_counts = defaultdict(int)
    fen_to_moves = defaultdict(list)

    # Başlangıç FEN kodu
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    start_key = fen_key(starting_fen)
    fen_counts[start_key] += 1
    fen_to_moves[start_key].append(0) # 0 = başlangıç

    output_lines = []
    halfmove_warning_triggered = False
    halfmove_75_triggered = False

    output_lines.append(f"0 - {starting_fen}")
    output_lines.append("")

    move_number = 1
    moves_list = list(game.mainline_moves())

    for idx, move in enumerate(moves_list):
        board.push(move)
        full_fen = board.fen()
        key = fen_key(full_fen)

        # Halfmove clock ("Hamle" sayacı)
        fields = full_fen.split()
        halfmove_clock = int(fields[4])

        # "50 hamle" uyarısı
        if halfmove_clock >= 100 and not halfmove_warning_triggered:
            output_lines.append("\n\nUyarı: 50 hamle kuralı, aşağıdaki hamle ile tamamlanıyor.\n")
            halfmove_warning_triggered = True

        # "75 hamle" uyarısı - FIDE 9.6.2
        if halfmove_clock >= 150 and not halfmove_75_triggered:
            output_lines.append("\n\nUyarı: 75 hamle kuralı, aşağıdaki hamle ile tamamlanıyor.\n")
            halfmove_75_triggered = True

        fen_counts[key] += 1
        count = fen_counts[key]

        current_move_nr = (idx // 2) + 1
        if current_move_nr not in fen_to_moves[key]:
            fen_to_moves[key].append(current_move_nr)

        # "Konum tekrarı" bilgisi
        repeat = ""
        if count > 1:
            previous_moves = sorted(fen_to_moves[key])
            if previous_moves:
                prev_str = "(" + ", ".join(map(str, previous_moves)) + ")"
                repeat = f" ---> {count}. konum {prev_str}"

        if idx % 2 == 0:
            output_lines.append(f"{move_number} - {full_fen}{repeat}")
        else:
            output_lines.append(f"{move_number} - {full_fen}{repeat}")
            output_lines.append("")
            move_number += 1

    if len(moves_list) % 2 == 1:
        output_lines.append("")

    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    for line in output_lines:
        output_box.insert(tk.END, (line if line else "") + "\n")
    output_box.config(state='disabled')

# GUI - Tkinter

root = tk.Tk()
root.title("Konum Tekrarı (1.0)")
root.iconbitmap(resource_path("tsf-icon.ico")) # Proje klasöründeki ".ico" dosyası

WINDOW_W = 850
WINDOW_H = 800

root.geometry(f"{WINDOW_W}x{WINDOW_H}")
center_window(root, WINDOW_W, WINDOW_H)

label = tk.Label(root, text="Notasyonu buraya aktarınız.\n(İngilizce notasyon gerekmektedir.)", font=("Arial", 12))
label.pack(pady=5)

input_box = scrolledtext.ScrolledText(root, width=110, height=12, font=("Consolas", 11))
input_box.pack(pady=5)

process_button = tk.Button(root, text="Kontrol", command=process_moves,
                           font=("Arial", 12), bg="#1976D2", fg="white")
process_button.pack(pady=10)

warning_label = tk.Label(
    root,
    text="Program, FIDE kuralları 9.2.3 dikkate alınarak hazırlanmıştır.\n"
         "'Hamlede olan oyuncu', 'rok' ve 'en passant' durumları dikkate alınmaktadır.\n\n"
         "Ayrıca, '50 hamle' ve '75 hamle' takibi de yapılmaktadır.\n\n"
         "(Düzenleyen: 11841)",
    font=("Arial", 12)
)
warning_label.pack(pady=2)

output_box = scrolledtext.ScrolledText(root, width=110, height=20, font=("Consolas", 11))
output_box.pack(pady=5)
output_box.config(state='disabled')

root.mainloop()