import chess_assistance
import moves
import engine
import boards
from data import *
import os


path = r'parties\p' + [str(liczba) for liczba in range(1, len(os.listdir('parties')) + 2) if 'p' + str(liczba) + '.py' not in os.listdir('parties')][0] + '.py'

player_color = input('Wybierz kolor figur którymi chcesz grać lub wpisz numer partii którą chcesz dokończyć. ').lower()
while player_color not in ['biały', 'czarny'] and 'p' + player_color + '.py' not in os.listdir('parties'):
    player_color = input('Nie rozumiem, wpisz kolor figur jakimi chcesz grać lub numer partii. ').lower()
player_color, board, log, draw_check = boards.add(player_color)

if len(log) == 0:
    round = player_color
    if player_color == 0:
        chess_assistance.write(player_color, board)
else:
    if board[log[-1][1][0]][log[-1][1][1]] in [white_pieces, black_pieces][player_color]:
        round = 1
    else:
        round = 0
    chess_assistance.write(player_color, board)


while True:
    if round % 2 == 0:
        chess_assistance.introduce_move(player_color, board, log)
        chess_assistance.save(path, player_color, log)
        chess_assistance.introduce_promotion(board, log)
        board = moves.make(board, log[-1])

    else:
        log.append(engine.best_move(board, log, player_color - 1, draw_check))
        chess_assistance.save(path, player_color, log)
        board = moves.make(board, log[-1])

        chess_assistance.write(player_color, board)

        print('Silnik: ' + chess_assistance.deconvert(log[-1]) + '\n')
        advantage = engine.advantage(board, log)
        print('Gracz', str(advantage[player_color] * 10000 // sum(advantage) / 100) + '% :', str(advantage[player_color - 1] * 10000 // sum(advantage) / 100) + '% Silnik')

    round += 1

    if draw_check[-1][log[-1][1][0]][log[-1][1][1]] in white_pieces + black_pieces or draw_check[-1][log[-1][0][0]][log[-1][0][1]] in [white_pieces[0], black_pieces[0]] or draw_check[-1][log[-1][0][0]][log[-1][0][1]] in [white_pieces[5], black_pieces[5]] and abs(log[-1][0][1] - log[-1][1][1]) == 2:
        draw_check = []
    draw_check.append(board)

    if chess_assistance.stalemate(board, round % 2 - player_color, log) or chess_assistance.draw(board, draw_check):
        print('\n'*2, '½ – ½ remis')
        break
    if chess_assistance.checkmate(board, round % 2 - player_color, log):
        print('\n' * 2, ['0 – 1 wygrana czarnych', '1 – 0 wygrana białych'][round % 2 - player_color])
        break
