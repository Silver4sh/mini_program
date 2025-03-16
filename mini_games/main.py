import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Mini Game: Guess Number ---
def launch_guess_number():
    win = tk.Toplevel()
    win.title("Guess Number")
    win.geometry("300x200")
    
    # Komputer memilih angka acak antara 1 sampai 100
    number = random.randint(1, 100)
    
    prompt = ttk.Label(win, text="Tebak angka antara 1 sampai 100", font=("Helvetica", 12))
    prompt.pack(pady=10)
    
    result_label = ttk.Label(win, text="", font=("Helvetica", 10))
    result_label.pack(pady=5)
    
    guess_entry = ttk.Entry(win, font=("Helvetica", 12))
    guess_entry.pack(pady=5)
    
    def check_guess():
        try:
            guess = int(guess_entry.get())
        except ValueError:
            result_label.config(text="Masukkan angka yang valid!")
            return
        
        if guess < number:
            result_label.config(text="Terlalu rendah!")
        elif guess > number:
            result_label.config(text="Terlalu tinggi!")
        else:
            result_label.config(text=f"Tepat! Angkanya adalah {number}")
            messagebox.showinfo("Selamat!", "Tebakanmu benar!")
            win.destroy()
    
    submit_btn = ttk.Button(win, text="Submit", command=check_guess)
    submit_btn.pack(pady=10)

# --- Mini Game: Hang Man ---
def launch_hang_man():
    win = tk.Toplevel()
    win.title("Hang Man")
    win.geometry("400x300")
    
    # Untuk kesederhanaan, gunakan kata yang sudah ditentukan
    word = "python"
    guessed = ["_" for _ in word]
    attempts = 6
    used_letters = set()
    
    word_label = ttk.Label(win, text=" ".join(guessed), font=("Helvetica", 20))
    word_label.pack(pady=10)
    
    info_label = ttk.Label(win, text=f"Sisa kesempatan: {attempts}", font=("Helvetica", 12))
    info_label.pack(pady=5)
    
    letter_entry = ttk.Entry(win, font=("Helvetica", 12))
    letter_entry.pack(pady=5)
    
    message_label = ttk.Label(win, text="", font=("Helvetica", 10))
    message_label.pack(pady=5)
    
    def guess_letter():
        nonlocal attempts
        letter = letter_entry.get().lower()
        letter_entry.delete(0, tk.END)
        
        if not letter or len(letter) != 1 or not letter.isalpha():
            message_label.config(text="Masukkan satu huruf yang valid!")
            return
        
        if letter in used_letters:
            message_label.config(text="Huruf sudah ditebak!")
            return
        used_letters.add(letter)
        
        if letter in word:
            for i, l in enumerate(word):
                if l == letter:
                    guessed[i] = letter
            word_label.config(text=" ".join(guessed))
            message_label.config(text="Huruf cocok!")
        else:
            attempts -= 1
            info_label.config(text=f"Sisa kesempatan: {attempts}")
            message_label.config(text="Huruf tidak cocok!")
        
        if "_" not in guessed:
            messagebox.showinfo("Selamat!", "Kamu berhasil menebak kata!")
            win.destroy()
        elif attempts <= 0:
            messagebox.showinfo("Game Over", f"Kamu kalah! Kata yang benar adalah '{word}'.")
            win.destroy()
    
    submit_btn = ttk.Button(win, text="Tebak", command=guess_letter)
    submit_btn.pack(pady=10)

# --- Mini Game: Rock Paper Scissor ---
def launch_rock_paper_scissor():
    win = tk.Toplevel()
    win.title("Rock Paper Scissor")
    win.geometry("300x200")
    
    options = ["Rock", "Paper", "Scissor"]
    
    result_label = ttk.Label(win, text="Pilih salah satu!", font=("Helvetica", 12))
    result_label.pack(pady=10)
    
    def play(user_choice):
        comp_choice = random.choice(options)
        if user_choice == comp_choice:
            outcome = "Seri!"
        elif (user_choice == "Rock" and comp_choice == "Scissor") or \
             (user_choice == "Paper" and comp_choice == "Rock") or \
             (user_choice == "Scissor" and comp_choice == "Paper"):
            outcome = "Kamu menang!"
        else:
            outcome = "Kamu kalah!"
        result_label.config(text=f"Kamu: {user_choice}\nKomputer: {comp_choice}\n{outcome}")
    
    btn_frame = ttk.Frame(win)
    btn_frame.pack(pady=10)
    
    for option in options:
        btn = ttk.Button(btn_frame, text=option, command=lambda opt=option: play(opt))
        btn.pack(side=tk.LEFT, padx=5)

# --- Mini Game: Rolling Dice ---
def launch_rolling_dice():
    win = tk.Toplevel()
    win.title("Rolling Dice")
    win.geometry("300x200")
    
    result_label = ttk.Label(win, text="Tekan tombol untuk lempar dadu", font=("Helvetica", 14))
    result_label.pack(pady=20)
    
    def roll_dice():
        dice_value = random.randint(1, 6)
        result_label.config(text=f"Nilai dadu: {dice_value}")
    
    roll_btn = ttk.Button(win, text="Roll Dice", command=roll_dice)
    roll_btn.pack(pady=10)

# --- GUI Utama ---
def main():
    root = tk.Tk()
    root.title("Koleksi Mini Games")
    root.geometry("400x200")
    
    # Menggunakan tema yang lebih modern
    style = ttk.Style(root)
    style.theme_use('clam')
    
    title_label = ttk.Label(root, text="Mini Games Collection", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)
    
    # Dropdown untuk memilih mini game
    selected_game = tk.StringVar()
    games = ["Guess Number", "Hang Man", "Rock Paper Scissor", "Rolling Dice"]
    game_dropdown = ttk.Combobox(root, textvariable=selected_game, values=games, state="readonly", font=("Helvetica", 12))
    game_dropdown.pack(pady=10)
    game_dropdown.current(0)
    
    def launch_selected_game():
        game = selected_game.get()
        if game == "Guess Number":
            launch_guess_number()
        elif game == "Hang Man":
            launch_hang_man()
        elif game == "Rock Paper Scissor":
            launch_rock_paper_scissor()
        elif game == "Rolling Dice":
            launch_rolling_dice()
        else:
            messagebox.showerror("Error", "Pilih game yang valid!")
    
    launch_btn = ttk.Button(root, text="Play", command=launch_selected_game)
    launch_btn.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
