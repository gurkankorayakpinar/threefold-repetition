import tkinter as tk
from tkinter import scrolledtext
import chess
import chess.pgn
import io
from collections import defaultdict

def fen_key(full_fen):
    # Sadece "taş dizilimi" değil; "hamlede olan" oyuncu, "rok" ve "en passant" durumları da değerlendirilmektedir.
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
        return # UYARI VERME
    
    try:
        game = chess.pgn.read_game(io.StringIO("[Event \"?\"]\n\n" + moves_str))
        if game is None:
            return # HATA VERME
    except:
        return # HATA VERME

    board = chess.Board()
    fen_counts = defaultdict(int)

    # Başlangıç FEN kodu
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen_counts[fen_key(starting_fen)] += 1 # Başlangıç FEN kodunu kaydet

    output_lines = []
    halfmove_warning_triggered = False

    # Başlangıç konumunu çıktı olarak yaz ve bir satır boşluk bırak
    output_lines.append(f"0 - {starting_fen}")
    output_lines.append("")  # başlangıç sonrası boş satır

    move_number = 1
    moves_list = list(game.mainline_moves())

    for idx, move in enumerate(moves_list):
        board.push(move)
        full_fen = board.fen()
        key = fen_key(full_fen)

        # Halfmove clock kontrolü
        fields = full_fen.split()
        halfmove_clock = int(fields[4])

        if halfmove_clock >= 100 and not halfmove_warning_triggered:
            output_lines.append("\n\nUyarı: 50 hamle, aşağıdaki hamle ile tamamlanıyor.\n")
            halfmove_warning_triggered = True

        fen_counts[key] += 1
        count = fen_counts[key]

        repeat = f" ---> {count}. konum" if count > 1 else ""

        if idx % 2 == 0:
            # Beyazın hamlesi sonrası → yeni çiftin ilk satırı
            output_lines.append(f"{move_number} - {full_fen}{repeat}")
        else:
            # Siyahın hamlesi sonrası → aynı numarayı tekrar yaz
            output_lines.append(f"{move_number} - {full_fen}{repeat}")
            output_lines.append("")  # her "tam hamle"den sonra boş satır
            move_number += 1

    # Eğer oyun tek hamleyle bittiyse (sadece beyaz oynadıysa) boş satır bırak
    if len(moves_list) % 2 == 1:
        output_lines.append("")

    # Çıktıyı ekrana yaz
    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    for line in output_lines:
        output_box.insert(tk.END, (line if line else "") + "\n")
    output_box.config(state='disabled')

# GUI Setup
root = tk.Tk()
root.title("Konum Tekrarı (v. 1.0)")

WINDOW_W = 850
WINDOW_H = 800

# Pencereyi oluştur ve boyutunu ayarla
root.geometry(f"{WINDOW_W}x{WINDOW_H}")

# Pencere için "yatay ve dikey ortalama" ayarlandı.
center_window(root, WINDOW_W, WINDOW_H)

label = tk.Label(root, text="Notasyonu buraya aktarınız.\n(İngilizce notasyon gerekmektedir, Va4 yerine Qa4 gibi)", font=("Arial", 12))
label.pack(pady=5)

input_box = scrolledtext.ScrolledText(root, width=110, height=12, font=("Consolas", 11))
input_box.pack(pady=5)

process_button = tk.Button(root, text="Kontrol", command=process_moves,
                           font=("Arial", 12), bg="#1976D2", fg="white")
process_button.pack(pady=10)

warning_label = tk.Label(root, text="Program, FIDE kuralları 9.2.3 dikkate alınarak hazırlanmıştır.\n'Hamlede olan oyuncu', 'rok' ve 'en passant' durumları dikkate alınmaktadır.\n\nAyrıca, '50 hamle' kontrolü de yapılmaktadır.\n\n(github.com/gurkankorayakpinar/threefold-repetition)",
                         font=("Arial", 12))
warning_label.pack(pady=2)

output_box = scrolledtext.ScrolledText(root, width=110, height=20, font=("Consolas", 11))
output_box.pack(pady=5)
output_box.config(state='disabled')

root.mainloop()