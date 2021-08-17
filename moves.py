from data import *


def search(board, log, piece):
    available_moves = []
    team = 1
    if board[piece[0]][piece[1]] in white_pieces:
        team = 0

# pawns
    if board[piece[0]][piece[1]] in [white_pieces[0], black_pieces[0]]:
        direction = -1
        if board[piece[0]][piece[1]] in black_pieces:
            direction = 1

        # forward two squares
        if piece[0] == 3.5 - 2.5 * direction:
            if board[piece[0] + direction][piece[1]] == '' and board[piece[0] + 2 * direction][piece[1]] == '':
                available_moves.append([piece[0] + 2 * direction, piece[1]])
        # forward one square
        if board[piece[0] + direction][piece[1]] == '':
            available_moves.append([piece[0] + direction, piece[1]])
        # capture left
        if piece[1] != 0:
            if board[piece[0] + direction][piece[1] - 1] in [white_pieces, black_pieces][team - 1]:
                available_moves.append([piece[0] + direction, piece[1] - 1])
        # capture right
        if piece[1] != 7:
            if board[piece[0] + direction][piece[1] + 1] in [white_pieces, black_pieces][team - 1]:
                available_moves.append([piece[0] + direction, piece[1] + 1])
        if len(log) > 0:
            # en passant left
            if piece[1] != 0:
                if board[piece[0]][piece[1] - 1] == [white_pieces[0], black_pieces[0]][team - 1] and log[-1][0][0] == piece[0] + 2 * direction and log[-1][0][1] == piece[1] - 1 and log[-1][1][0] == piece[0] and log[-1][1][1] == piece[1] - 1:
                    available_moves.append([piece[0] + direction, piece[1] - 1])
            # en passant right
            if piece[1] != 7:
                if board[piece[0]][piece[1] + 1] == [white_pieces[0], black_pieces[0]][team - 1] and log[-1][0][0] == piece[0] + 2 * direction and log[-1][0][1] == piece[1] + 1 and log[-1][1][0] == piece[0] and log[-1][1][1] == piece[1] + 1:
                    available_moves.append([piece[0] + direction, piece[1] + 1])

# knights
    elif board[piece[0]][piece[1]] in [white_pieces[1], black_pieces[1]]:
        knight_border = [[], []]

        for dimension in range(2):
            if piece[dimension] > 1:
                knight_border[dimension].append(-2)
                knight_border[dimension].append(-1)
            elif piece[dimension] > 0:
                knight_border[dimension].append(-1)
            if piece[dimension] < 6:
                knight_border[dimension].append(2)
                knight_border[dimension].append(1)
            elif piece[dimension] < 7:
                knight_border[dimension].append(1)

        for y in knight_border[0]:
            for x in knight_border[1]:
                if (x + y) % 2 == 1:
                    if not board[piece[0] + y][piece[1] + x] in [white_pieces, black_pieces][team]:
                        available_moves.append([piece[0] + y, piece[1] + x])

# bishops and queens
    elif board[piece[0]][piece[1]] in [white_pieces[2], black_pieces[2]] or board[piece[0]][piece[1]] in [white_pieces[4], black_pieces[4]]:
        if piece[0] < piece[1]:
            for available_move in range(1, piece[0] + 1):
                if board[piece[0] - available_move][piece[1] - available_move] in [white_pieces, black_pieces][team]:
                    break
                available_moves.append([piece[0] - available_move, piece[1] - available_move])
                if board[piece[0] - available_move][piece[1] - available_move] in [white_pieces, black_pieces][team - 1]:
                    break
            for available_move in range(1, 8 - piece[1]):
                if board[piece[0] + available_move][piece[1] + available_move] in [white_pieces, black_pieces][team]:
                    break
                available_moves.append([piece[0] + available_move, piece[1] + available_move])
                if board[piece[0] + available_move][piece[1] + available_move] in [white_pieces, black_pieces][team - 1]:
                    break
        else:
            for available_move in range(1, piece[1] + 1):
                if board[piece[0] - available_move][piece[1] - available_move] in [white_pieces, black_pieces][team]:
                    break
                available_moves.append([piece[0] - available_move, piece[1] - available_move])
                if board[piece[0] - available_move][piece[1] - available_move] in [white_pieces, black_pieces][team - 1]:
                    break
            for available_move in range(1, 8 - piece[0]):
                if board[piece[0] + available_move][piece[1] + available_move] in [white_pieces, black_pieces][team]:
                    break
                available_moves.append([piece[0] + available_move, piece[1] + available_move])
                if board[piece[0] + available_move][piece[1] + available_move] in [white_pieces, black_pieces][team - 1]:
                    break
        if 7 - piece[0] < piece[1]:
            for available_move in range(1, 8 - piece[0]):
                if board[piece[0] + available_move][piece[1] - available_move] in [white_pieces, black_pieces][team]:
                    break
                available_moves.append([piece[0] + available_move, piece[1] - available_move])
                if board[piece[0] + available_move][piece[1] - available_move] in [white_pieces, black_pieces][team - 1]:
                    break
            for available_move in range(1, 8 - piece[1]):
                if board[piece[0] - available_move][piece[1] + available_move] in [white_pieces, black_pieces][team]:
                    break
                available_moves.append([piece[0] - available_move, piece[1] + available_move])
                if board[piece[0] - available_move][piece[1] + available_move] in [white_pieces, black_pieces][team - 1]:
                    break
        else:
            for available_move in range(1, piece[1] + 1):
                if board[piece[0] + available_move][piece[1] - available_move] in [white_pieces, black_pieces][team]:
                    break
                available_moves.append([piece[0] + available_move, piece[1] - available_move])
                if board[piece[0] + available_move][piece[1] - available_move] in [white_pieces, black_pieces][team - 1]:
                    break
            for available_move in range(1, piece[0] + 1):
                if board[piece[0] - available_move][piece[1] + available_move] in [white_pieces, black_pieces][team]:
                    break
                available_moves.append([piece[0] - available_move, piece[1] + available_move])
                if board[piece[0] - available_move][piece[1] + available_move] in [white_pieces, black_pieces][team - 1]:
                    break

