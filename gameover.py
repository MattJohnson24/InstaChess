import chess

def game_status(board: chess.Board):
    outcome = board.outcome()
    winner = ""
    result = ""
    if outcome:
        if outcome.winner == chess.WHITE:
            winner = "White wins"
        elif outcome.winner == chess.BLACK:
            winner = "Black wins"
        else:
            winner = "Draw"
        if outcome.termination == chess.Termination.CHECKMATE:
            result = "CHECKMATE"
        elif outcome.termination == chess.Termination.INSUFFICIENT_MATERIAL:
            result = "INSUFFICIENT MATERIAL"
        elif outcome.termination == chess.Termination.STALEMATE:
            result = "STALEMATE"
        else:
            result = ""
        return winner, result
    else:
        return "", ""