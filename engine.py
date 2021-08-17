import moves
import chess_assistance
from data import *

# warunki
# 1. nie dać się za matować
# 2. dać mata
# 3. zdobyć przewagę materialną
# może

# dzielenie przez zero

# przyznawanie punktów za roszadę
# ilość figur
# bliskość mata
# ilość atakaowanych pól i ich wartość
# ilość bronionych pól
# ilość dostępnych pól


def advantage(board, log):
    teams_positions = [chess_assistance.team_positions(board, 0), chess_assistance.team_positions(board, 1)]
    pieces_values = [1, 3, 3, 5, 9, 2]
    # punkty za:
    # dostepne_pola = 1/4
    # bronione_pola = 1/3
    # atakowane_pola = 1/2

    points = [0, 0]

    for team in range(len(teams_positions)):
        for piece in teams_positions[team]:
            for opponent in teams_positions[team - 1]:
                if opponent in moves.search(board, log, piece):
                    points[team] += pieces_values[[white_pieces, black_pieces][team - 1].index(board[opponent[0]][opponent[1]])] / pieces_values[[white_pieces, black_pieces][team].index(board[piece[0]][piece[1]])]
            points[team] += pieces_values[[white_pieces, black_pieces][team].index(board[piece[0]][piece[1]])]
    return points