# rooks and queens
    if board[piece[0]][piece[1]] in [white_pieces[3], black_pieces[3]] or board[piece[0]][piece[1]] in [white_pieces[4], black_pieces[4]]:
        for available_move in range(1, piece[0] + 1):
            if board[piece[0] - available_move][piece[1]] in [white_pieces, black_pieces][team]:
                break
            available_moves.append([piece[0] - available_move, piece[1]])
            if board[piece[0] - available_move][piece[1]] in [white_pieces, black_pieces][team - 1]:
                break
        for available_move in range(1, piece[1] + 1):
            if board[piece[0]][piece[1] - available_move] in [white_pieces, black_pieces][team]:
                break
            available_moves.append([piece[0], piece[1] - available_move])
            if board[piece[0]][piece[1] - available_move] in [white_pieces, black_pieces][team - 1]:
                break
        for available_move in range(1, 8 - piece[0]):
            if board[piece[0] + available_move][piece[1]] in [white_pieces, black_pieces][team]:
                break
            available_moves.append([piece[0] + available_move, piece[1]])
            if board[piece[0] + available_move][piece[1]] in [white_pieces, black_pieces][team - 1]:
                break
        for available_move in range(1, 8 - piece[1]):
            if board[piece[0]][piece[1] + available_move] in [white_pieces, black_pieces][team]:
                break
            available_moves.append([piece[0], piece[1] + available_move])
            if board[piece[0]][piece[1] + available_move] in [white_pieces, black_pieces][team - 1]:
                break

# kings
    elif board[piece[0]][piece[1]] in [white_pieces[5], black_pieces[5]]:
        # castle
        if len(log) > 0 and len(piece) == 2 and len(['' for move in log if piece in move]) == 0:
            piece += ['', '']
            if len([empty for empty in board[piece[0]][1:piece[1]] if empty != '']) == 0:
                if len(['' for move in log if [piece[0], 0] in move]) == 0:
                    if [piece[0], piece[1] - 1] in search(board, log, [piece[0], piece[1], 'castle']):
                        board[piece[0]][piece[1] - 1], board[piece[0]][piece[1]] = board[piece[0]][piece[1]], ''
                        if [piece[0], piece[1] - 2] in search(board, log, [piece[0], piece[1] - 1, 'castle']) and [piece[0], piece[1]] in search(board, log, [piece[0], piece[1] - 1]):
                            available_moves.append([piece[0], piece[1] - 2])
                        board[piece[0]][piece[1]], board[piece[0]][piece[1] - 1] = board[piece[0]][piece[1] - 1], ''
            if len([empty for empty in board[piece[0]][piece[1] + 1:-1] if empty != '']) == 0:
                if len(['' for move in log if [piece[0], 7] in move]) == 0:
                    if [piece[0], piece[1] + 1] in search(board, log, [piece[0], piece[1], 'castle']):
                        board[piece[0]][piece[1] + 1], board[piece[0]][piece[1]] = board[piece[0]][piece[1]], ''
                        if [piece[0], piece[1]] in search(board, log, [piece[0], piece[1] + 1, 'castle']) and [piece[0], piece[1] + 2] in search(board, log, [piece[0], piece[1] + 1]):
                            available_moves.append([piece[0], piece[1] + 2])
                        board[piece[0]][piece[1]], board[piece[0]][piece[1] + 1] = board[piece[0]][piece[1] + 1], ''
            del piece[-2:]

        # normal move
        if piece[0] > 0:
            if not board[piece[0] - 1][piece[1]] in [white_pieces, black_pieces][team]:
                available_moves.append([piece[0] - 1, piece[1]])
            if piece[1] > 0:
                if not board[piece[0] - 1][piece[1] - 1] in [white_pieces, black_pieces][team]:
                    available_moves.append([piece[0] - 1, piece[1] - 1])
        if piece[0] < 7:
            if not board[piece[0] + 1][piece[1]] in [white_pieces, black_pieces][team]:
                available_moves.append([piece[0] + 1, piece[1]])
            if piece[1] < 7:
                if not board[piece[0] + 1][piece[1] + 1] in [white_pieces, black_pieces][team]:
                    available_moves.append([piece[0] + 1, piece[1] + 1])
        if piece[1] > 0:
            if not board[piece[0]][piece[1] - 1] in [white_pieces, black_pieces][team]:
                available_moves.append([piece[0], piece[1] - 1])
            if piece[0] < 7:
                if not board[piece[0] + 1][piece[1] - 1] in [white_pieces, black_pieces][team]:
                    available_moves.append([piece[0] + 1, piece[1] - 1])
        if piece[1] < 7:
            if not board[piece[0]][piece[1] + 1] in [white_pieces, black_pieces][team]:
                available_moves.append([piece[0], piece[1] + 1])
            if piece[0] > 0:
                if not board[piece[0] - 1][piece[1] + 1] in [white_pieces, black_pieces][team]:
                    available_moves.append([piece[0] - 1, piece[1] + 1])

