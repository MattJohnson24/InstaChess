#modified to have chess pieces instead of letters
#https://stackoverflow.com/a/59926492
def make_matrix(board): #type(board) == chess.Board()
    pgn = board.epd()
    foo = []  #Final board
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []  #This is the row I make
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('')
            else:
                pieces_dict = {
                    "P": "♙",
                    "R": "♖",
                    "N": "♘", 
                    "B": "♗",
                    "Q": "♕",
                    "K": "♔",
                    "p": "♟",
                    "r": "♜",
                    "n": "♞",
                    "b": "♝",
                    "q": "♛",
                    "k": "♚"
                    }
                foo2.append(pieces_dict[thing])
        foo.append(foo2)
    return foo