from typing import Iterable, Callable
from itertools import product
from copy import deepcopy


class Piece:

  def __init__(self, type, color):
    self.type = type
    self.color = color

  def __str__(self):
    return self.type.upper() if self.color == 'white' else self.type

  # Unused code. I'm missing the font for my terminal, but go ahead and use piece.symbol instead of str(symbol) in board.draw if you'd like
  @property
  def symbol(self):
    symbols = [{
      'p': '♙',
      'r': '♖',
      'n': '♘',
      'b': '♗',
      'q': '♕',
      'k': '♔',
    }, {
      'p': '♟︎',
      'r': '♜',
      'n': '♞',
      'b': '♝',
      'q': '♛',
      'k': '♚',
    }]
    return symbols[0 if self.color == 'white' else 1][self.type]

  @staticmethod
  def possibleMoves(
    x,
    y,
    board,
    legalMoves=None,
    simulation=False,
  ) -> Callable[[int, int], Iterable[tuple]]:
    """
      Calculate all possible moves for a piece at (x, y) given a board in a certain state.

      If there is restrictions for where the piece can go, the legal moves can be set to these.
      If the function is part of a simulation, simulation needs to be set to True so that it doesn't keep on recursing simulation indefinetely.
    """

    piece = board.getPieceAt(x, y)
    moves = []

    pieceIsEnemyColor = lambda pieceToCheck: pieceToCheck != None and pieceToCheck.color != piece.color
    pieceIsEmpty = lambda pieceToCheck: pieceToCheck == None
    pieceIsEmptyOrEnemyColor = lambda pieceToCheck: pieceToCheck == None or pieceToCheck.color != piece.color
    positionInsideBounds = lambda x, y: x in range(8) and y in range(8)

    def addMoveIfTrue(xOffset, yOffset, condition: Callable[[Piece], bool]) -> bool:
      """Tests a condition against a position away from self. Adds move if condition returns true. Returns condition result"""
      if condition(board.getPieceAt(x + xOffset, y + yOffset)):
        moves.append((x + xOffset, y + yOffset))
        return True
      return False

    def assertNotCheck(newX, newY) -> bool:
      """Simulate a move and return whether or not the move will result in check"""
      testBoard = deepcopy(board)
      testBoard.movePiece((x, y), (newX, newY))
      return not testBoard.checkCheck(piece.color, simulation=True)

    def addWhileInsideBoard(direction: tuple):
      """Adds moves in direction until it either hits a piece or the edge"""
      localX, localY = x, y
      while positionInsideBounds(localX, localY):
        localX += direction[0]
        localY += direction[1]
        currentPiece = board.getPieceAt(localX, localY)
        if pieceIsEmpty(currentPiece):
          moves.append((localX, localY))
        else:
          if pieceIsEnemyColor(currentPiece):
            moves.append((localX, localY))
          return

    if piece.type == 'p':
      localY = 1 if piece.color == 'black' else -1
      startPosition = 1 if piece.color == 'black' else 6
      pieceAtStartPosition = lambda pieceToCheck: pieceToCheck == None and y == startPosition

      addMoveIfTrue(1, localY, pieceIsEnemyColor)
      addMoveIfTrue(-1, localY, pieceIsEnemyColor)
      if addMoveIfTrue(0, localY, pieceIsEmpty):
        addMoveIfTrue(0, localY * 2, pieceAtStartPosition)

    elif piece.type == 'n':
      positions = [
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
      ]
      for position in positions:
        addMoveIfTrue(*position, pieceIsEmptyOrEnemyColor)

    elif piece.type == 'k':
      positions = list(product([-1, 0, 1], repeat=2))
      positions.remove((0, 0))
      for position in positions:
        addMoveIfTrue(*position, pieceIsEmptyOrEnemyColor)

    elif piece.type == 'r':
      for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        addWhileInsideBoard(direction)

    elif piece.type == 'b':
      for direction in product([-1, 1], repeat=2):
        addWhileInsideBoard(direction)

    elif piece.type == 'q':
      directions = list(product([-1, 0, 1], repeat=2))
      directions.remove((0, 0))
      for direction in directions:
        addWhileInsideBoard(direction)

    # Remove moves that will lead the piece out of the board
    moves = [move for move in moves if positionInsideBounds(*move)]

    # Remove moves that is not included in the legal moves (moves to block check)
    if legalMoves != None and piece.type != 'k':
      moves = [move for move in moves if move in legalMoves]

    # Remove moves that will put the king in check
    if not simulation:
      moves = [position for position in moves if assertNotCheck(*position)]

    return moves
