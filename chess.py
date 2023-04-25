havestockfish = True

import pygame
import cairosvg
import io
import os
from testboard import testboards
try:
  from stockfish import Stockfish
except(ModuleNotFoundError):
  print("Stockfish module not found.")
  havestockfish = False
from random import randint
from collections import Counter
from stockfishpath import thepath

def movetonumber(move, p=None): #converts the notation to numbers for code to use
    if p == True:
        number = (8 - int(move[-3])) * 8 + squares[move[-4]]
    else:
        number = (8 - int(move[-1])) * 8 + squares[move[-2]]
    return number


def tostring(number): #converts the numbers back to notations
    string = list(squares.keys())[list(squares.values()).index(
        number % 8)]+str(7-int(number/8)+1)
    return string


def configboard(board): #configurates the 64 length list to a 8 by 8 list of lists
    tempboard = []
    for i in range(0, 8):
        row = []
        for piece in range(0, 8):
            pieceappend = piece + i * 8
            row.append(board[pieceappend])
        tempboard.append(row)
    return(tempboard)


def printboard(board): #prints the board
    print("[' ']['a ', 'b ', 'c ', 'd ', 'e ', 'f ', 'g ', 'h ']")
    i = 8
    for a in configboard(board):
        b = "['" + str(i) + "']"
        print(f"{b}{a}")
        i -= 1


allking = []


def check(turn, move=None): #check if the king is in check
    if move != None:
        kinglocation = move
    else:
        try:
            kinglocation = gameboard.index(turn+'K')
            allking.append(kinglocation)
        except(ValueError):
            gameboard[allking[-2]] = turn+'K'
            kinglocation = gameboard.index(turn+'K')
    if turn == 'w':
        opp = 'b'
    else:
        opp = 'w'
    if kinglocation % 8 - 1 > -1:
        if kinglocation - 9 > -1:
            if gameboard[kinglocation - 9] == opp + 'K':
                return True
            if gameboard[kinglocation - 9] == 'bP' and turn == 'w':
                return True
        if kinglocation + 7 < 64:
            if gameboard[kinglocation + 7] == opp + 'K':
                return True
            if gameboard[kinglocation + 7] == 'wP' and turn == 'b':
                return True
    if kinglocation % 8 + 1 < 8:
        if kinglocation + 9 < 64:
            if gameboard[kinglocation + 9] == opp + 'K':
                return True
            if gameboard[kinglocation + 9] == 'wP' and turn == 'b':
                return True
        if kinglocation - 7 > -1:
            if gameboard[kinglocation - 7] == opp + 'K':
                return True
            if gameboard[kinglocation - 7] == 'bP' and turn == 'w':
                return True
    if kinglocation - 8 > -1:
        if gameboard[kinglocation - 8] == opp + 'K':
            return True
    if kinglocation + 8 < 64:
        if gameboard[kinglocation + 8] == opp + 'K':
            return True
    i = 1
    while kinglocation - 8 * i > -1:
        if gameboard[kinglocation - 8 * i] == opp + 'R' or gameboard[kinglocation - 8 * i] == opp + 'Q':
            return True
        elif gameboard[kinglocation - 8 * i] != '  ' and gameboard[kinglocation - 8 * i] != turn + 'K':
            break
        else:
            i += 1
    i = 1
    while kinglocation + 8 * i < 64:
        if gameboard[kinglocation + 8 * i] == opp + 'R' or gameboard[kinglocation + 8 * i] == opp + 'Q':
            return True
        elif gameboard[kinglocation + 8 * i] != '  ' and gameboard[kinglocation + 8 * i] != turn + 'K':
            break
        else:
            i += 1
    i = 1
    while kinglocation % 8 - i > -1:
        if gameboard[kinglocation - i] == opp + 'R' or gameboard[kinglocation - i] == opp + 'Q':
            return True
        elif gameboard[kinglocation - i] != '  ' and gameboard[kinglocation - i] != turn + 'K':
            break
        else:
            i += 1
    i = 1
    while kinglocation % 8 + i < 8:
        if gameboard[kinglocation + i] == opp + 'R' or gameboard[kinglocation + i] == opp + 'Q':
            return True
        elif gameboard[kinglocation + i] != '  ' and gameboard[kinglocation + i] != turn + 'K':
            break
        else:
            i += 1
    i = 1
    while kinglocation - 9 * i > -1 and kinglocation % 8 - i > -1:
        if gameboard[kinglocation - 9 * i] == opp + 'B' or gameboard[kinglocation - 9 * i] == opp + 'Q':
            return True
        elif gameboard[kinglocation - 9 * i] != '  ' and gameboard[kinglocation - 9 * i] != turn + 'K':
            break
        else:
            i += 1
    i = 1
    while kinglocation - 7 * i > -1 and kinglocation % 8 + i < 8:
        if gameboard[kinglocation - 7 * i] == opp + 'B' or gameboard[kinglocation - 7 * i] == opp + 'Q':
            return True
        elif gameboard[kinglocation - 7 * i] != '  ' and gameboard[kinglocation - 7 * i] != turn + 'K':
            break
        else:
            i += 1
    i = 1
    while kinglocation + 7 * i < 64 and kinglocation % 8 - i > -1:
        if gameboard[kinglocation + 7 * i] == opp + 'B' or gameboard[kinglocation + 7 * i] == opp + 'Q':
            return True
        elif gameboard[kinglocation + 7 * i] != '  ' and gameboard[kinglocation + 7 * i] != turn + 'K':
            break
        else:
            i += 1
    i = 1
    while kinglocation + 9 * i < 64 and kinglocation % 8 + i < 8:
        if gameboard[kinglocation + 9 * i] == opp + 'B' or gameboard[kinglocation + 9 * i] == opp + 'Q':
            return True
        elif gameboard[kinglocation + 9 * i] != '  ' and gameboard[kinglocation + 9 * i] != turn + 'K':
            break
        else:
            i += 1
    if kinglocation - 17 > -1 and kinglocation % 8 - 1 > -1:
        if gameboard[kinglocation - 17] == opp + 'N':
            return True
    if kinglocation - 15 > -1 and kinglocation % 8 + 1 < 8:
        if gameboard[kinglocation - 15] == opp + 'N':
            return True
    if kinglocation - 10 > -1 and kinglocation % 8 - 2 > -1:
        if gameboard[kinglocation - 10] == opp + 'N':
            return True
    if kinglocation - 6 > -1 and kinglocation % 8 + 2 < 8:
        if gameboard[kinglocation - 6] == opp + 'N':
            return True
    if kinglocation + 6 < 64 and kinglocation % 8 - 2 > -1:
        if gameboard[kinglocation + 6] == opp + 'N':
            return True
    if kinglocation + 10 < 64 and kinglocation % 8 + 2 < 8:
        if gameboard[kinglocation + 10] == opp + 'N':
            return True
    if kinglocation + 15 < 64 and kinglocation % 8 - 1 > -1:
        if gameboard[kinglocation + 15] == opp + 'N':
            return True
    if kinglocation + 17 < 64 and kinglocation % 8 + 1 < 8:
        if gameboard[kinglocation + 17] == opp + 'N':
            return True
    return False


