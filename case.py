import customtkinter as ctk

class Case(ctk.CTkButton) :
    def __init__(self, parent, row, column, is_bomb) :
        
        self.BASE_COLOR_BLUE = "#0362fc"
        self.HOVER_COLOR_BLUE = "#0249bd"

        self.parent = parent
        self.text = ""
        self.row = row
        self.column = column
        self.is_bomb = is_bomb

        self.revealed = False
        self.marked = False
        self.flagged = False

        super().__init__(parent.frame, text=self.text, width=parent.case_size, height=parent.case_size, fg_color=self.BASE_COLOR_BLUE, hover_color=self.HOVER_COLOR_BLUE)
        

        self.grid(row=self.row, column=self.column, padx=4, pady=4)

        self.bind("<Button-1>", command=self.left_click)
        self.bind("<Button-3>", command=self.right_click)
    
    def right_click(self, event) :
        if (self.revealed == False) and (self.marked == False) and (self.flagged == False) : # Blank case
            self.configure(text="?", fg_color="orange", hover_color="yellow")
            self.marked = True
            return

        elif (self.revealed == False) and (self.marked == True) and (self.flagged == False): # Question mark case
            self.configure(text="F", fg_color="red", hover_color="red")
            self.flagged = True
            self.parent.bomb_amount -= 1
            self.marked = False
            return

        elif (self.revealed == False) and (self.marked == False) and (self.flagged == True): # Flagged case
            self.configure(text="", fg_color=self.BASE_COLOR_BLUE, hover_color=self.HOVER_COLOR_BLUE)
            self.flagged = False
            self.parent.bomb_amount += 1
            return
    
    def left_click(self, event) :
        self.parent.start_game(self.row, self.column)

        if self.revealed or self.marked or self.flagged :
            return
        else :
            self.reveal()
    
    def reveal(self) :
        if self.revealed :
            return

        elif self.is_bomb :
            self.revealed = True
            self.text = "B"
            self.configure(text=self.text, fg_color="red", hover_color="red")
            return

        self.revealed = True
        self.text = self.get_number()

        if self.text == 0 :
            self.configure(text="", fg_color="black", hover_color="black")
            for i in range(-1, 2) :
                for j in range(-1, 2) :
                    r = self.row + i
                    c = self.column + j

                    if (r >= 0) and (c >= 0) and (r < self.parent.grid_size) and (c < self.parent.grid_size) :
                        adjacent =  self.parent.buttons[r][c]
                        if adjacent.revealed == False :
                            adjacent.reveal()
        else :
            self.configure(text=self.text, fg_color="green", hover_color="green")


    def get_number(self) :
        c = self.column - 1
        number = 0
        for i in range(3) :
            r = self.row - 1
            for j in range(3) :
                if self.parent.get_is_bomb(r, c) :
                    number += 1
                r += 1
            c += 1

        return number
