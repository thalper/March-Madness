# https://github.com/JonathanZwiebel/bracket-generator
bracketLoc = {}
boxKey = 1
HEIGHT = 625  # root.winfo_screenheight()
WIDTH = 1250  # root.winfo_screenwidth()
HORIZONTAL_PADDING = 70
GAME_BOX_WIDTH_HEIGHT_RATIO = 3

def addXY(boxKey):
    xValue = x_center - _game_box_width / 16
    yValue = y_center - _game_box_height / 16
    bracketLoc[boxKey] = [xValue, yValue]

if __name__ == "__main__":
    _size = 5
    _columns = _size * 2 + 1
    _column_width = WIDTH / _columns
    _game_box_width = _column_width - HORIZONTAL_PADDING
    _game_box_height = _game_box_width / GAME_BOX_WIDTH_HEIGHT_RATIO

    for i in range(_columns):
        games = 2 ** abs(i - _size)
        x_center = _column_width * (i + 0.5)
        y_size = HEIGHT / games
        for j in range(games):
            y_center = y_size * (j + 0.5)
            if i <= 10: #creates dictionary of x, y coords on the bracket L to R, top to bottom
                addXY(boxKey)
                boxKey += 1