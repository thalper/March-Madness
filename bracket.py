import tkinter
from PIL import Image, ImageDraw, ImageFont

# https://github.com/JonathanZwiebel/bracket-generator
root = tkinter.Tk()
bracketLoc = {}
finalTwo = 0
boxKey = 0
HEIGHT = 625  # root.winfo_screenheight()
WIDTH = 1250  # root.winfo_screenwidth()
HORIZONTAL_PADDING = 70
GAME_BOX_WIDTH_HEIGHT_RATIO = 3

def computeAccuracy():
    BracketFile = open("Simulations/2021output.txt", 'r')
    CorrectBracket = open("Previous/bracket19.txt", 'r')
    bList = []
    cList = []
    for i in BracketFile:
        bList.append(i)
    for j in CorrectBracket:
        cList.append(j)
    correct = 0
    for i in range(len(bList)):
        if bList[i] == cList[i]:
           # print(i)
            correct += 1
    print("Accuracy:", (correct - 60) / 67 * 100, "%")
    BracketFile.close()
    CorrectBracket.close()
    if (correct - 60) / 67 * 100 > 70:
        return True
    return False

def addXY(team):
    # CHANGE FOR TEAM NAMES NOW
    # BOXKEY SHOULD BE TEAM NAMES
    if finalTwo == 1:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16 - 2 - 80
    elif finalTwo == 2:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16 + 2 + 76
    else:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16
    bracketLoc[team] = [xValue, yValue]
    canvas.create_text(bracketLoc[team][0], bracketLoc[team][1], text=team, fill="black", font=('Helvetica 5 bold'))
    draw.text((bracketLoc[team][0] - 20, bracketLoc[team][1] - 2), text=team, fill="black", font=ImageFont.truetype("arial.ttf", 7), align= "center")

if __name__ == "__main__":
    _size = 5
    _columns = _size * 2 + 1
    _column_width = WIDTH / _columns
    _game_box_width = _column_width - HORIZONTAL_PADDING
    _game_box_height = _game_box_width / GAME_BOX_WIDTH_HEIGHT_RATIO

    BracketFile = open("Simulations/2021output.txt", 'r')
    output = BracketFile.read().split("\n")
    BracketFile.close()
    computeAccuracy()
    canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    image1 = Image.new("RGB", (WIDTH, HEIGHT), 'white')
    draw = ImageDraw.Draw(image1)
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
            draw.rectangle([x_center - _game_box_width / 2, y_center - _game_box_height / 2, x_center + _game_box_width / 2, y_center + _game_box_height / 2], outline = 'black')
            if i == 5:
                #left final two
                finalTwo += 1
                canvas.create_rectangle(x_center - _game_box_width / 2, y_center - _game_box_height / 2 - 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 - 80)
                draw.rectangle([x_center - _game_box_width / 2, y_center - _game_box_height / 2 - 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 - 80], outline='black')
                addXY(output[62])
                #champion
                finalTwo -= 1
                addXY(output[63])
                #right final two
                finalTwo += 2
                canvas.create_rectangle(x_center - _game_box_width / 2, y_center - _game_box_height / 2 + 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 + 80)
                draw.rectangle([x_center - _game_box_width / 2, y_center - _game_box_height / 2 + 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 + 80], outline='black')
                addXY(output[64])
                boxKey += 3
                finalTwo -= 2
            if i <= 10: #creates dictionary of x, y coords on the bracket L to R, top to bottom
                if i != 5:
                    addXY(output[boxKey])
                    boxKey += 1
            #horizontal lines right of rectangles
            if i != _columns - 1:
                if i == 5:
                    canvas.create_line(x_center - _game_box_width / 2 + 2 * _game_box_width - 8, y_center + 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2 + 2 * _game_box_width - 8, y_center + 80)
                    draw.line([x_center - _game_box_width / 2 + 2 * _game_box_width - 8, y_center + 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2 + 2 * _game_box_width - 8, y_center + 80], 'black')
                else:
                    canvas.create_line(x_center + _game_box_width / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center)
                    draw.line([x_center + _game_box_width / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center], 'black')
            # horizontal lines left of rectangles
            if i != 0:
                if i == 5:
                    canvas.create_line(x_center - _game_box_width / 2, y_center - 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - 80)
                    draw.line([x_center - _game_box_width / 2, y_center - 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - 80], 'black')
                else:
                    canvas.create_line(x_center - _game_box_width / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center)
                    draw.line([x_center - _game_box_width / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center], 'black')
            #vertical lines
            if j % 2 == 1:
                if side == "LEFT":
                    canvas.create_line(x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center - y_size)
                    draw.line([x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center - y_size], 'black')
                if side == "RIGHT":
                    canvas.create_line(x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - y_size)
                    draw.line([x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - y_size], 'black')
    filename = "myBracket.jpg"
    image1.save(filename)
    tkinter.mainloop()