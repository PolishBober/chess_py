import chess_assistance
import moves
import engine
import engine2
import boards
from data import *
import os


path = r'parties\p' + [str(liczba) for liczba in range(1, len(os.listdir('parties')) + 2) if 'p' + str(liczba) + '.py' not in os.listdir('parties')][0] + '.py'
def save(log):
    file = open(path, 'w')
    file.write('def add():\n    return ' + str(log))
    file.close()


pieces_color = 'biały'
board, log = boards.add(pieces_color)
if pieces_color == 'biały':
    pieces_color = 0
    round = 0
else:
    pieces_color = 1
    round = 1

chess_assistance.write(board, pieces_color)


while True:
    if round % 2 == 0:
        log.append(engine2.best_move(board, log, pieces_color, pieces_color))
        save(log)
        board = moves.make(board, log[-1])
        chess_assistance.write(board, pieces_color)

        print('Silnik1: ' + chess_assistance.deconvert(log[-1], pieces_color) + '\n')
        advantage = engine2.advantage(board, log, pieces_color)
        print('Biały', str(advantage[0] * 10000 // sum(advantage) / 100) + '% :',
              str(advantage[1] * 10000 // sum(advantage) / 100) + '% Czarny')

        if chess_assistance.stalemate(board, pieces_color, log, pieces_color):
            print('pat')
            break

        if chess_assistance.checkmate(board, pieces_color, log, pieces_color):
            print('mat')
            break

    else:
        log.append(engine.best_move(board, log, pieces_color - 1, pieces_color))
        save(log)
        board = moves.make(board, log[-1])
        chess_assistance.write(board, pieces_color)

        print('Silnik2: ' + chess_assistance.deconvert(log[-1], pieces_color) + '\n')
        advantage = engine.advantage(board, log, pieces_color)
        print('Biały', str(advantage[0] * 10000 // sum(advantage) / 100) + '% :',
              str(advantage[1] * 10000 // sum(advantage) / 100) + '% Czarny')

        if chess_assistance.stalemate(board, pieces_color, log, pieces_color):
            print('pat')
            break

        if chess_assistance.checkmate(board, pieces_color, log, pieces_color):
            print('mat')
            break
    round += 1