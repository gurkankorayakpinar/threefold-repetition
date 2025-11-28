import tkinter as tk
from tkinter import scrolledtext
import chess
import chess.pgn
import io
from collections import defaultdict

def fen_key(full_fen):
    # Sadece "taş dizilimi" değil; hamlede olan oyuncu, rok hakları ve "en passant" hakkı da dikkate alınmaktadır.
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
        return  # UYARI VERME, SADECE ÇIK

    try:
        game = chess.pgn.read_game(io.StringIO("[Event \"?\"]\n\n" + moves_str))
        if game is None:
            return  # HATA VERME
    except:
        return  # HATA VERME

    board = chess.Board()
    fen_counts = defaultdict(int)
    output_lines = []

    move_number = 1
    fen_index = 0  # her iki FEN için sayım
    halfmove_clock_triggered = False  # 50 hamle kuralı tamamlandığını kontrol etmek için
    halfmove_warning_triggered = False  # 50 hamle kuralı uyarısı için tetikleyici

    for move_index, move in enumerate(game.mainline_moves()):
        board.push(move)
        full_fen = board.fen()
        key = fen_key(full_fen)  # FEN'in tamamını dikkate alıyoruz

        # Halfmove clock'u alıyoruz
        fields = full_fen.split()
        halfmove_clock = int(fields[4])

        # Eğer halfmove clock 100 veya daha büyükse, "50 hamle" uyarısını ekle
        if halfmove_clock >= 100 and not halfmove_warning_triggered:
            output_lines.append("\n\n\nUyarı: 50 hamle kuralı, aşağıdaki hamle ile tamamlandı.\n\n")
            halfmove_warning_triggered = True  # Uyarıyı sadece bir kez ekliyoruz

        # Fen kodunu kaydediyoruz
        fen_counts[key] += 1
        count = fen_counts[key]

        prefix = f"{move_number} -"

        if count == 1:
            line = f"{prefix} {full_fen}"
        else:
            line = f"{prefix} {full_fen}    <-- tekrar ({count}. kez)"

        output_lines.append(line)

        fen_index += 1
        if fen_index % 2 == 0:
            move_number += 1

    # Sonuçları ekrana yaz
    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)

    # Fen kodlarını yazdır
    for i, ln in enumerate(output_lines, start=1):
        output_box.insert(tk.END, ln + "\n")
        if i % 2 == 0:
            output_box.insert(tk.END, "\n")  # her iki satırdan sonra boşluk

    output_box.config(state='disabled')

# GUI Setup
root = tk.Tk()
root.title("Konum Tekrarı (v. 1.0)")

WINDOW_W = 850
WINDOW_H = 825

# Boyut sabitleme yok. (Tam ekran yapılabilir.)
root.resizable(True, True)

# Pencereyi ortala
center_window(root, WINDOW_W, WINDOW_H)

label = tk.Label(root, text="Notasyonun İngilizce olması gerekmektedir.", font=("Arial", 12))
label.pack(pady=5)

input_box = scrolledtext.ScrolledText(root, width=110, height=10, font=("Consolas", 11))
input_box.pack(pady=5)

process_button = tk.Button(root, text="Hesapla", command=process_moves,
                           font=("Arial", 12), bg="#1976D2", fg="white")
process_button.pack(pady=10)

warning_label = tk.Label(root, text="Program, FIDE kuralları 9.2.3 dikkate alınarak hazırlanmıştır.\n'Hamlede olan' oyuncu, 'rok' durumu ve 'en passant' kontrolleri yapılmaktadır.\n\n(Ayrıca, '50 hamle' kontrolü de yapılmaktadır.)",
                         font=("Arial", 12))
warning_label.pack(pady=2)

output_box = scrolledtext.ScrolledText(root, width=110, height=22, font=("Consolas", 11))
output_box.pack(pady=5)
output_box.config(state='disabled')

footer = tk.Label(root, text="Düzenleyen: Gürkan Koray Akpınar", font=("Arial", 12, "bold"))
footer.pack(pady=5)

root.mainloop()
