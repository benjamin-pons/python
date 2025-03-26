import customtkinter as ctk

class Case(ctk.CTkButton) :
    def __init__(self, parent, row, column, is_bomb) :
        
        self.parent = parent
        self.text = ""
        self.row = row
        self.column = column
        self.is_bomb = is_bomb

        super().__init__(parent.frame, text=self.text, width=parent.case_size, height=parent.case_size)
        

        self.grid(row=self.row, column=self.column, padx=4, pady=4)

        self.bind("<Button-1>", command=self.left_click)
        self.bind("<Button-3>", command=self.right_click)

    
    def right_click(self, event) :
        print("Right Click")
    
    def left_click(self, event) :
        if self.is_bomb == True:
            self.text = "MINE"
            self.configure(text=self.text, fg_color="red", hover_color="red")
        else : 
            self.reveal()

    def reveal(self) :
        print("Pas Boom")
        self.text = self.get_number()
        self.configure(text=self.text, fg_color="green", hover_color="green")
    
    def get_number(self) :
        c = self.column - 1
        number = 0
        for i in range(3) :
            r = self.row - 1
            for j in range(3) :
                print(f"Checking : {r},{c}")
                if self.parent.get_is_bomb(r, c) :
                    number += 1
                r += 1
            c += 1

        return number