def checkmate(turn): #checks for checkmate or stalemate
    for pieces in ['', 'R', 'K', 'Q', 'B', 'N']:
        for i in range(64):
            if getmove(pieces + tostring(i), turn, True):
                return False
    if check(turn):
        return 'checkmate'
    return 'stalemate'


allboards = []
pawnpos = []
numpieces = []
strboards = []


def draw(): #checks for draws
    numpieces.append(gameboard.count('  '))
    pawninboard = []
    allboards.append(gameboard)
    strboards.append(str(gameboard))
    for i in range(0, 64):
        if 'P' in gameboard[i]:
            pawninboard.append(i)
    pawnpos.append(pawninboard)
    if strboards.count(str(gameboard)) == 3:
        return 'Threefold Repetition'
    if allboards[-1].count('wR') == 0 and allboards[-1].count('bR') == 0:
        if allboards[-1].count('wQ') == 0 and allboards[-1].count('bQ') == 0:
            if allboards[-1].count('wP') == 0 and allboards[-1].count('bP') == 0:
                if allboards[-1].count('wB') == 0 and allboards[-1].count('bB') == 0:
                    if allboards[-1].count('wN') == 0 and allboards[-1].count('bN') == 0:
                        return 'Insufficient Material'
                    elif allboards[-1].count('wN') + allboards[-1].count('bN') == 1:
                        return 'Insufficient Material'
                    elif allboards[-1].count('wN') == 2 and allboards[-1].count('bN') == 0:
                        return 'Insufficient Material'
                    elif allboards[-1].count('bN') == 2 and allboards[-1].count('wN') == 0:
                        return 'Insufficient Material'
                elif allboards[-1].count('wB') + allboards[-1].count('bB') == 1:
                    return 'Insufficient Material'
                elif allboards[-1].count('wB') == 1 and allboards[-1].count('bB') == 1:
                    if allboards[-1].index('wB') % 2 == allboards[-1].index(bB) % 2:
                        return 'Insufficient Material'
    if len(pawnpos) >= 100:
        for i in range(1, 50):
            if not pawnpos[i] == pawnpos[-1]:
                return False
            if not numpieces[i] == numpieces[-1]:
                return False
        return '50 Move Rule'
    return False


