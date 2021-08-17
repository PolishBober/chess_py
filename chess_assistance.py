import moves
from data import *


def save(path, pieces_color, log):
    file = open(path, 'w')
    file.write('def add():\n    return ' + str(pieces_color) + ', ' + str(log))
    file.close()


def write(player_color, board):
    order = 1
    if player_color == 1:
        board = [line[::-1] for line in board][::-1]
        order = -1
    print('\n' + ' '*3, '\t'.join(alphabet[::order]).upper())
    for x in range(8):
        numbers = 8 - x
        if player_color == 1:
            numbers = x + 1
        print(numbers, end='\t')
        for y in range(8):
            if board[x][y] == '':
                print(squares[(x % 2 + y % 2) % 2], end='\t')
            else:
                print(board[x][y], end='\t')
        print(numbers)
    print(' '*3, '\t'.join(alphabet[::order]).upper() + '\n')


def team_positions(board, team):
    return [[int(square / 8), square % 8] for square in range(64) if board[int(square / 8)][square % 8] in [white_pieces, black_pieces][team]]


def draw(board, draw_check):
    pieces = []
    for line in range(8):
        pieces += board[line]
    while '' in pieces:
        pieces.remove('')
    if len(pieces) == 3:
        if white_pieces[1] in pieces or white_pieces[2] in pieces or black_pieces[1] in pieces or black_pieces[2] in pieces:
            return True

    for position in draw_check:
        if draw_check.count(position) > 2:
            return True

    return False

def stalemate(board, team, log):
    if len(['' for piece in team_positions(board, team) if len(moves.search(board, log, piece)) == 0]) == len(team_positions(board, team)) and len(['' for piece in team_positions(board, team - 1) if [[int(king / 8), king % 8] for king in range(64) if board[int(king / 8)][king % 8] == [white_pieces[5], black_pieces[5]][team]][0] in moves.search(board, log, piece)]) == 0:
        return True
    return False

def checkmate(board, team, log):
    if len(['' for piece in team_positions(board, team) if len(moves.search(board, log, piece)) == 0]) == len(team_positions(board, team)) and len(['' for piece in team_positions(board, team - 1) if [[int(king / 8), king % 8] for king in range(64) if board[int(king / 8)][king % 8] == [white_pieces[5], black_pieces[5]][team]][0] in moves.search(board, log, piece)]) > 0:
        return True
    return False


def introduce_move(player_color, board, log):
    log.append(input('Podaj swój ruch. ').lower())

    while len(log[-1]) != 5:
        log[-1] = input('Niepoprawny zapis ruchu, wpisz go jeszcze raz. ').lower()

    while not log[-1][0] in alphabet or not log[-1][1] in numbers or not log[-1][2] == '-' or not log[-1][3] in alphabet or not log[-1][4] in numbers:
        log[-1] = input('Niepoprawna nazwa pola, wpisz ją jeszcze raz. ').lower()
        while len(log[-1]) != 5:
            log[-1] = input('Niepoprawny zapis ruchu, wpisz go jeszcze raz. ').lower()

    log[-1] = convert(log[-1])
    while not board[log[-1][0][0]][log[-1][0][1]] in [white_pieces, black_pieces][player_color] or not log[-1][1] in moves.search(board, log[:-1], log[-1][0]):
        log[-1] = input('Podany przez ciebie ruch jest niedostępny, wpisz swój ruch jeszcze raz. ').lower()
        while not log[-1][0] in alphabet or not log[-1][1] in numbers or not log[-1][2] == '-' or not log[-1][3] in alphabet or not log[-1][4] in numbers:
            log[-1] = input('Niepoprawna nazwa pola, wpisz ją jeszcze raz. ').lower()
            while len(log[-1]) != 5:
                log[-1] = input('Niepoprawny zapis ruchu, wpisz go jeszcze raz. ').lower()
        log[-1] = convert(log[-1])

def introduce_promotion(board, log):
    if log[-1][1][0] in [0, 7] and board[log[-1][0][0]][log[-1][0][1]] in [white_pieces[0], black_pieces[0]]:
        promotion = input('Podaj nazwę figury jaką chcesz uzyskać w promocji. ').lower()
        while promotion not in ['skoczek', 'goniec', 'wieża', 'hetman']:
            promotion = input('Takiej figury nie możesz uzyskać w promocji, wpisz nazwę figury jeszcze raz. ').lower()
        log[-1][1].append(['N', 'B', 'R', 'Q'][['skoczek', 'goniec', 'wieża', 'hetman'].index(promotion)])


def convert(move):
    return [[8 - int(move[1]), alphabet.index(move[0])], [8 - int(move[4]), alphabet.index(move[3])]]

def deconvert(move):
    return alphabet[move[0][1]] + str(-move[0][0] + 8) + '-' + alphabet[move[1][1]] + str(-move[1][0] + 8)
