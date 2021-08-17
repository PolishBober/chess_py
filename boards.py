import boards_download
import moves
from data import *


def add(board_name):
    board = [
        ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
        ['♙' for x in range(8)],
        ['' for x in range(8)],
        ['' for x in range(8)],
        ['' for x in range(8)],
        ['' for x in range(8)],
        ['♟' for x in range(8)],
        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']
    ]
    if board_name == 'biały':
        return 0, board, [], [board]
    elif board_name == 'czarny':
        return 1, board, [], [board]
    else:
        file = open('boards_download.py', 'w')
        file.write(r'from parties import p' + board_name + '\ndef add():\n    return p' + board_name + '.add()')
        file.close()
        pieces_color, log = boards_download.add()
        draw_check = [board]
        for move in log:
            board = moves.make(board, move)
            if draw_check[-1][move[1][0]][move[1][1]] in white_pieces + black_pieces or draw_check[-1][move[0][0]][move[0][1]] in [white_pieces[0], black_pieces[0]] or draw_check[-1][move[0][0]][move[0][1]] in [white_pieces[5], black_pieces[5]] and abs(move[0][1] - move[1][1]) == 2:
                draw_check = []
            draw_check.append(board)
        return pieces_color, board, log, draw_check
