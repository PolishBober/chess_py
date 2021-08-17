import moves
import chess_assistance
from data import *

def advantage(board, log, pieces_color):
    teams_posiotions = [chess_assistance.team_positions(board, 0), chess_assistance.team_positions(board, 1)]
    pieces_values = [2, 3, 3, 5, 9, 2]
    #punkty za:
    #dostepne_pola = 1/4
    #bronione_pola = 1/3
    #atakowane_pola = 1/2

    points = [0, 0]

    for team in range(len(teams_posiotions)):
        for piece in teams_posiotions[team]:
            for opponent in teams_posiotions[team - 1]:
                if opponent in moves.search(board, log, piece, pieces_color):
                    points[team] += pieces_values[[white_pieces, black_pieces][team - 1].index(board[opponent[0]][opponent[1]])] / pieces_values[[white_pieces, black_pieces][team].index(board[piece[0]][piece[1]])]
            points[team] += pieces_values[[white_pieces, black_pieces][team].index(board[piece[0]][piece[1]])]
    return points


def best_move(board, log, team, pieces_color):
    checked_team = team
    # dorobić promocję
    #dorobić mata w więcej niż jednym
    depth = 2
    logs = [[log]]
    boards = [[board]]
    pieces = [[chess_assistance.team_positions(board, team)]]
    punctation = []
    for level in range(depth):
        logs.append([])
        boards.append([])
        pieces.append([])
        for possibility in range(len(logs[level])):
            for piece in pieces[level][possibility]:
                for move in moves.search(boards[level][possibility], logs[level][possibility], piece, pieces_color):
                    if level == 0:
                        punctation.append([[piece, move], []])
                    logs[level + 1].append(logs[level][possibility] + [[piece, move]])
                    boards[level + 1].append(moves.make(boards[level][possibility], [piece, move]))
                    pieces[level + 1].append(chess_assistance.team_positions(boards[level + 1][-1], team - 1))

                    #chess_assistance.write(boards[level + 1][-1], pieces_color)

                    if level == 0:
                        if chess_assistance.checkmate(boards[level][possibility], checked_team - 1, logs[level][possibility], pieces_color):
                            return punctation[-1][0]
                        if chess_assistance.stalemate(boards[level][possibility], checked_team - 1, logs[level][possibility], pieces_color):
                            if advantage(board, log, pieces_color)[team] <= advantage(board, log, pieces_color)[team - 1]:
                                return punctation[-1][0]
                            else:
                                del punctation[-1]

                    if level + 1 == depth:
                        for evaluation in range(len(punctation)):
                            if punctation[evaluation][0] == logs[level][possibility][len(log)]:
                                punctation[evaluation][-1].append(advantage(boards[level + 1][-1], logs[level + 1][-1], pieces_color)[checked_team] - advantage(boards[level + 1][-1], logs[level + 1][-1], pieces_color)[checked_team - 1])

        team = chess_assistance.renewing(team - 1)

    for evaluation in range(len(punctation)):
        punctation[evaluation][-1] = [min(punctation[evaluation][-1]), sum(punctation[evaluation][-1]) / len(punctation[evaluation][-1])]
    while len(punctation) != 1:
        if punctation[0][-1][0] > punctation[1][-1][0]:
            del punctation[1]
        elif punctation[0][-1][0] < punctation[1][-1][0]:
            del punctation[0]
        else:
            if punctation[0][-1][1] > punctation[1][-1][1]:
                del punctation[1]
            else:
                del punctation[0]
    return punctation[0][0]
