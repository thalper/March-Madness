import tkinter
from PIL import Image, ImageDraw, ImageFont
from importlib_resources import files
import MarchMadness.Previous
import MarchMadness.Simulations
import MarchMadness.Brackets
import MarchMadness.Simulate as Simulate


# https://github.com/JonathanZwiebel/bracket-generator

bracketLoc = {}
finalTwo = [0]
boxKey = [0]
HEIGHT = 625  # root.winfo_screenheight()
WIDTH = 1250  # root.winfo_screenwidth()
HORIZONTAL_PADDING = 70
GAME_BOX_WIDTH_HEIGHT_RATIO = 3

def computeAccuracy(year):
    BracketFileStr = files(MarchMadness.Simulations).joinpath(str(year)+"output.txt")
    CorrectBracketStr = files(MarchMadness.Previous).joinpath("bracket"+str(year%2000)+".txt")
    BracketFile = open(BracketFileStr, "r")
    CorrectBracket = open(CorrectBracketStr, "r")
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
    #print("Accuracy:", (correct - 60) / 67 * 100, "%", (correct - 60))
    BracketFile.close()
    CorrectBracket.close()
    return (correct - 60) / 67 * 100
    if (correct - 60) / 67 * 100 > 70:
        return True
    return False

def computeScore(year):
    BracketFileStr = files(MarchMadness.Simulations).joinpath(str(year)+"output.txt")
    CorrectBracketStr = files(MarchMadness.Previous).joinpath("bracket"+str(year%2000)+".txt")
    BracketFile = open(BracketFileStr, "r")
    CorrectBracket = open(CorrectBracketStr, "r")
    bList = []
    cList = []
    for i in BracketFile:
        bList.append(i)
    for j in CorrectBracket:
        cList.append(j)
    BracketFile.close()
    CorrectBracket.close()
    bList = bList[32:95]
    cList = cList[32:95]
    score = 0
    for i in range(16): # round of 32 correct
        if bList[i] == cList[i]:
            score += 10
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 10
    for i in range(16,24): # sweet 16 correct
        if bList[i] == cList[i]:
            score += 20
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 20
    for i in range(24,28): # elite 8 correct
        if bList[i] == cList[i]:
            score += 40
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 40
    for i in range(28,30): # final 4 correct
        if bList[i] == cList[i]:
            score += 80
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 80
    for i in range(30,31): # championship game correct
        if bList[i] == cList[i]:
            score += 160
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 160
    if bList[31] == cList[31]: # champion correct
        score += 320

    return score
    
    

def addXY(team, x_center, y_center, _game_box_width, _game_box_height, canvas, draw):
    # CHANGE FOR TEAM NAMES NOW
    # BOXKEY[0] SHOULD BE TEAM NAMES
    if finalTwo[0] == 1:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16 - 2 - 80
    elif finalTwo[0] == 2:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16 + 2 + 76
    else:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16
    bracketLoc[team] = [xValue, yValue]
    # # canvas.create_text(bracketLoc[team][0], bracketLoc[team][1], text=team, fill="black", font=('Helvetica 5 bold'))
    # canvas.create_text(bracketLoc[team][0], bracketLoc[team][1], text=team, fill="black", font = ImageFont.load_default())
    # draw.text((bracketLoc[team][0] - 20, bracketLoc[team][1] - 2), text=team, fill="black", font=ImageFont.truetype("arial.ttf", 7), align= "center")
    draw.text((bracketLoc[team][0] - 20, bracketLoc[team][1] - 2), text=team, fill="black", font = ImageFont.load_default(), align= "center")

def addXYJPG(team, x_center, y_center, _game_box_width, _game_box_height, draw):
    # CHANGE FOR TEAM NAMES NOW
    # BOXKEY[0] SHOULD BE TEAM NAMES
    if finalTwo[0] == 1:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16 - 2 - 80
    elif finalTwo[0] == 2:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16 + 2 + 76
    else:
        xValue = x_center - _game_box_width / 16 + 2
        yValue = y_center - _game_box_height / 16
    bracketLoc[team] = [xValue, yValue]
    # draw.text((bracketLoc[team][0] - 20, bracketLoc[team][1] - 2), text=team, fill="black", font=ImageFont.truetype("arial.ttf", 7), align= "center")
    draw.text((bracketLoc[team][0] - 20, bracketLoc[team][1] - 2), text=team, fill="black", font = ImageFont.load_default(), align= "center")


