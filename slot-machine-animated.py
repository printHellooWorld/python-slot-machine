import random
import tkinter as tk
from tkinter import font

def spin_row():
    symbols = ['🍒', '🍋', '🔔', '🍉', '⭐']
    return [random.choice(symbols) for _ in range(3)]

def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == '🍒':
            return bet * 3
        elif row[0] == '🍋':
            return bet * 4
        elif row[0] == '🔔':
            return bet * 5
        elif row[0] == '🍉':
            return bet * 10
        elif row[0] == '⭐':
            return bet * 20
    return 0

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Slot Machine")
        self.balance = 100
        self.create_widgets()
        self.update_balance_label()

    def create_widgets(self):
        self.symbol_font = font.Font(size=48)
        
        self.balance_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.balance_label.pack(pady=20)
        
        self.slot_frame = tk.Canvas(self.root, width=300, height=100)
        self.slot_frame.pack()

        self.slot_items = [
            self.slot_frame.create_text(50, 50, text='🍒', font=self.symbol_font),
            self.slot_frame.create_text(150, 50, text='🍒', font=self.symbol_font),
            self.slot_frame.create_text(250, 50, text='🍒', font=self.symbol_font)
        ]

        self.bet_entry = tk.Entry(self.root, font=("Arial", 18))
        self.bet_entry.pack(pady=20)
        
        self.spin_button = tk.Button(self.root, text="Spin", command=self.spin, font=("Arial", 18), bg="green", fg="white")
        self.spin_button.pack(pady=20)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.result_label.pack(pady=20)

    def update_balance_label(self):
        self.balance_label.config(text=f"Current Balance: ${self.balance}")

    def spin(self):
        bet = self.bet_entry.get()
        if not bet.isdigit():
            self.result_label.config(text="Please enter a valid number")
            return

        bet = int(bet)
        if bet > self.balance:
            self.result_label.config(text="Insufficient funds")
            return

        if bet <= 0:
            self.result_label.config(text="Bet must be greater than 0")
            return

        self.balance -= bet
        self.update_balance_label()
        
        # Animation part
        self.animate_spin(bet)

    def animate_spin(self, bet):
        for i in range(10):
            row = spin_row()
            for j in range(3):
                self.slot_frame.itemconfig(self.slot_items[j], text=row[j])
                self.slot_frame.itemconfig(self.slot_items[j], fill=self.get_color(row[j]))
            self.root.update()
            self.root.after(100)  # Wait for 100ms

        # Final spin result
        row = spin_row()
        for j in range(3):
            self.slot_frame.itemconfig(self.slot_items[j], text=row[j])
            self.slot_frame.itemconfig(self.slot_items[j], fill=self.get_color(row[j]))

        payout = get_payout(row, bet)
        if payout > 0:
            self.result_label.config(text=f"You won ${payout}!", fg="green")
        else:
            self.result_label.config(text="Sorry, you lost this round.", fg="red")
        
        self.balance += payout
        self.update_balance_label()
        
        if self.balance <= 0:
            self.result_label.config(text="Game over! Your final balance is $0", fg="red")
            self.spin_button.config(state="disabled")

    def get_color(self, symbol):
        colors = {
            '🍒': 'red',
            '🍋': 'yellow',
            '🔔': 'orange',
            '🍉': 'green',
            '⭐': 'gold'
        }
        return colors.get(symbol, 'black')

if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()
