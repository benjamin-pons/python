import customtkinter as ctk

class Démineur(ctk.CTk):
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        self.root.geometry("600x650")

        self.root.grid_columnconfigure(0, weight=1)

        self.top_frame = ctk.CTkFrame(root)
        self.top_frame.grid(row=0, column=0)

        self.top_frame.grid_columnconfigure((0, 1), weight=1)

        self.new_game_btn = ctk.CTkButton(self.top_frame, text="Nouveau jeu", width=100, command=self.new_game)
        self.new_game_btn.grid(column=0, row=0, padx=5)

        self.difficulty_menu = ctk.CTkOptionMenu(self.top_frame, width=100, values=["Facile", "Moyen", "Difficile"], command=self.option_changed)
        self.difficulty_menu.grid(column=1, row=0, padx=5)

        self.grid_size = 5

        self.frame = ctk.CTkFrame(root)
        self.frame.grid(row=1, column=0)


        self.temps = 0
        self.running = False 
        self.first_click = True
        self.chrono_label = ctk.CTkLabel(self.top_frame, text="Temps : 0s")
        self.chrono_label.grid(column=2, row=0, padx=5)
    
        self.create_grid()

    def create_grid(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.buttons = [] 

        for row in range(self.grid_size):
            row_buttons = []
            for col in range(self.grid_size):
                btn = ctk.CTkButton(self.frame, text="", width=40, height=40)
                btn.grid(row=row, column=col, padx=4, pady=4)
                btn.bind("<Button-1>", self.on_button_click)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def option_changed(self, choice):
        if choice == "Facile":
            self.grid_size = 5
        elif choice == "Moyen":
            self.grid_size = 10
        elif choice == "Difficile":
            self.grid_size = 15

        self.new_game()

    def new_game(self):
        self.create_grid()
        self.temps = 0
        self.first_click = True
        self.running = False
        self.chrono_label.configure(text="Temps : 0s")
        

    def on_button_click(self, event):
        if self.first_click == True:
            self.running = True
            self.first_click = False
            self.update_chronometre()

    def update_chronometre(self):
        if self.running:
            self.chrono_label.configure(text=f"Temps : {self.temps}s")
            self.temps += 1
            self.root.after(1000, self.update_chronometre)  

if __name__ == "__main__":
    root = ctk.CTk()
    game = Démineur(root)
    root.mainloop()