def checkorigin(move, mtype, turn, origin): #checks if a piece can move to the specified squared
    if mtype == 'pawn':
        if turn == 'w':
            try:
                if gameboard[move + 8] == 'wP':
                    return(move + 8)
                elif (gameboard[move % 8 + 48] == 'wP' and gameboard[move + 2 * 8] == 'wP') and move % 8 + 48 == move + 2 * 8 and gameboard[move + 8] == '  ':
                    return(move + 2 * 8)
                else:
                    return False
            except(IndexError):
                return False
        if turn == 'b':
            try:
                if gameboard[move - 8] == 'bP':
                    return(move - 8)
                elif (gameboard[move % 8 + 8] == 'bP' and gameboard[move - 2 * 8] == 'bP') and move % 8 + 8 == move - 2 * 8 and gameboard[move - 8] == '  ':
                    return(move - 2 * 8)
                else:
                    return False
            except(IndexError):
                return False
    elif mtype == 'pawncap':
        if turn == 'w':
            if squares[origin] < move % 8:
                if gameboard[move + 7] == 'wP':
                    return(move + 7)
            elif squares[origin] > move % 8:
                if gameboard[move + 9] == 'wP':
                    return(move + 9)
            else:
                return False
            return False
        if turn == 'b':
            if squares[origin] < move % 8:
                if gameboard[move - 9] == 'bP':
                    return(move - 9)
            elif squares[origin] > move % 8:
                if gameboard[move - 7] == 'bP':
                    return(move - 7)
            else:
                return False
            return False
    elif mtype == 'N':
        n = []
        if move % 8 - 2 > -1:
            if move - 10 > -1:
                if gameboard[move - 10] == turn + 'N':
                    n.append(move - 10)
            if move + 6 < 64:
                if gameboard[move + 6] == turn + 'N':
                    n.append(move + 6)
        if move % 8 - 1 > -1:
            if move - 17 > -1:
                if gameboard[move - 17] == turn + 'N':
                    n.append(move - 17)
            if move + 15 < 64:
                if gameboard[move + 15] == turn + 'N':
                    n.append(move + 15)
        if move % 8 + 1 < 8:
            if move - 15 > -1:
                if gameboard[move - 15] == turn + 'N':
                    n.append(move - 15)
            if move + 17 < 64:
                if gameboard[move + 17] == turn + 'N':
                    n.append(move + 17)
        if move % 8 + 2 < 8:
            if move - 6 > -1:
                if gameboard[move - 6] == turn + 'N':
                    n.append(move - 6)
            if move + 10 < 64:
                if gameboard[move + 10] == turn + 'N':
                    n.append(move + 10)
        if len(n) > 0:
            return n
        else:
            return False
    elif mtype == 'B':
        b = []
        i = 1
        while move % 8 - i > -1 and move - 9 * i > -1:
            if gameboard[move - 9 * i] != '  ':
                if gameboard[move - 9 * i] == turn + 'B':
                    b.append(move - 9 * i)
                break
            else:
                i += 1
        i = 1
        while move % 8 + i < 8 and move - 7 * i > -1:
            if gameboard[move - 7 * i] != '  ':
                if gameboard[move - 7 * i] == turn + 'B':
                    b.append(move - 7 * i)
                break
            else:
                i += 1
        i = 1
        while move % 8 - i > -1 and move + 7 * i < 64:
            if gameboard[move + 7 * i] != '  ':
                if gameboard[move + 7 * i] == turn + 'B':
                    b.append(move + 7 * i)
                break
            else:
                i += 1
        i = 1
        while move % 8 + i < 8 and move + 9 * i < 64:
            if gameboard[move + 9 * i] != '  ':
                if gameboard[move + 9 * i] == turn + 'B':
                    b.append(move + 9 * i)
                break
            else:
                i += 1
        if len(b) > 0:
            return b
        return False
    elif mtype == 'R':
        r = []
        i = 1
        while move - 8 * i > -1:
            if gameboard[move - 8 * i] != '  ':
                if gameboard[move - 8 * i] == turn + 'R':
                    r.append(move - 8 * i)
                break
            else:
                i += 1
        i = 1
        while move + 8 * i < 64:
            if gameboard[move + 8 * i] != '  ':
                if gameboard[move + 8 * i] == turn + 'R':
                    r.append(move + 8 * i)
                break
            else:
                i += 1
        i = 1
        while move % 8 - i > -1:
            if gameboard[move - i] != '  ':
                if gameboard[move - i] == turn + 'R':
                    r.append(move - i)
                break
            else:
                i += 1
        i = 1
        while move % 8 + i < 8:
            if gameboard[move + i] != '  ':
                if gameboard[move + i] == turn + 'R':
                    r.append(move + i)
                break
            else:
                i += 1
        if len(r) > 0:
            return r
        return False
    elif mtype == 'Q':
        q = []
        i = 1
        while move % 8 - i > -1 and move - 9 * i > -1:
            if gameboard[move - 9 * i] != '  ':
                if gameboard[move - 9 * i] == turn + 'Q':
                    q.append(move - 9 * i)
                break
            else:
                i += 1
        i = 1
        while move % 8 + i < 8 and move - 7 * i > -1:
            if gameboard[move - 7 * i] != '  ':
                if gameboard[move - 7 * i] == turn + 'Q':
                    q.append(move - 7 * i)
                break
            else:
                i += 1
        i = 1
        while move % 8 - i > -1 and move + 7 * i < 64:
            if gameboard[move + 7 * i] != '  ':
                if gameboard[move + 7 * i] == turn + 'Q':
                    q.append(move + 7 * i)
                break
            else:
                i += 1
        i = 1
        while move % 8 + i < 8 and move + 9 * i < 64:
            if gameboard[move + 9 * i] != '  ':
                if gameboard[move + 9 * i] == turn + 'Q':
                    q.append(move + 9 * i)
                break
            else:
                i += 1
        i = 1
        while move - 8 * i > -1:
            if gameboard[move - 8 * i] != '  ':
                if gameboard[move - 8 * i] == turn + 'Q':
                    q.append(move - 8 * i)
                break
            else:
                i += 1
        i = 1
        while move + 8 * i < 64:
            if gameboard[move + 8 * i] != '  ':
                if gameboard[move + 8 * i] == turn + 'Q':
                    q.append(move + 8 * i)
                break
            else:
                i += 1
        i = 1
        while move % 8 - i > -1:
            if gameboard[move - i] != '  ':
                if gameboard[move - i] == turn + 'Q':
                    q.append(move - i)
                break
            else:
                i += 1
        i = 1
        while move % 8 + i < 8:
            if gameboard[move + i] != '  ':
                if gameboard[move + i] == turn + 'Q':
                    q.append(move + i)
                break
            else:
                i += 1
        if len(q) > 0:
            return q
        else:
            return False
    elif mtype == 'K':
        if move % 8 - 1 > -1:
            if move - 9 > -1:
                if gameboard[move - 9] == turn + 'K':
                    return(move - 9)
            if move - 1 > -1:
                if gameboard[move - 1] == turn + 'K':
                    return(move - 1)
            if move + 7 < 64:
                if gameboard[move + 7] == turn + 'K':
                    return(move + 7)
        if move - 8 > -1:
            if gameboard[move - 8] == turn + 'K':
                return(move - 8)
        if move + 8 < 64:
            if gameboard[move + 8] == turn + 'K':
                return(move + 8)
        if move % 8 + 1 < 8:
            if move - 7 > -1:
                if gameboard[move - 7] == turn + 'K':
                    return(move - 7)
            if move + 1 < 64:
                if gameboard[move + 1] == turn + 'K':
                    return(move + 1)
            if move + 9 < 64:
                if gameboard[move + 9] == turn + 'K':
                    return(move + 9)
        return False


moves = []


