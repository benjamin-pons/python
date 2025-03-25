import customtkinter as ctk


NUM_MIN = 15  

class Démineur(ctk.CTk):
    def __init__(self, root, grid_size):
        self.root = root
        self.root.title("Démineur")
        self.root.geometry("550x600")
        self.grid_size = grid_size
        
        self.top_frame = ctk.CTkFrame(root)
        self.top_frame.grid(row=0, column=0, pady=2)

        self.top_frame.grid_columnconfigure((0, 1), weight=1)

        
        self.new_game_btn = ctk.CTkButton(self.top_frame, text="Nouveau jeu", width=100, command=lambda: print("Nouveau jeu"))
        self.new_game_btn.grid(column=0, row=0, padx=5)
        
        self.difficulty_menu = ctk.CTkOptionMenu(self.top_frame, width=100, values=["Facile", "Moyen", "Difficile"],command=self.option_changed)
        self.difficulty_menu.grid(column=1, row=0, padx= 5)

        self.grid_size = 15

        self.frame = ctk.CTkFrame(root)
        self.frame.grid(row=1, column=0)

        




        self.buttons = []

        for row in range(self.grid_size):
            row_buttons = []
            for col in range(self.grid_size):
                btn = ctk.CTkButton(self.frame, text="", width=40, height=40)
                btn.grid(row=row, column=col, padx=4, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        

    def option_changed(self, choice):
        if self.option_changed == "Facile" :
            self.grid_size = 5
        elif self.option_changed == "Moyen":
            self.grid_size = 10
        elif self.option_changed == "Difficile":
            self.grid_size = 15
        
        return


if __name__ == "__main__":
    root = ctk.CTk()
    game = Démineur(root)
    root.mainloop()
