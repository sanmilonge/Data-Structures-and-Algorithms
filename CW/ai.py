from copy import deepcopy


def evaluate_board(game):
    score = 0
    size = len(game.board)
    for r in range(size):
        for c in range(size):
            piece = game.board[r][c]
            if piece == ".":
                continue

            if piece == 'c':
                score += 5
            elif piece == 'C':
                score += 10
            elif piece == 'b':
                score -= 5
            elif piece == 'B':
                score -= 10
            
            if 2 <= r <= size-3 and 2 <= c <= size-3:
                if piece.lower() == 'c':
                    score += 1
                else:
                    score -= 1

            if piece == 'c':
                score += r * 0.3
            elif piece == 'b':
                score -= (size - r) * 0.3

            if c == 0 or c == size-1:
                if piece.lower() == 'c':
                    score += 0.5
                else:
                    score -= 0.5

            ai_moves = len(game.get_all_moves('c'))
            player_moves = len(game.get_all_moves('b'))
            score += (ai_moves - player_moves) * 0.5
    return score


def get_next_states(game, player):
    """
    Returns all (move_summary, resulting_game) pairs for the given player.
    move_summary is ((start_row, start_col), (end_row, end_col)) representing
    the first and last position of the full chain (for animation purposes).

    For captures, full multi-jump chains are expanded so the AI evaluates
    complete jump sequences rather than single hops.
    For regular moves, each move is a single hop as before.
    """
    next_states = []

    # Check if any captures are available
    jump_chains = game.get_all_jump_chains(player)

    if jump_chains:
        # Only captures allowed — expand full chains
        for (start_row, start_col), chains in jump_chains.items():
            for chain in chains:
                # chain is [(r0,c0), (r1,c1), ..., (rN,cN)]
                # Execute each hop in sequence on a copy of the board
                new_game = deepcopy(game)
                valid = True

                for i in range(len(chain) - 1):
                    sr, sc = chain[i]
                    er, ec = chain[i + 1]
                    if not new_game.make_move(sr, sc, er, ec):
                        valid = False
                        break

                if valid:
                    # move summary: start -> final landing
                    move = ((start_row, start_col), (chain[-1][0], chain[-1][1]))
                    next_states.append((move, new_game, chain))

    else:
        # No captures — regular single-hop moves
        all_moves = game.get_all_moves(player)
        for (start_row, start_col), destinations in all_moves.items():
            for end_row, end_col in destinations:
                new_game = deepcopy(game)
                moved = new_game.make_move(start_row, start_col, end_row, end_col)
                if moved:
                    move = ((start_row, start_col), (end_row, end_col))
                    chain = [(start_row, start_col), (end_row, end_col)]
                    next_states.append((move, new_game, chain))

    return next_states


def minimax(game, depth, alpha, beta, maximizing_player):

    winner = game.check_winner()

    if depth == 0 or winner is not None:
        return evaluate_board(game), None, None

    # AI turn
    if maximizing_player:

        best_score = float("-inf")
        best_move = None
        best_chain = None

        for move, next_game, chain in get_next_states(game, "c"):

            score, _, _ = minimax(next_game, depth - 1, alpha, beta, False)

            if score > best_score:
                best_score = score
                best_move = move
                best_chain = chain

            alpha = max(alpha, score)

            if beta <= alpha:
                break

        return best_score, best_move, best_chain

    # Player turn
    else:

        best_score = float("inf")
        best_move = None
        best_chain = None

        for move, next_game, chain in get_next_states(game, "b"):

            score, _, _ = minimax(next_game, depth - 1, alpha, beta, True)

            if score < best_score:
                best_score = score
                best_move = move
                best_chain = chain

            beta = min(beta, score)

            if beta <= alpha:
                break

        return best_score, best_move, best_chain