def getmove(move, turn, checked=None):
    mtype = ''
    temp = ''
    tempno = 0
    tempstring = ''
    moved = False
    theorigin = ''
    if turn == 'w':
        opp = 'b'
    else:
        opp = 'w'
    if move == 'O-O':
        if turn == 'w':
            for elem in moves:
                if 'e1' in elem or 'h1' in elem:
                    return False
            if gameboard[62] == '  ' and gameboard[61] == '  ':
                if check('w') is False and check('w', 62) is False and check('w', 61) is False:
                    if checked == None:
                        gameboard[63] = '  '
                        gameboard[62] = 'wK'
                        gameboard[61] = 'wR'
                        gameboard[60] = '  '
                        moves.append('e1g1')
                    return True
            return False
        else:
            for elem in moves:
                if 'e8' in elem or 'h8' in elem:
                    return False
            if gameboard[5] == '  ' and gameboard[6] == '  ':
                if check('b') is False and check('b', 5) is False and check('b', 6) is False:
                    if checked == None:
                        gameboard[7] = '  '
                        gameboard[6] = 'bK'
                        gameboard[5] = 'bR'
                        gameboard[4] = '  '
                        moves.append('e8g8')
                    return True
            return False
    elif move == 'O-O-O':
        if turn == 'w':
            for elem in moves:
                if 'e1' in elem or 'a1' in elem:
                    return False
            if gameboard[57] == '  ' and gameboard[58] == '  ' and gameboard[59] == '  ':
                if check('w') is False and check('w', 58) is False and check('w', 59) is False:
                    if checked == None:
                        gameboard[56] = '  '
                        gameboard[58] = 'wK'
                        gameboard[59] = 'wR'
                        gameboard[60] = '  '
                        moves.append('e1c1')
                    return True
        else:
            for elem in moves:
                if 'e8' in elem or 'a8' in elem:
                    return False
            if gameboard[1] == '  ' and gameboard[2] == '  ' and gameboard[3] == '  ':
                if check('b') is False and check('b', 2) is False and check('b', 3) is False:
                    if checked == None:
                        gameboard[0] = '  '
                        gameboard[2] = 'bK'
                        gameboard[3] = 'bR'
                        gameboard[4] = '  '
                        moves.append('e8c8')
                    return True
    else:
        try:
            if '=' in move:
                number = movetonumber(move, True)
            else:
                number = movetonumber(move)
        except(KeyError, ValueError, IndexError):
            return False

    if len(move) == 4:
        if 'x' not in move:
            theorigin = move[1]
    elif len(move) == 5:
        if 'x' not in move:
            theorigin = move[1] + move[2]
        else:
            theorigin = move[1]
    elif len(move) == 6:
        theorigin = move[1] + move[2]

    if move[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        mtype = 'pawn'
    elif move[0] in ['N', 'B', 'R', 'Q', 'K']:
        mtype = move[0]
    if mtype == 'N':
        origins = checkorigin(number, 'N', turn, None)
        if origins is not False:
            if len(theorigin) == 1:
                for ogns in origins:
                    if str(theorigin) in tostring(ogns):
                        theorigin = ogns
                        break
                if len(str(theorigin)) == 2:
                    pass
                else:
                    return False
            elif len(theorigin) == 2:
                theorigin = movetonumber(theorigin)
                if theorigin not in origins:
                    return False
            elif len(origins) == 2:
                if checked == None:
                    if abs(origins[0]-origins[1]) < 8:
                        print("Please specify the file, for example, Nad4")
                    else:
                        print("Please specify the rank, for example, N3d4")
                return False
            elif len(origins) > 2:
                if checked == None:
                    print("Please specify the square, for example, Ne5d3")
                return False
            else:
                theorigin = origins[0]
            temp = gameboard[number]
            gameboard[number] = turn + 'N'
            tempno = theorigin
            gameboard[theorigin] = '  '
            if check(turn):
                gameboard[number] = temp
                gameboard[tempno] = turn + 'N'
                return False
            elif checked == True:
                gameboard[number] = temp
                gameboard[tempno] = turn + 'N'
                return True
            else:
                tempstring = tostring(tempno) + tostring(number)
                moves.append(tempstring)
                return True
        return False
    elif mtype == 'B':
        origins = checkorigin(number, 'B', turn, None)
        if origins is not False:
            if len(theorigin) == 1:
                for ogns in origins:
                    if str(theorigin) in tostring(ogns):
                        theorigin = ogns
                        break
                if len(str(theorigin)) == 2:
                    pass
                else:
                    return False
            elif len(theorigin) == 2:
                theorigin = movetonumber(theorigin)
                if theorigin not in origins:
                    return False
            elif len(origins) == 2:
                if checked == None:
                    if abs(origins[0]-origins[1]) < 8:
                        print("Please specify the file, for example, Bad4")
                    else:
                        print("Please specify the rank, for example, B3d4")
                return False
            elif len(origins) > 2:
                if checked == None:
                    print("Please specify the square, for example, Be5d4")
                return False
            else:
                theorigin = origins[0]
            temp = gameboard[number]
            gameboard[number] = turn + 'B'
            tempno = theorigin
            gameboard[theorigin] = '  '
            if check(turn):
                gameboard[number] = temp
                gameboard[tempno] = turn + 'B'
                return False
            elif checked == True:
                gameboard[number] = temp
                gameboard[tempno] = turn + 'B'
                return True
            else:
                tempstring = tostring(tempno) + tostring(number)
                moves.append(tempstring)
                return True
        return False
    elif mtype == 'R':
        origins = checkorigin(number, 'R', turn, None)
        if origins is not False:
            if len(theorigin) == 1:
                for ogns in origins:
                    if str(theorigin) in tostring(ogns):
                        theorigin = ogns
                        break
                if len(str(theorigin)) == 2:
                    pass
                else:
                    return False
            elif len(theorigin) == 2:
                theorigin = movetonumber(theorigin)
                if theorigin not in origins:
                    return False
            elif len(origins) == 2:
                if checked == None:
                    if abs(origins[0]-origins[1]) < 8:
                        print("Please specify the file, for example, Rad4")
                    else:
                        print("Please specify the rank, for example, R3d4")
                return False
            elif len(origins) > 2:
                if checked == None:
                    print("Please specify the square, for example, Re4d4")
                return False
            else:
                theorigin = origins[0]
            temp = gameboard[number]
            gameboard[number] = turn + 'R'
            tempno = theorigin
            gameboard[theorigin] = '  '
            if check(turn):
                gameboard[number] = temp
                gameboard[tempno] = turn + 'R'
                return False
            elif checked == True:
                gameboard[number] = temp
                gameboard[tempno] = turn + 'R'
                return True
            else:
                tempstring = tostring(tempno) + tostring(number)
                moves.append(tempstring)
                return True
        return False
    elif mtype == 'Q':
        origins = checkorigin(number, 'Q', turn, None)
        if origins is not False:
            if len(theorigin) == 1:
                for ogns in origins:
                    if str(theorigin) in tostring(ogns):
                        theorigin = ogns
                        break
                if len(str(theorigin)) == 2:
                    pass
                else:
                    return False
            elif len(theorigin) == 2:
                theorigin = movetonumber(theorigin)
                if theorigin not in origins:
                    return False
            elif len(origins) == 2:
                if abs(origins[0]-origins[1]) < 8:
                    print("Please specify the file, for example, Qad4")
                else:
                    print("Please specify the rank, for example, Q3d4")
                return False
            elif len(origins) > 2:
                print("Please specify the square, for example, Qe4d4")
                return False
            else:
                theorigin = origins[0]
            temp = gameboard[number]
            gameboard[number] = turn + 'Q'
            tempno = theorigin
            gameboard[theorigin] = '  '
            if check(turn):
                gameboard[number] = temp
                gameboard[tempno] = turn + 'Q'
                return False
            elif checked == True:
                gameboard[number] = temp
                gameboard[tempno] = turn + 'Q'
                return True
            else:
                tempstring = tostring(tempno) + tostring(number)
                moves.append(tempstring)
                return True
        return False
    elif mtype == 'K':
        theorigin = checkorigin(number, 'K', turn, None)
        if not theorigin is False:
            if turn not in gameboard[number]:
                temp = gameboard[number]
                gameboard[number] = turn + 'K'
                tempno = theorigin
                gameboard[theorigin] = '  '
                if check(turn):
                    gameboard[number] = temp
                    gameboard[tempno] = turn + 'K'
                    return False
                elif checked == True:
                    gameboard[number] = temp
                    gameboard[tempno] = turn + 'K'
                    return True
                else:
                    tempstring = tostring(tempno) + tostring(number)
                    moves.append(tempstring)
                    return True
        return False
    elif mtype == 'pawn':
        if '1' in move or '8' in move:
            if '=' in move and move[-1] in ['N', 'B', 'R', 'Q']:
                if 'x' in move:
                    if checkorigin(number, 'pawncap', turn, move[0]):
                        if turn not in gameboard[number] and gameboard[number] != '  ':
                            print('b')
                            temp = gameboard[number]
                            gameboard[number] = turn + move[-1]
                            tempno = checkorigin(
                                number, 'pawncap', turn, move[0])
                            gameboard[checkorigin(
                                number, 'pawncap', turn, move[0])] = '  '
                            if check(turn):
                                gameboard[number] = temp
                                gameboard[tempno] = turn + 'P'
                                return False
                            elif checked == True:
                                gameboard[number] = temp
                                gameboard[tempno] = turn + 'P'
                                return True
                            else:
                                tempstring = tostring(
                                    tempno) + tostring(number) + move[-1].lower()
                                moves.append(tempstring)
                                return True
                        elif gameboard[checkorigin(number, 'pawncap', turn, move[0], None)+1] == opp + 'P':
                            tempno = checkorigin(
                                number, 'pawncap', turn, move[0])+1
                            if moves[-3] == tostring(tempno-16) + tostring(tempno) or moves[-3] == tostring(tempno+16) + tostring(tempno):
                                gameboard[number] = turn + move[-1]
                                gameboard[tempno] = '  '
                                gameboard[tempno-1] = '  '
                                if check(turn):
                                    gameboard[number] = '  '
                                    gameboard[tempno] = opp + 'P'
                                    gameboard[tempno-1] = turn + 'P'
                                    return False
                                elif checked == True:
                                    gameboard[number] = '  '
                                    gameboard[tempno] = opp + 'P'
                                    gameboard[tempno-1] = turn + 'P'
                                    return True
                                else:
                                    tempstring = tostring(
                                        tempno-1) + tostring(number) + move[-1].lower()
                                    moves.append(tempstring)
                                    return True
                        elif gameboard[checkorigin(number, 'pawncap', turn, move[0])-1] == opp + 'P':
                            tempno = checkorigin(
                                number, 'pawncap', turn, move[0])-1
                            if moves[-3] == tostring(tempno-16) + tostring(tempno) or moves[-3] == tostring(tempno+16) + tostring(tempno):
                                gameboard[number] = turn + move[-1]
                                gameboard[tempno] = '  '
                                gameboard[tempno+1] = '  '
                                if check(turn):
                                    gameboard[number] = '  '
                                    gameboard[tempno] = opp + 'P'
                                    gameboard[tempno+1] = turn + 'P'
                                    return False
                                elif checked == True:
                                    gameboard[number] = '  '
                                    gameboard[tempno] = opp + 'P'
                                    gameboard[tempno+1] = turn + 'P'
                                    return False
                                else:
                                    tempstring = tostring(
                                        tempno-1) + tostring(number) + move[-1].lower()
                                    moves.append(tempstring)
                                    return True
                            else:
                                return False
                        else:
                            return False
                else:
                    if checkorigin(number, 'pawn', turn, None):
                        if gameboard[number] == '  ':
                            temp = gameboard[number]
                            tempno = checkorigin(number, 'pawn', turn, None)
                            gameboard[checkorigin(
                                number, 'pawn', turn, None)] = '  '
                            gameboard[number] = turn + move[-1]
                            if check(turn):
                                gameboard[number] = temp
                                gameboard[tempno] = turn + 'P'
                                return False
                            elif checked == True:
                                gameboard[number] = temp
                                gameboard[tempno] = turn + 'P'
                                return True
                            else:
                                tempstring = tostring(
                                    tempno) + tostring(number) + move[-1].lower()
                                moves.append(tempstring)
                                return True
                        else:
                            return False
                    else:
                        return False
            else:
                if checked == None:
                    print('Please use the notation ' +
                          move[0:4] + '=p, where p is N, B, R, Q.')
                return False
        elif 'x' in move:
            if checkorigin(number, 'pawncap', turn, move[0]):
                if turn not in gameboard[number] and gameboard[number] != '  ':
                    temp = gameboard[number]
                    gameboard[number] = turn + 'P'
                    tempno = checkorigin(number, 'pawncap', turn, move[0])
                    gameboard[checkorigin(
                        number, 'pawncap', turn, move[0])] = '  '
                    if check(turn):
                        gameboard[number] = temp
                        gameboard[tempno] = turn + 'P'
                        return False
                    elif checked == True:
                        gameboard[number] = temp
                        gameboard[tempno] = turn + 'P'
                        return True
                    else:
                        tempstring = tostring(tempno) + tostring(number)
                        moves.append(tempstring)
                        return True
                elif gameboard[checkorigin(number, 'pawncap', turn, move[0])+1] == opp + 'P':
                    tempno = checkorigin(number, 'pawncap', turn, move[0])+1
                    if moves[-1] == tostring(tempno-16) + tostring(tempno) or moves[-1] == tostring(tempno+16) + tostring(tempno):
                        gameboard[number] = turn + 'P'
                        gameboard[tempno] = '  '
                        gameboard[tempno-1] = '  '
                        if check(turn):
                            gameboard[number] = '  '
                            gameboard[tempno] = opp + 'P'
                            gameboard[tempno-1] = turn + 'P'
                            return False
                        elif checked == True:
                            gameboard[number] = '  '
                            gameboard[tempno] = opp + 'P'
                            gameboard[tempno-1] = turn + 'P'
                            return True
                        else:
                            tempstring = tostring(tempno-1) + tostring(number)
                            moves.append(tempstring)
                            return True
                elif gameboard[checkorigin(number, 'pawncap', turn, move[0])-1] == opp + 'P':
                    tempno = checkorigin(number, 'pawncap', turn, move[0])-1
                    if moves[-1] == tostring(tempno-16) + tostring(tempno) or moves[-1] == tostring(tempno+16) + tostring(tempno):
                        gameboard[number] = turn + 'P'
                        gameboard[tempno] = '  '
                        gameboard[tempno+1] = '  '
                        if check(turn):
                            gameboard[number] = '  '
                            gameboard[tempno] = opp + 'P'
                            gameboard[tempno+1] = turn + 'P'
                            return False
                        elif checked == True:
                            gameboard[number] = '  '
                            gameboard[tempno] = opp + 'P'
                            gameboard[tempno+1] = turn + 'P'
                            return False
                        else:
                            tempstring = tostring(tempno-1) + tostring(number)
                            moves.append(tempstring)
                            return True
                else:
                    return False
        elif len(move) < 3:
            if checkorigin(number, 'pawn', turn, None):
                if gameboard[number] == '  ':
                    temp = gameboard[number]
                    tempno = checkorigin(number, 'pawn', turn, None)
                    gameboard[checkorigin(number, 'pawn', turn, None)] = '  '
                    gameboard[number] = turn + 'P'
                    if check(turn):
                        gameboard[number] = temp
                        gameboard[tempno] = turn + 'P'
                        return False
                    elif checked == True:
                        gameboard[number] = temp
                        gameboard[tempno] = turn + 'P'
                        return True
                    else:
                        tempstring = tostring(tempno) + tostring(number)
                        moves.append(tempstring)
                        return True
            else:
                return False
        else:
            return False
    else:
        return False


gameboard = [
    'bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR',
    'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP',
    '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
    '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
    '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
    '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
    'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP',
    'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'
]

squares = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
           'e': 4, 'f': 5, 'g': 6, 'h': 7}