def best_move(board, log, team, draw_check):
    checked_team = abs(team)
    depth = 2
    logs = [[log]]
    boards = [[board]]
    pieces = [[chess_assistance.team_positions(board, team)]]
    advantages = [[['']]]
    available_moves = []
    for level in range(depth):
        logs.append([])
        boards.append([])
        pieces.append([])
        for possibility in range(len(logs[-2])):
            for piece in pieces[-2][possibility]:
                for advantage_ in moves.search(boards[-2][possibility], logs[-2][possibility], piece):
                    promotions = 1
                    if advantage_[0] in [0, 7] and board[piece[0]][piece[1]] in [white_pieces[0], black_pieces[0]]:
                        promotions = 4
                    for promotion in range(promotions):
                        if promotions == 1:
                            logs[-1].append(logs[-2][possibility] + [[piece, advantage_]])
                            boards[-1].append(moves.make(boards[-2][possibility], [piece, advantage_]))
                        else:
                            logs[-1].append(logs[-2][possibility] + [[piece, advantage_ + [['N', 'B', 'R', 'Q'][promotion]]]])
                            boards[-1].append(moves.make(boards[-2][possibility], [piece, advantage_ + [['N', 'B', 'R', 'Q'][promotion]]]))
                        pieces[-1].append(chess_assistance.team_positions(boards[-1][-1], team - 1))

                        #chess_assistance.write(boards[level + 1][-1], pieces_color)

                        if level == 0:
                            if promotions == 1:
                                available_moves.append([piece, advantage_])
                            else:
                                available_moves.append([piece, advantage_ + [['N', 'B', 'R', 'Q'][promotion]]])

                        if level + 1 == depth:
                            if len(logs[-1]) == 1:
                                advantages.append([[advantage(boards[-1][-1], logs[-1][-1])[checked_team] - advantage(boards[-1][-1], logs[-1][-1])[checked_team - 1]]])
                            else:
                                if logs[-1][-1][-2] == logs[-1][-2][-2]:
                                    advantages[-1][-1].append(advantage(boards[-1][-1], logs[-1][-1])[checked_team] - advantage(boards[-1][-1], logs[-1][-1])[checked_team - 1])
                                else:
                                    advantages[-1].append([advantage(boards[-1][-1], logs[-1][-1])[checked_team] - advantage(boards[-1][-1], logs[-1][-1])[checked_team - 1]])
                        else:
                            if len(logs[-1]) == 1:
                                advantages.append([['']])
                            else:
                                if len(logs[-1][-1]) == 1:
                                    advantages[-1][-1].append('')
                                else:
                                    if logs[-1][-1][-2] == logs[-1][-2][-2]:
                                        advantages[-1][-1].append('')
                                    else:
                                        advantages[-1].append([''])
                        if chess_assistance.stalemate(boards[-1][-1], checked_team - 1, logs[-1][-1]) or chess_assistance.stalemate(boards[-1][-1], checked_team, logs[-1][-1]) or chess_assistance.draw(board, draw_check):
                            advantages[-1][-1][-1] = 0
                            del logs[-1][-1], boards[-1][-1], pieces[-1][-1]

                        if chess_assistance.checkmate(boards[-1][-1], checked_team - 1, logs[-1][-1]) or chess_assistance.checkmate(boards[-1][-1], checked_team, logs[-1][-1]):
                            if level == 0:
                                for available_move in available_moves:
                                    if available_move == logs[-1][-1][len(log)]:
                                        return available_move
                            if chess_assistance.checkmate(boards[-1][-1], checked_team - 1, logs[-1][-1]):
                                advantages[-1][-1][-1] = str(team) + '#'
                            else:
                                advantages[-1][-1][-1] = str(abs(team - 1)) + '#'
                            del logs[-1][-1], boards[-1][-1], pieces[-1][-1]
        team = abs(team - 1)

    for level in range(depth, 0, -1):
        for advantage_ in range(len(advantages[level])):

            if '0#' in advantages[level][advantage_] or '1#' in advantages[level][advantage_]:
                # opponent
                if level % 2 == 0:
                    if str(abs(team - 1)) + '#' in advantages[level][advantage_]:
                        best = str(abs(team - 1)) + '#'
                    else:
                        while str(team) + '#' in advantages[level][advantage_]:
                            del advantages[level][advantage_][advantages[level][advantage_].index(str(team) + '#')]

                        if len(advantages[level][advantage_]) == 0:
                            best = str(team) + '#'
                        else:
                            best = min(advantages[level][advantage_])
                # checked
                else:
                    if str(team) + '#' in advantages[level][advantage_]:
                        best = str(team) + '#'
                    else:
                        while str(abs(team - 1)) + '#' in advantages[level][advantage_]:
                            del advantages[level][advantage_][advantages[level][advantage_].index(str(abs(team - 1)) + '#')]

                        if len(advantages[level][advantage_]) == 0:
                            best = str(abs(team - 1)) + '#'
                        else:
                            best = max(advantages[level][advantage_])
            else:
                # opponent
                if level % 2 == 0:
                    best = min(advantages[level][advantage_])
                # checked
                else:
                    best = max(advantages[level][advantage_])

            available_move = 0
            while advantage_ >= len(advantages[level - 1][available_move]) and level != 1:
                advantage_ -= len(advantages[level - 1][available_move]) + advantages[level - 1][available_move].count('0#') + advantages[level - 1][available_move].count('1#')
                available_move += 1
                if advantage_ < len(advantages[level - 1][available_move]):
                    advantage_ += advantages[level - 1][available_move][:advantage_].count('0#') + advantages[level - 1][available_move][:advantage_].count('1#')
                    while advantages[level - 1][available_move][advantage_] in ['0#', '1#'] and advantage_ < len(advantages[level - 1][available_move]):
                        advantage_ += 1
            if level == 1:
                for available_move in range(len(available_moves)):
                    if advantages[1][0][available_move] == best:
                        while '0#' in advantages[2][available_move]:
                            del advantages[2][available_move][advantages[2][available_move].index('0#')]
                        while '1#' in advantages[2][available_move]:
                            del advantages[2][available_move][advantages[2][available_move].index('1#')]

                        if advantages[0][0][0] == '':
                            advantages[0][0][0] = available_move
                        elif sum(advantages[2][advantages[0][0][0]]) / len(advantages[2][advantages[0][0][0]]) < sum(advantages[2][available_move]) / len(advantages[2][available_move]):
                            advantages[0][0][0] = available_move
            else:
                advantages[level - 1][available_move][advantage_] = best
    return available_moves[advantages[0][0][0]]
