import random
import tkinter as tk
from tkinter import messagebox
 
BG, PANEL, ACCENT, TEXT = "#101827", "#1d2b40", "#32d6ac", "#edf5ff"


def has_bingo(marked):
    lines = [[(r, c) for c in range(5)] for r in range(5)]
    lines += [[(r, c) for r in range(5)] for c in range(5)]
    lines += [[(i, i) for i in range(5)], [(i, 4 - i) for i in range(5)]]
    return any(all(cell in marked for cell in line) for line in lines)


def make_card():
    columns = [random.sample(range(1 + 15 * c, 16 + 15 * c), 5) for c in range(5)]
    return [[columns[c][r] for c in range(5)] for r in range(5)]


class BingoApp:
    def __init__(self, root):
        self.root = root
        root.title("Bingo Blitz")
        root.configure(bg=BG)
        root.resizable(False, False)
        tk.Label(root, text="BINGO BLITZ", font=("Segoe UI", 23, "bold"), bg=BG, fg=ACCENT).pack(pady=(16, 2))
        self.status = tk.Label(root, bg=BG, fg=TEXT, font=("Segoe UI", 12))
        self.status.pack(pady=5)
        self.grid_frame = tk.Frame(root, bg=BG)
        self.grid_frame.pack(padx=18, pady=8)
        controls = tk.Frame(root, bg=BG)
        controls.pack(pady=(8, 16))
        tk.Button(controls, text="CALL A NUMBER", command=self.call, bg=ACCENT, font=("Segoe UI", 11, "bold"), relief="flat", padx=12).pack(side="left", padx=5)
        tk.Button(controls, text="NEW CARD", command=self.new_game, bg=PANEL, fg=TEXT, relief="flat", padx=12, pady=6).pack(side="left", padx=5)
        self.history = tk.Label(root, text="", bg=BG, fg="#9eb1c9", wraplength=360)
        self.history.pack(pady=(0, 12))
        self.new_game()

    def new_game(self):
        self.card = make_card()
        self.called = set()
        self.marked = {(2, 2)}
        self.pool = list(range(1, 76))
        random.shuffle(self.pool)
        self.done = False
        for child in self.grid_frame.winfo_children():
            child.destroy()
        self.buttons = {}
        for col, letter in enumerate("BINGO"):
            tk.Label(self.grid_frame, text=letter, width=5, bg=BG, fg=ACCENT,
                     font=("Segoe UI", 15, "bold")).grid(row=0, column=col, pady=4)
        for r in range(5):
            for c in range(5):
                number = "FREE" if (r, c) == (2, 2) else str(self.card[r][c])
                btn = tk.Button(self.grid_frame, text=number, width=5, height=2,
                                bg=PANEL, fg=TEXT, font=("Segoe UI", 11, "bold"), relief="flat",
                                command=lambda row=r, col=c: self.mark(row, col))
                btn.grid(row=r + 1, column=c, padx=3, pady=3)
                self.buttons[r, c] = btn
        self.buttons[2, 2].config(bg=ACCENT, fg=BG)
        self.status.config(text="Press CALL A NUMBER to begin")
        self.history.config(text="Mark a square only after its number is called.")

    def call(self):
        if self.done or not self.pool:
            return
        number = self.pool.pop()
        self.called.add(number)
        letter = "BINGO"[(number - 1) // 15]
        self.status.config(text=f"Called: {letter}-{number}  |  {len(self.called)} / 75")
        self.history.config(text="Recent calls: " + ", ".join(str(n) for n in sorted(self.called)[-12:]))
        for (r, c), btn in self.buttons.items():
            if self.card[r][c] == number and (r, c) not in self.marked:
                btn.config(bg="#42688a")
        if not self.pool:
            messagebox.showinfo("All called", "All numbers have been called. Check your card!")

    def mark(self, r, c):
        if self.done or (r, c) in self.marked or self.card[r][c] not in self.called:
            return
        self.marked.add((r, c))
        self.buttons[r, c].config(bg=ACCENT, fg=BG)
        if has_bingo(self.marked):
            self.done = True
            self.status.config(text="BINGO! YOU WON!")
            messagebox.showinfo("BINGO!", "Five in a row. You win!")


if __name__ == "__main__":
    window = tk.Tk()
    BingoApp(window)
    window.mainloop()