# check detect
    if piece[-1] != 'verification':
        for y in range(8):
            for x in range(8):
                if board[y][x] == [white_pieces[5], black_pieces[5]][team]:
                    king = [y, x]
        for available_move in available_moves:
            if board[piece[0]][piece[1]] == [white_pieces[5], black_pieces[5]][team]:
                king = available_move
            for y in range(8):
                for x in range(8):
                    if board[y][x] in [white_pieces, black_pieces][team - 1]:
                        if board[y][x] in [white_pieces[5], black_pieces[5]] and board[piece[0]][piece[1]] in [white_pieces[5], black_pieces[5]] and available_move in available_moves:
                            if [abs(y - available_move[0]), abs(x - available_move[1])] in [[0, 1], [1, 1], [1, 0]]:
                                available_moves[available_moves.index(available_move)] = ''
                        elif board[y][x] != [white_pieces[5], black_pieces[5]][team - 1] and available_move in available_moves:
                            board[available_move[0]][available_move[1]], kopia = board[piece[0]][piece[1]], board[available_move[0]][available_move[1]]
                            board[piece[0]][piece[1]] = ''
                            if king in search(board, log, [y, x, 'verification']):
                                board[piece[0]][piece[1]] = board[available_move[0]][available_move[1]]
                                board[available_move[0]][available_move[1]] = kopia
                                available_moves[available_moves.index(available_move)] = ''
                            else:
                                board[piece[0]][piece[1]] = board[available_move[0]][available_move[1]]
                                board[available_move[0]][available_move[1]] = kopia
        while '' in available_moves:
            del available_moves[available_moves.index('')]

    return available_moves


def make(board, move):
    board = [element.copy() for element in board]
# promotion
    if len(move[1]) == 3:
        piece_color = 1
        if board[move[0][0]][move[0][1]] in white_pieces:
            piece_color = 0
        board[move[0][0]][move[0][1]] = ''
        board[move[1][0]][move[1][1]] = [white_pieces, black_pieces][piece_color][['N', 'B', 'R', 'Q'].index(move[1][2]) + 1]
# en passant
    elif board[move[0][0]][move[0][1]] in [white_pieces[0], black_pieces[0]] and board[move[1][0]][move[1][1]] == '' and move[0][0] != move[1][0]:
        board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
        board[move[0][0]][move[0][1]] = ''
        board[move[0][0]][move[1][1]] = ''
# castle
    elif board[move[0][0]][move[0][1]] in [white_pieces[5], black_pieces[5]] and abs(move[0][1] - move[1][1]) == 2:
        if move[1][1] < move[0][1]:
            board[move[1][0]][move[1][1]], board[move[0][0]][move[0][1]] = board[move[0][0]][move[0][1]], ''
            board[move[1][0]][move[1][1] + 1], board[move[1][0]][0] = board[move[1][0]][0], ''
        else:
            board[move[1][0]][move[1][1]], board[move[0][0]][move[0][1]] = board[move[0][0]][move[0][1]], ''
            board[move[1][0]][move[1][1] - 1], board[move[1][0]][7] = board[move[1][0]][7], ''
# normal move
    else:
        board[move[1][0]][move[1][1]], board[move[0][0]][move[0][1]] = board[move[0][0]][move[0][1]], ''

    return board
