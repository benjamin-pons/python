import customtkinter as ctk
from case import Case
import time
import random
from PIL import Image

class Minesweeper(ctk.CTk):
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.geometry("600x650")

        self.root.grid_columnconfigure(0, weight=1)
        
        self.top_frame = ctk.CTkFrame(root)
        self.top_frame.grid(row=0, column=0, pady=20)


        self.top_frame.grid_columnconfigure((0, 1), weight=1)

        self.new_game_btn = ctk.CTkButton(self.top_frame, text="Nouveau jeu", width=100, command=self.new_game)
        self.new_game_btn.grid(column=1, row=0, padx=5)

        self.difficulty_menu = ctk.CTkOptionMenu(self.top_frame, width=100, values=["Facile", "Moyen", "Difficile"], command=self.option_changed)
        self.difficulty_menu.grid(column=2, row=0, padx=5)

        # Default difficulty : Easy
        self.grid_size = 5  
        self.case_size = 60
        self.bomb_difficulty = random.randint(3,7)

        self.frame = ctk.CTkFrame(root)
        self.frame.grid(row=1, column=0)


        self.timer = 0
        self.timer_running = False 
        self.first_click = True
        self.chrono_label = ctk.CTkLabel(self.top_frame, text="Temps : 0s")
        self.chrono_label.grid(column=0, row=0, padx=5)

        self.bomb_amount = self.bomb_difficulty
        self.bomb_label = ctk.CTkLabel(self.top_frame, text=f"Bombes : {self.bomb_amount}")
        self.bomb_label.grid(column=3, row=0, padx=5)
    
        self.new_game()
    

    def create_grid(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.buttons = []

        for row in range(self.grid_size):
            row_buttons = []
            for col in range(self.grid_size):
                case = Case(self, row, col, False)
                row_buttons.append(case)

            self.buttons.append(row_buttons)
        
        
    
    def get_is_bomb(self, row, column) :
        # If case doesn't exist
        if (row < 0) or (column < 0) or (row > self.grid_size-1) or (column > self.grid_size-1) :
            return False

        if self.buttons[row][column].is_bomb :
            return True
        else :
            return False

    def option_changed(self, choice):
        if choice == "Facile":
            self.grid_size = 5
            self.case_size = 60
            self.bomb_difficulty = random.randint(3,7)
        elif choice == "Moyen":
            self.grid_size = 10
            self.case_size = 40
            self.bomb_difficulty = random.randint(13,17)
        elif choice == "Difficile":
            self.grid_size = 15
            self.case_size = 25
            self.bomb_difficulty = random.randint(25,35)
        
        # Restart game after difficulty is changed
        self.restart() 

    def new_game(self):
        self.create_grid()
        self.timer = 0
        self.bomb_amount = self.bomb_difficulty
        self.update_ui()
        self.first_click = True
        self.timer_running = False
        self.chrono_label.configure(text="Temps : 0s")

    def start_game(self, row, column):
        if self.first_click == True:
            self.timer_running = True
            self.first_click = False
            self.update_ui()
            for i in range(self.bomb_difficulty) :
                self.generate_bomb(row, column)
    
    def generate_bomb(self, row, column) :
        r = random.randint(0, self.grid_size-1)
        c = random.randint(0, self.grid_size-1)
        
        # If bomb is near first click
        if (row+1 >= r >= row-1) and (column+1 >= c >= column-1) :
            return self.generate_bomb(row, column)

        elif self.buttons[r][c].is_bomb :
            return self.generate_bomb(row, column)
        else :
            self.buttons[r][c].is_bomb = True
            return


    def update_ui(self):
        if self.timer_running:
            self.chrono_label.configure(text=f"Temps : {self.timer}s")
            self.bomb_label.configure(text=f"Bombes : {self.bomb_amount}")
            self.timer += 1
            self.root.after(1000, self.update_ui)

    
    def check_win(self):
        for row in self.buttons:
            for case in row:
                if not case.is_bomb and not case.revealed:
                    return
        self.timer_running = False
        time.sleep(1)
        self.show_win_screen()


    def lose_game(self):
        self.timer_running = False
        time.sleep(1)
        self.show_lose_screen()
    

    def show_lose_screen(self):
        self.frame.grid_forget()

        self.lose_frame = ctk.CTkFrame(self.root)
        self.lose_frame.grid(row=1, column=0, pady=20)

        lose_text = f"💥 Tu as perdu ! Temps : {self.timer}s 💥"
        lose_label = ctk.CTkLabel(self.lose_frame, text=lose_text, font=("Arial", 24))
        lose_label.grid(column=0, row=0, padx=5, pady=20)

        self.lose_image = ctk.CTkImage(light_image=Image.open("assets\lose.png"), size=(510, 361))
        image_label = ctk.CTkLabel(self.lose_frame, image=self.lose_image, text="")
        image_label.grid(column=0, row=1, pady=10)

        restart_button = ctk.CTkButton(self.lose_frame, text="Rejouer", command=self.restart)
        restart_button.grid(column=0, row=2, pady=20)


    def show_win_screen(self):
        self.frame.grid_forget()

        self.win_frame = ctk.CTkFrame(self.root)
        self.win_frame.grid(row=1, column=0, pady=20)

        win_text = f"💥 Tu as gagné ! Temps : {self.timer}s 💥"
        win_label = ctk.CTkLabel(self.win_frame, text=win_text, font=("Arial", 24))
        win_label.grid(column=0, row=0, padx=5, pady=20)

        self.win_image = ctk.CTkImage(light_image=Image.open("assets\win.png"), size=(510, 361))
        image_label = ctk.CTkLabel(self.win_frame, image=self.win_image, text="")
        image_label.grid(column=0, row=1, pady=10)

        restart_button = ctk.CTkButton(self.win_frame, text="Rejouer", command=self.restart)
        restart_button.grid(column=0, row=2, padx=5)
        
    
    def restart(self):
        try :
            self.lose_frame.destroy()
        except :
            pass

        try :
            self.win_frame.destroy()        
        except :
            pass
        
        self.frame.grid(row=1, column=0)
        self.new_game()

if __name__ == "__main__":
    root = ctk.CTk()
    game = Minesweeper(root)
    root.mainloop()