def buildBracketJPG(BracketFileStr, ScoreFileStr, JPGOutStr):
    boxKey = [0]
    _size = 5
    _columns = _size * 2 + 1
    _column_width = WIDTH / _columns
    _game_box_width = _column_width - HORIZONTAL_PADDING
    _game_box_height = _game_box_width / GAME_BOX_WIDTH_HEIGHT_RATIO

    BracketFile = open(BracketFileStr, 'r')
    output = BracketFile.read().split("\n")
    BracketFile.close()
    ScoreFile = open(ScoreFileStr, 'r')
    outputScore = ScoreFile.read().split("\n")
    ScoreFile.close()
    #computeAccuracy()
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
            #canvas.create_rectangle(x_center - _game_box_width / 2, y_center - _game_box_height / 2, x_center + _game_box_width / 2, y_center + _game_box_height / 2)
            draw.rectangle([x_center - _game_box_width / 2, y_center - _game_box_height / 2, x_center + _game_box_width / 2, y_center + _game_box_height / 2], outline = 'black')
            if i == 5:
                #left final two
                finalTwo[0] += 1
                #canvas.create_rectangle(x_center - _game_box_width / 2, y_center - _game_box_height / 2 - 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 - 80)
                draw.rectangle([x_center - _game_box_width / 2, y_center - _game_box_height / 2 - 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 - 80], outline='black')
                addXYJPG(output[62], x_center, y_center, _game_box_width, _game_box_height, draw)
                #champion
                finalTwo[0] -= 1
                addXYJPG(output[63], x_center, y_center, _game_box_width, _game_box_height, draw)
                #canvas.create_text(WIDTH / 2, HEIGHT / 2 + 30, text=str(outputScore[0]) + "-" + str(outputScore[1]), fill="black", font=('Helvetica 10 bold'))
                # draw.text((WIDTH / 2 - 15, HEIGHT / 2 + 30), text=str(outputScore[0]) + "-" + str(outputScore[1]), fill="black", font=ImageFont.truetype("arial.ttf", 12), align= "center")
                draw.text((WIDTH / 2 - 15, HEIGHT / 2 + 30), text=str(outputScore[0]) + "-" + str(outputScore[1]), fill="black", font = ImageFont.load_default(), align= "center")
                #right final two
                finalTwo[0] += 2
                #canvas.create_rectangle(x_center - _game_box_width / 2, y_center - _game_box_height / 2 + 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 + 80)
                draw.rectangle([x_center - _game_box_width / 2, y_center - _game_box_height / 2 + 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 + 80], outline='black')
                addXYJPG(output[64], x_center, y_center, _game_box_width, _game_box_height, draw)
                boxKey[0] += 3
                finalTwo[0] -= 2
            if i <= 10: #creates dictionary of x, y coords on the bracket L to R, top to bottom
                if i != 5:
                    addXYJPG(output[boxKey[0]], x_center, y_center, _game_box_width, _game_box_height, draw)
                    boxKey[0] += 1
            #horizontal lines right of rectangles
            if i != _columns - 1:
                if i == 5:
                    #canvas.create_line(x_center - _game_box_width / 2 + 2 * _game_box_width - 8, y_center + 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2 + 2 * _game_box_width - 8, y_center + 80)
                    draw.line([x_center - _game_box_width / 2 + 2 * _game_box_width - 8, y_center + 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2 + 2 * _game_box_width - 8, y_center + 80], 'black')
                else:
                    #canvas.create_line(x_center + _game_box_width / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center)
                    draw.line([x_center + _game_box_width / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center], 'black')
            # horizontal lines left of rectangles
            if i != 0:
                if i == 5:
                    #canvas.create_line(x_center - _game_box_width / 2, y_center - 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - 80)
                    draw.line([x_center - _game_box_width / 2, y_center - 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - 80], 'black')
                else:
                    #canvas.create_line(x_center - _game_box_width / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center)
                    draw.line([x_center - _game_box_width / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center], 'black')
            #vertical lines
            if j % 2 == 1:
                if side == "LEFT":
                    #canvas.create_line(x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center - y_size)
                    draw.line([x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center - y_size], 'black')
                if side == "RIGHT":
                    #canvas.create_line(x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - y_size)
                    draw.line([x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - y_size], 'black')
    image1.save(JPGOutStr)
    #tkinter.mainloop()