bots = {'Michael Adams': 1, 'Mace': 400, 'Oliver': 600, 'Rainier': 800, 'Yixuan': 1000,
        'Pranav': 1200, 'Joel': 1400, 'Bruce': 1600, 'amogus': 1800, 'bob': 2000, 'monke': 2200,
        'real bot': 2400, 'cheater': 2600, 'sheesh': 2800, 'stockfish': 3000}

allboards.append(gameboard)
strboards.append(str(gameboard))

if havestockfish == True:
  mode = input("Play against a human(H) or bot(B): ").lower()
  while mode not in ['b', 'h', 't']:
      mode = input("Please input 'H' or 'B'. ").lower()
  match mode:
    case 'b':
        bot = True
        for key, value in bots.items():
            print(key + ": " + str(value) + " ELO")
        against = input("Pick a bot to play against. ")
        while against not in bots:
            for key, value in bots.items():
                print(key + ": " + str(value) + " ELO")
            against = input("Pick a bot to play against.(Case sensitive) ")
        rating = bots[against]
        stockfish = Stockfish(path=thepath, depth=list(bots.keys()).index(
            against) + 2, parameters={"UCI_LimitStrength": "true", "UCI_Elo": rating})
        playas = input("Do you want to play as white(W) or black(B): ").lower()
        while playas not in ['b', 'w']:
            playas = input("Please input 'W' or 'B'. ").lower()
        if playas == 'w':
            player = 'w'
        else:
            player = 'b'
    case 't':
        stockfish = Stockfish(path=thepath, depth=15, parameters={
                              "UCI_LimitStrength": "true", "UCI_Elo": 2850})
        against = 'Michael Adams'
        rating = bots[against]
        if input('') == 'b':
            bot = True
            player = None
        else:
            bot = False
        gameboard = testboards[int(input('no. '))]
    case other:
        bot = False
