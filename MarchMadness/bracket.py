#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
from importlib_resources import files
import MarchMadness.Previous
import MarchMadness.Simulations
import MarchMadness.Brackets

# https://github.com/JonathanZwiebel/bracket-generator

bracketLoc = {}
finalTwo = [0]
boxKey = [0]
HEIGHT = 1250
WIDTH = 2500
HORIZONTAL_PADDING = 50
GAME_BOX_WIDTH_HEIGHT_RATIO = 5

# finds the accuracy of the bracket in comparison to a correctly filled-out bracket from that year
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
            correct += 1
    BracketFile.close()
    CorrectBracket.close()
    return (correct - 60) / 67 * 100

# finds the score of the bracket using the scoring method found on ESPN.com
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
    for i in range(16): # round of 32
        if bList[i] == cList[i]:
            score += 10
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 10
    for i in range(16,24): # sweet 16
        if bList[i] == cList[i]:
            score += 20
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 20
    for i in range(24,28): # elite 8
        if bList[i] == cList[i]:
            score += 40
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 40
    for i in range(28,30): # final 4
        if bList[i] == cList[i]:
            score += 80
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 80
    for i in range(30,31): # championship game
        if bList[i] == cList[i]:
            score += 160
        if bList[-(1+i)] == cList[-(1+i)]:
            score += 160
    if bList[31] == cList[31]: # champion
        score += 320
    return score

# adds team names to the bracket .jpg output
def addXYJPG(team, x_center, y_center, _game_box_width, _game_box_height, draw):
    # left final two team coords
    if finalTwo[0] == 1:
        xValue = x_center - _game_box_width / 16 - 50
        yValue = y_center - _game_box_height / 16 - 2 - 80
    # right final two team coords
    elif finalTwo[0] == 2:
        xValue = x_center - _game_box_width / 16 - 50
        yValue = y_center - _game_box_height / 16 + 2 + 76
    # every other box coords
    else:
        xValue = x_center - _game_box_width / 16 - 50
        yValue = y_center - _game_box_height / 16 - 2
    bracketLoc[team] = [xValue, yValue]
    draw.text((bracketLoc[team][0] - 20, bracketLoc[team][1] - 2), text=team, fill="black", font = ImageFont.truetype(font=str(files(MarchMadness.Previous).joinpath("DejaVuSerif-Bold.ttf")), size=20, index=0, encoding='', layout_engine=None), align= "center")

# creates the bracket .jpg output
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
            draw.rectangle([x_center - _game_box_width / 2, y_center - _game_box_height / 2, x_center + _game_box_width / 2, y_center + _game_box_height / 2], outline = 'black')
            if i == 5:
                #final two left team
                finalTwo[0] += 1
                draw.rectangle([x_center - _game_box_width / 2, y_center - _game_box_height / 2 - 80, x_center + _game_box_width / 2, y_center + _game_box_height / 2 - 80], outline='black')
                addXYJPG(output[62], x_center, y_center, _game_box_width, _game_box_height, draw)
                #champion
                finalTwo[0] -= 1
                addXYJPG(output[63], x_center, y_center, _game_box_width, _game_box_height, draw)
                draw.text((WIDTH / 2 - 35, HEIGHT / 2 + 30), text=str(outputScore[0]) + "-" + str(outputScore[1]), fill="black", font = ImageFont.truetype(font=str(files(MarchMadness.Previous).joinpath("DejaVuSerif-Bold.ttf")), size=20, index=0, encoding='', layout_engine=None), align= "center")
                #final two right team
                finalTwo[0] += 2
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
                if i == 5: # for the little line to the right of the final two right team
                    draw.line([x_center - _game_box_width / 2 + 2 * _game_box_width - 150, y_center + 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2 + 2 * _game_box_width - 150, y_center + 80], 'black')
                else:
                    draw.line([x_center + _game_box_width / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center], 'black')
            # horizontal lines left of rectangles
            if i != 0:
                if i == 5: # for the little line to the left of the final two left team
                    draw.line([x_center - _game_box_width / 2, y_center - 80, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - 80], 'black')
                else:
                    draw.line([x_center - _game_box_width / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center], 'black')
            #vertical lines
            if j % 2 == 1:
                if side == "LEFT":
                    draw.line([x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center, x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center - y_size], 'black')
                if side == "RIGHT":
                    draw.line([x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center, x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center - y_size], 'black')
    # saves final .jpg output
    image1.save(JPGOutStr)