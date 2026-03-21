from copy import deepcopy


def evaluate_board(game):
    score = 0
    size = len(game.board)
    for r in range(size):
        for c in range(size):
            piece = game.board[r][c]
            if piece == ".": # Empty piece
                continue

            # Base piece value
            if piece == 'c':
                score += 5
            elif piece == 'C':
                score += 10
            elif piece == 'b':
                score -= 5
            elif piece == 'B':
                score -= 10
            
            # Central control
            if 2 <= r <= size-3 and 2 <= c <= size-3:
                if piece.lower() == 'c':
                    score += 1
                else:
                    score -= 1

            # Advancement
            if piece == 'c':
                score += r * 0.3
            elif piece == 'b':
                score -= (size - r) * 0.3

            # Edge safety
            if c == 0 or c == size-1:
                if piece.lower() == 'c':
                    score += 0.5
                else:
                    score -= 0.5

            # Mobility
            ai_moves = len(game.get_all_moves('c'))
            player_moves = len(game.get_all_moves('b'))
            score += (ai_moves - player_moves) * 0.5
    return score


def get_next_states(game, player):
    next_states = []
    all_moves = game.get_all_moves(player)

    for (start_row, start_col), destinations in all_moves.items():
        for end_row, end_col in destinations:
            new_game = deepcopy(game)

            moved = new_game.make_move(start_row, start_col, end_row, end_col)

            if moved:
                move = ((start_row, start_col), (end_row, end_col))
                next_states.append((move, new_game))

    return next_states


def minimax(game, depth, alpha, beta, maximizing_player):

    winner = game.check_winner()

    if depth == 0 or winner is not None:
        return evaluate_board(game), None

    # AI turn
    if maximizing_player:

        best_score = float("-inf")
        best_move = None

        for move, next_game in get_next_states(game, "c"):

            score, _ = minimax(next_game, depth - 1, alpha, beta, False)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)

            if beta <= alpha:
                break

        return best_score, best_move


    # Player turn
    else:

        best_score = float("inf")
        best_move = None

        for move, next_game in get_next_states(game, "b"):

            score, _ = minimax(next_game, depth - 1, alpha, beta, True)

            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, score)

            if beta <= alpha:
                break

        return best_score, best_move