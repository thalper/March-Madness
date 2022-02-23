import tkinter

# https://github.com/JonathanZwiebel/bracket-generator
root = tkinter.Tk()
bracketLoc = {}
boxKey = 1
HEIGHT = 625  # root.winfo_screenheight()
WIDTH = 1250  # root.winfo_screenwidth()
HORIZONTAL_PADDING = 70
GAME_BOX_WIDTH_HEIGHT_RATIO = 3

def addXY(boxKey):
    # CHANGE FOR TEAM NAMES NOW
    # BOXKEY SHOULD BE TEAM NAMES
    xValue = x_center - _game_box_width / 16
    yValue = y_center - _game_box_height / 16
    bracketLoc[boxKey] = [xValue, yValue]
    canvas.create_text(bracketLoc[boxKey][0], bracketLoc[boxKey][1], text=boxKey, fill="black", font=('Helvetica 5 bold'))

if __name__ == "__main__":
    _size = 5
    _columns = _size * 2 + 1
    _column_width = WIDTH / _columns
    _game_box_width = _column_width - HORIZONTAL_PADDING
    _game_box_height = _game_box_width / GAME_BOX_WIDTH_HEIGHT_RATIO
    canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    for i in range(_columns):
        if i - _size < 0:
            side = "LEFT"
        elif i - _size > 0:
            side = "RIGHT"
        else:
            side = "CENTER"
        games = 2 ** abs(i - _size)
        x_center = _column_width * (i + 0.5)
        y_size = HEIGHT / games
        for j in range(games):
            y_center = y_size * (j + 0.5)
            canvas.create_rectangle(x_center - _game_box_width / 2, y_center - _game_box_height / 2, x_center + _game_box_width / 2, y_center + _game_box_height / 2)
            if i <= 10: #creates dictionary of x, y coords on the bracket L to R, top to bottom
                addXY(boxKey)
                boxKey += 1
            if i != _columns - 1:
                canvas.create_line(x_center + _game_box_width / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center)
            if i != 0:
                canvas.create_line(x_center - _game_box_width / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center)

            if j % 2 == 1:
                if side == "LEFT":
                    canvas.create_line(x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center - y_size)
                if side == "RIGHT":
                    canvas.create_line(x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - y_size)

    tkinter.mainloop()