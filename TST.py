import tkinter as tk
from tkinter import messagebox


class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Крестики-нолики")
        self.screen_mid_width = self.master.winfo_screenwidth()//2
        self.screen_mid_height = self.master.winfo_screenheight()//2
        self.master.geometry(f'400x400+{self.screen_mid_width-200}+{self.screen_mid_height-200}')
        self.master.resizable(0,0)
        
        self.current_player = "X"
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.game_mode = tk.StringVar(
            value="player")

        """
        Предварительная инициализация статических атрибутов как None 
        для читаемости. Последующие присваения происходят в
        функции create_widgets().
        """
        self.board_frame = None #Фрейм для игрового поля
        self.buttons = None #Список кнопок
        self.new_game_button = None #Кнопка "Новая Игра"
        self.player_mode_button = None #Кнопка "Игра против игрока"
        self.computer_mode_button = None #Кнопка "Игра против компьютера"

        self.create_widgets()
        self.show_info()
        
    def create_widgets(self):

        self.board_frame = tk.Frame(self.master,borderwidth = 1,relief = 'solid')
        self.board_frame.pack(side = 'top', padx=10, pady=10)
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.board_frame, width=4, height=2,bg = "green" ,font=("Arial", 20),
                                   command=lambda x_coord = i, y_coord = j: self.on_button_click(x_coord, y_coord))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

        self.new_game_button = tk.Button(self.master, text="Новая игра", font=("Arial", 14), command=self.new_game)
        self.new_game_button.pack(side='top', pady=10)

        self.player_mode_button = tk.Radiobutton(self.master, text="Против игрока", font=("Arial", 14),
                                                 variable=self.game_mode, value="player")
        self.player_mode_button.pack(side='left', padx=10)
        self.computer_mode_button = tk.Radiobutton(self.master, text="Против компьютера", font=("Arial", 14),
                                                   variable=self.game_mode, value="computer")
        self.computer_mode_button.pack(side='left', padx=10)

    def on_button_click(self, i: int, j: int) -> None:
        if self.board[i][j] == "" and not self.check_winner():
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player, state="disabled",
                                      disabledforeground="black", highlightbackground="yellow")
            if self.check_winner():
                self.show_winner()
            elif self.check_draw():
                self.show_draw()
            else:
                self.switch_player()
                if self.game_mode.get() == "computer" and self.current_player == "O":
                    self.computer_move()

    def switch_player(self) -> None:
        self.current_player = "X" if self.current_player == "O" else "O"

    def check_winner(self) -> bool:

        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True

        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != "":
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_draw(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    return False
        return True

    def show_winner(self) -> None:
        winner = self.current_player
        tk.messagebox.showinfo("Победа!", f"Игрок {winner} победил!")
        self.new_game()

    def show_draw(self) -> None:
        tk.messagebox.showinfo("Ничья!", "Ничья!")
        self.new_game()

    @staticmethod
    def show_info() -> None:
        tk.messagebox.showinfo("ВНИМАНИЕ", "Если вы уже начали игру ,а затем захотели сменить режим, "
                                           "выполните следующие действия:\n 1.Нажмите на кнопку с соответствующим режимом.\n "
                                           "2.Нажмите на кнопку Новая игра")

    def new_game(self) -> None:
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal")

    def minimax(self, depth: int, is_maximizing: bool) -> float:
        if self.check_winner():
            if is_maximizing:
                return -1
            else:
                return 1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ""
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ""
                        best_score = min(best_score, score)
            return best_score

    def computer_move(self) -> None:

        best_score = -float("inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(0, False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        i, j = best_move
        self.board[i][j] = "O"
        self.buttons[i][j].config(text="O", state="disabled",
                                  disabledforeground="black", highlightbackground="yellow")
        if self.check_winner():
            self.show_winner()
        elif self.check_draw():
            self.show_draw()
        else:
            self.switch_player()


if __name__ == '__main__':
    root = tk.Tk()
    game = Game(root)
    root.mainloop()