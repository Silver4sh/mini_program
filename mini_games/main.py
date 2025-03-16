import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Helper: Buat window standar dengan style konsisten ---
def create_game_window(title, width, height, bg_color="#e6f2ff"):
    win = tk.Toplevel()
    win.title(title)
    win.geometry(f"{width}x{height}")
    win.configure(bg=bg_color)
    return win

# --- Mini Game: Guess Number ---
def launch_guess_number():
    win = create_game_window("Guess Number", 300, 250, "#dff0d8")
    
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
            if messagebox.askyesno("Selamat!", "Tebakanmu benar! Main lagi?"):
                win.destroy()
                launch_guess_number()
            else:
                win.destroy()
    
    submit_btn = ttk.Button(win, text="Submit", command=check_guess)
    submit_btn.pack(pady=10)
    
    guess_entry.bind("<Return>", lambda event: check_guess())
    
    back_btn = ttk.Button(win, text="Main Menu", command=win.destroy)
    back_btn.pack(pady=5)

# --- Mini Game: Hang Man dengan tema Buah atau Hewan ---
def launch_hang_man():
    win = create_game_window("Hang Man", 400, 400, "#fff2cc")
    
    # Daftar kata untuk tiap tema
    fruits = ["apel", "pisang", "jeruk", "mangga", "anggur"]
    animals = ["kucing", "anjing", "gajah", "harimau", "kuda"]
    
    theme_frame = ttk.Frame(win)
    theme_frame.pack(pady=10)
    theme_label = ttk.Label(theme_frame, text="Pilih Tema:", font=("Helvetica", 12))
    theme_label.pack(side=tk.LEFT)
    theme_var = tk.StringVar()
    theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, values=["Buah", "Hewan"], state="readonly", font=("Helvetica", 12))
    theme_combo.pack(side=tk.LEFT, padx=5)
    theme_combo.current(0)
    
    start_btn = ttk.Button(win, text="Mulai Game")
    start_btn.pack(pady=5)
    
    word_label = ttk.Label(win, text="", font=("Helvetica", 20))
    info_label = ttk.Label(win, text="", font=("Helvetica", 12))
    letter_entry = ttk.Entry(win, font=("Helvetica", 12))
    message_label = ttk.Label(win, text="", font=("Helvetica", 10))
    submit_btn = ttk.Button(win, text="Tebak")
    
    word = ""
    guessed = []
    attempts = 6
    used_letters = set()
    
    def start_game():
        nonlocal word, guessed, attempts, used_letters
        used_letters = set()
        attempts = 6
        theme = theme_var.get()
        if theme == "Buah":
            word = random.choice(fruits)
        else:
            word = random.choice(animals)
        guessed = ["_" for _ in word]
        
        theme_frame.pack_forget()
        start_btn.pack_forget()
        
        word_label.config(text=" ".join(guessed))
        word_label.pack(pady=10)
        info_label.config(text=f"Sisa kesempatan: {attempts}")
        info_label.pack(pady=5)
        letter_entry.pack(pady=5)
        message_label.pack(pady=5)
        submit_btn.pack(pady=10)
    
    start_btn.config(command=start_game)
    
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
            if messagebox.askyesno("Selamat!", "Kamu berhasil menebak kata! Main lagi?"):
                win.destroy()
                launch_hang_man()
            else:
                win.destroy()
        elif attempts <= 0:
            if messagebox.askyesno("Game Over", f"Kamu kalah! Kata yang benar adalah '{word}'. Main lagi?"):
                win.destroy()
                launch_hang_man()
            else:
                win.destroy()
    
    letter_entry.bind("<Return>", lambda event: guess_letter())
    submit_btn.config(command=guess_letter)
    
    back_btn = ttk.Button(win, text="Main Menu", command=win.destroy)
    back_btn.pack(pady=5)

# --- Mini Game: Rock Paper Scissor ---
def launch_rock_paper_scissor():
    win = create_game_window("Rock Paper Scissor", 300, 250, "#f2d7d5")
    
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
    
    def reset_game():
        result_label.config(text="Pilih salah satu!")
    
    reset_btn = ttk.Button(win, text="Reset", command=reset_game)
    reset_btn.pack(pady=5)
    
    back_btn = ttk.Button(win, text="Main Menu", command=win.destroy)
    back_btn.pack(pady=5)

# --- Mini Game: Rolling Dice ---
def launch_rolling_dice():
    win = create_game_window("Rolling Dice", 300, 250, "#d9edf7")
    
    result_label = ttk.Label(win, text="Tekan tombol untuk lempar dadu", font=("Helvetica", 14))
    result_label.pack(pady=20)
    
    def roll_dice():
        dice_value = random.randint(1, 6)
        result_label.config(text=f"Nilai dadu: {dice_value}")
    
    roll_btn = ttk.Button(win, text="Roll Dice", command=roll_dice)
    roll_btn.pack(pady=10)
    
    back_btn = ttk.Button(win, text="Main Menu", command=win.destroy)
    back_btn.pack(pady=5)

# --- GUI Utama ---
def main():
    root = tk.Tk()
    root.title("Koleksi Mini Games")
    root.geometry("450x250")
    root.configure(bg="#f0f0f0")
    
    # Menu Bar
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)
    
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", 
        "Mini Games Collection v1.0\nDibuat dengan Python dan Tkinter.\nKesederhanaan bisa jadi awal revolusi!"))
    menu_bar.add_cascade(label="Help", menu=help_menu)
    
    root.config(menu=menu_bar)
    
    title_label = ttk.Label(root, text="Mini Games Collection", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=15)
    
    instruction_label = ttk.Label(root, text="Pilih mini game dari dropdown di bawah:", font=("Helvetica", 12))
    instruction_label.pack(pady=5)
    
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