else:
  bot = False

rules = input(
    "Do you want to see the rules and input for this program? ").lower()
while rules not in ['y', 'n']:
    rules = input('Please enter "y" or "n" ').lower()
if rules == 'y':
  print(os.read(os.open(os.getcwd()+"/movesandrules.txt",os.O_RDONLY),10000).decode("UTF-8"))

pygame.init()
squaresize = input('How big do you want each square to be?(default is 80) ')
while not isinstance(squaresize, int) and squaresize != '':
    try:
        squaresize = int(squaresize)
    except(ValueError):
        squaresize = input('Please input an integer. ')
if squaresize == '':
    squaresize = 80
elif squaresize < 20:
    squaresize = 20
elif squaresize > 100:
    squaresize = 100

width = squaresize * 8
height = squaresize * 8
borderwidth = squaresize
screen = pygame.display.set_mode(
    (width + squaresize * 2, height + squaresize * 2))
pygame.display.set_caption("Chess.py")
chessboard = configboard(gameboard)
clock = pygame.time.Clock()
fps = 60

pieces = {
    'wP': os.getcwd()+'/pieces/wP.svg',
    'wR': os.getcwd()+'/pieces/wR.svg',
    'wN': os.getcwd()+'/pieces/wN.svg',
    'wB': os.getcwd()+'/pieces/wB.svg',
    'wQ': os.getcwd()+'/pieces/wQ.svg',
    'wK': os.getcwd()+'/pieces/wK.svg',
    'bP': os.getcwd()+'/pieces/bP.svg',
    'bR': os.getcwd()+'/pieces/bR.svg',
    'bN': os.getcwd()+'/pieces/bN.svg',
    'bB': os.getcwd()+'/pieces/bB.svg',
    'bQ': os.getcwd()+'/pieces/bQ.svg',
    'bK': os.getcwd()+'/pieces/bK.svg'
}


piece_images = {}
for name, filename in pieces.items():
    svg_data = open(filename).read()
    png_data = cairosvg.svg2png(file_obj=io.StringIO(
        svg_data), output_width=squaresize, output_height=squaresize)
    pygame_surface = pygame.image.load(io.BytesIO(png_data))
    piece_images[name] = pygame_surface


def draw_outer_layer(surface): #draw the outside, numbers and board
    font = pygame.font.Font(None, int(squaresize / 10 * 4))
    for row in range(8):
        label = font.render(str(8-row), 1, (255, 255, 255))
        screen.blit(label, (borderwidth//2, row*squaresize +
                            borderwidth+squaresize//2-label.get_height()//2))

    for col, letter in enumerate('abcdefgh'):
        label = font.render(letter, 1, (255, 255, 255))
        screen.blit(label, (col*squaresize+borderwidth+squaresize //
                            2-label.get_width()//2, borderwidth//2))


over = False
move = 1
turn = 'w'
moved = False
gameover = False
pgn = []

chessboard = configboard(gameboard)
for row in range(8):
    for col in range(8):
        x = col * squaresize + borderwidth
        y = row * squaresize + borderwidth
        if (row+col) % 2 == 0:
            color = (181, 136, 99)
        else:
            color = (240, 217, 181)
        pygame.draw.rect(screen, color, (x, y, squaresize, squaresize))
        if chessboard[row][col] != '  ':
            screen.blit(piece_images[chessboard[row][col]], (x, y))

draw_outer_layer(screen)

pygame.display.update()

input_text = ''

round = []

print('White to move: ')

while not over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if len(round) > 0 and pgn[-1] != round:
                pgn.append(round)
            over = True
        if gameover == False:
            if event.type == pygame.KEYDOWN:
                if event.unicode.isprintable():
                    input_text += event.unicode
                    print(event.unicode, end='', flush=True)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    print('\b', end='', flush=True)
                    print(' ', end='', flush=True)
                    print('\b', end='', flush=True)
                elif event.key == pygame.K_RETURN:
                    print('\n', end='')
                    if bot:
                        match turn:
                            case 'w':
                                takes = False
                                round = []
                                if player == 'w':
                                    if not getmove(input_text, 'w'):
                                        print("Illegal move!")
                                    else:
                                        round.append(input_text)
                                        drawed = draw()
                                        checkmated = checkmate('b')
                                        if drawed:
                                            print('Draw by ' + drawed)
                                            gameover = True
                                        elif checkmated == 'checkmate':
                                            print('White wins by checkmate.')
                                            gameover = True
                                        elif checkmated == 'stalemate':
                                            print('Draw by stalemate.')
                                            gameover = True
                                        else:
                                            print(
                                                'Black to move(press enter for stockfish move): ')
                                            turn = 'b'
                                            if check('b'):
                                                print("Black is in check!")
                                else:
                                    stockfish.set_position(moves)
                                    fullmove = stockfish.get_best_move_time(
                                        rating)
                                    if len(moves) == 0:
                                        try:
                                            fullmove = stockfish.get_top_moves(
                                                15)[randint(1, 15)]['Move']
                                        except(IndexError):
                                            fullmove = stockfish.get_top_moves(
                                                5)[randint(1, 5)]['Move']
                                    themove = fullmove[2:4]
                                    piece = fullmove[0:2]
                                    if len(fullmove) == 5:
                                        promo = fullmove[-1].upper()
                                    themove = movetonumber(themove)
                                    piece = movetonumber(piece)
                                    piecename = gameboard[piece]
                                    if len(fullmove) == 5:
                                        gameboard[piece] = '  '
                                        gameboard[themove] = 'w' + promo
                                        round.append(
                                            fullmove[0]+tostring(themove)+'='+promo)
                                    elif fullmove == 'e1g1':
                                        gameboard[60] = '  '
                                        gameboard[61] = 'wR'
                                        gameboard[62] = 'wK'
                                        gameboard[63] = '  '
                                        round.append('O-O')
                                    elif fullmove == 'e1c1':
                                        gameboard[60] = '  '
                                        gameboard[59] = 'wR'
                                        gameboard[58] = 'wK'
                                        gameboard[56] = '  '
                                        round.append('O-O-O')
                                    else:
                                        gameboard[piece] = '  '
                                        gameboard[themove] = piecename
                                        if 'P' in piecename:
                                            round.append(
                                                fullmove[0]+tostring(themove))
                                        else:
                                            if 'K' not in piecename:
                                                round.append(
                                                    piecename[-1]+tostring(piece)+tostring(themove))
                                            else:
                                                round.append(
                                                    piecename[-1]+tostring(themove))
                                    moves.append(fullmove)
                                    drawed = draw()
                                    checkmated = checkmate('b')
                                    if drawed:
                                        print('Draw by ' + drawed)
                                        gameover = True
                                    elif checkmated == 'checkmate':
                                        print('White wins by checkmate.')
                                        gameover = True
                                    elif checkmated == 'stalemate':
                                        print('Draw by stalemate.')
                                        gameover = True
                                    else:
                                        print('Black to move')
                                        turn = 'b'
                                        if check('b'):
                                            print('Black is in check!')
                            case 'b':
                                takes = False
                                if player == 'b':
                                    if not getmove(input_text, 'b'):
                                        print("Illegal move!")
                                    else:
                                        round.append(input_text)
                                        drawed = draw()
                                        checkmated = checkmate('w')
                                        if drawed:
                                            print('Draw by ' + drawed)
                                            round = []
                                            gameover = True
                                        elif checkmated == 'checkmate':
                                            print('Black wins by checkmate.')
                                            round = []
                                            gameover = True
                                        elif checkmated == 'stalemate':
                                            print('Draw by stalemate.')
                                            round = []
                                            gameover = True
                                        else:
                                            print(
                                                'White to move(press enter for stockfish move): ')
                                            turn = 'w'
                                            if check('w'):
                                                print("White is in check!")
                                else:
                                    stockfish.set_position(moves)
                                    fullmove = stockfish.get_best_move_time(
                                        rating)
                                    if len(moves) == 1:
                                        try:
                                            fullmove = stockfish.get_top_moves(
                                                5)[randint(1, 5)]['Move']
                                        except(IndexError):
                                            try:
                                                fullmove = stockfish.get_top_moves(
                                                    2)[randint(1, 2)]['Move']
                                            except(IndexError):
                                                fullmove = stockfish.get_best_move()
                                    themove = fullmove[2:4]
                                    piece = fullmove[0:2]
                                    if len(fullmove) == 5:
                                        promo = fullmove[-1].upper()
                                    themove = movetonumber(themove)
                                    piece = movetonumber(piece)
                                    piecename = gameboard[piece]
                                    if len(fullmove) == 5:
                                        gameboard[piece] = '  '
                                        gameboard[themove] = 'b' + promo
                                        round.append(
                                            fullmove[0]+tostring(themove)+'='+promo)
                                    elif fullmove == 'e8g8':
                                        gameboard[4] = '  '
                                        gameboard[5] = 'bR'
                                        gameboard[6] = 'bK'
                                        gameboard[7] = '  '
                                        round.append('O-O')
                                    elif fullmove == 'e8c8':
                                        gameboard[4] = '  '
                                        gameboard[3] = 'bR'
                                        gameboard[2] = 'bK'
                                        gameboard[0] = '  '
                                        round.append('O-O-O')
                                    else:
                                        gameboard[piece] = '  '
                                        gameboard[themove] = piecename
                                        if 'P' in piecename:
                                            round.append(
                                                fullmove[0]+tostring(themove))
                                        else:
                                            if 'K' not in piecename:
                                                round.append(
                                                    piecename[-1]+tostring(piece)+tostring(themove))
                                            else:
                                                round.append(
                                                    piecename[-1]+tostring(themove))
                                    moves.append(fullmove)
                                    drawed = draw()
                                    checkmated = checkmate('w')
                                    if drawed:
                                        print('Draw by ' + drawed)
                                        gameover = True
                                    elif checkmated == 'checkmate':
                                        print('Black wins by checkmate.')
                                        gameover = True
                                    elif checkmated == 'stalemate':
                                        print('Draw by stalemate.')
                                        gameover = True
                                    else:
                                        print('White to move')
                                        turn = 'w'
                                        if check('w'):
                                            print('White is in check!')
                                        pgn.append(round)

                    else:
                        match turn:
                            case 'w':
                                round = []
                                if not getmove(input_text, 'w'):
                                    print("Illegal move!")
                                else:
                                    round.append(input_text)
                                    drawed = draw()
                                    checkmated = checkmate('b')
                                    if drawed:
                                        print('Draw by ' + drawed)
                                        gameover = True
                                    elif checkmated == 'checkmate':
                                        print('White wins by checkmate.')
                                        gameover = True
                                    elif checkmated == 'stalemate':
                                        print('Draw by stalemate.')
                                        gameover = True
                                    else:
                                        print('Black to move: ')
                                        turn = 'b'
                                        if check('b'):
                                            print("Black is in check!")
                            case 'b':
                                if not getmove(input_text, 'b'):
                                    print("Illegal move!")
                                else:
                                    round.append(input_text)
                                    drawed = draw()
                                    checkmated = checkmate('w')
                                    if drawed:
                                        print('Draw by ' + drawed)
                                        gameover = True
                                    elif checkmated == 'checkmate':
                                        print('Black wins by checkmate.')
                                        gameover = True
                                    elif checkmated == 'stalemate':
                                        print('Draw by stalemate.')
                                        gameover = True
                                    else:
                                        print('White to move: ')
                                        turn = 'w'
                                        if check('w'):
                                            print("White is in check!")
                                        pgn.append(round)
                                    round = []
                    input_text = ''

    chessboard = configboard(gameboard)
    for row in range(8):
        for col in range(8):
            x = col * squaresize + borderwidth
            y = row * squaresize + borderwidth
            if (row+col) % 2 == 0:
                color = (181, 136, 99)
            else:
                color = (240, 217, 181)
            pygame.draw.rect(screen, color, (x, y, squaresize, squaresize))
            if chessboard[row][col] != '  ':
                screen.blit(piece_images[chessboard[row][col]], (x, y))
    draw_outer_layer(screen)
    pygame.display.update()
    clock.tick(fps)

pygame.quit()

print('')
pgnyn = input('Do you want the PGN of this game?("y", "n") ')
while pgnyn.lower() not in ['y', 'n']:
    print('')
    pgnyn = input('Please enter "y" or "n". ')
if pgnyn == 'y':
    for count, rounds in enumerate(pgn):
        print(str(count+1), end='. ')
        print(*rounds)
