from typing import Callable, Iterable, Union
from os import system
from shutil import get_terminal_size as getTerminalSize

from piece import Piece


def centerText(text):
  terminalWidth = getTerminalSize((60, 0))[0]   # Column size 60 as fallback
  return "\n".join(line.center(terminalWidth) for line in text.split('\n'))


def centerBlockText(text):
  terminalWidth = getTerminalSize((60, 0))[0]   # Column size 60 as fallback
  textArray = text.split('\n')
  offset = int((terminalWidth - len(textArray[0])) / 2)
  return "\n".join(offset * ' ' + line for line in textArray)


def determineMove(key, x, y, maxmin) -> tuple:
  if key in ['s', 'j'] and y != maxmin[1]: return (0, 1)
  elif key in ['w', 'k'] and y != maxmin[0]: return (0, -1)
  elif key in ['d', 'l'] and x != maxmin[1]: return (1, 0)
  elif key in ['a', 'h'] and x != maxmin[0]: return (-1, 0)
  else: return False


class Board:

  def __init__(self, boardState=None):
    """Create a standard board if nothing else is defined in boardState"""
    self.boardArray = [
      [Piece(type, 'black') for type in ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']],
      [Piece('p', 'black') for _ in range(8)],
      *[[None for _ in range(8)] for _ in range(4)],
      [Piece('p', 'white') for _ in range(8)],
      [Piece(type, 'white') for type in ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']],
    ] if boardState == None else boardState

  def draw(self, config={}) -> str:
    """Returns a string representing the board

    config options:
      highlightedContent: [(x,y)] - Pieces to color
      highlightEscapeCodes: (str, str) - Terminal escape codes to color highlightedContent with
      highlightedBoxes: [(x,y)] - Boxes to make bold
    """

    # Fill default values in config dict
    def fillConfigDefaultValue(key, defaultValue):
      if key not in config:
        config[key] = defaultValue

    fillConfigDefaultValue('highlightedContent', [])
    fillConfigDefaultValue('highlightedBoxes', [])
    fillConfigDefaultValue('highlightEscapeCodes', ('\033[32;5;7m', '\033[0m'))

    # Draw general outline with ┼ as all corners
    stringArray = [list('┼' + '───┼' * 8)] + [[None] for _ in range(8 * 2)]
    for y, row in enumerate(self.boardArray):
      for x, _ in enumerate(row):
        stringArray[2 * y + 1][4 * x] = '│'
        stringArray[2 * y + 2][4 * x] = '┼'

        symbol = str(self.boardArray[y][x]) if self.boardArray[y][x] != None else ' '
        stringArray[2 * y + 1] += list(' {} │'.format(symbol))
        stringArray[2 * y + 2] += list('───┼')

    # Overwrite corners
    stringArray[0][0] = '╭'
    stringArray[0][-1] = '╮'
    stringArray[-1][0] = '╰'
    stringArray[-1][-1] = '╯'

    # Overwrite T-junctions
    for i in range(int(len(stringArray[0]) / 4) - 1):   # Loop row
      stringArray[0][i * 4 + 4] = '┬'
      stringArray[-1][i * 4 + 4] = '┴'
    for i in range(int(len(stringArray) / 2) - 1):   # Loop column
      stringArray[i * 2 + 2][0] = '├'
      stringArray[i * 2 + 2][-1] = '┤'

    def highlightContent(x, y, modifiers=config['highlightEscapeCodes']):
      """highlight inner part of a box with xterm-256colors modifiers"""
      stringArray[y * 2 + 1][x * 4 + 1] = \
        modifiers[0] + stringArray[y * 2 + 1][x * 4 + 1]
      stringArray[y * 2 + 1][x * 4 + 3] += modifiers[1]

    def highlightBox(x, y):
      """Make box around a position bold"""

      boldBoxChars = {
        '─': '═',
        '│': '║',
        '┼': '╬',
        '╰': '╚',
        '╯': '╝',
        '╭': '╔',
        '╮': '╗',
        '├': '╠',
        '┴': '╩',
        '┤': '╣',
        '┬': '╦',
      }

      pointsToChange = \
      [(x * 4 + 0, y * 2 + i) for i in range(3)] + \
      [(x * 4 + 4, y * 2 + i) for i in range(3)] + \
      [(x * 4 + i, y * 2 + 0) for i in range(1,4)] + \
      [(x * 4 + i, y * 2 + 2) for i in range(1,4)]

      # This has to doublecheck that the character exists, because if neighbour
      # boxes are to be highlighed, it will try to overwrite already bold borders
      for x, y in pointsToChange:
        symbolExists = stringArray[y][x] in boldBoxChars
        stringArray[y][x] = boldBoxChars[stringArray[y][x]] if symbolExists else stringArray[y][x]

    # Color white pieces
    for piece in self.getPositionsWhere(lambda piece: piece.color == 'white'):
      highlightContent(*piece, ('\033[7m', '\033[0m'))

    for box in config['highlightedBoxes']:
      highlightBox(*box)

    for piece in config['highlightedContent']:
      highlightContent(*piece)

    return '\n'.join([''.join(line) for line in stringArray])

  def selectPiece(self, player, x=0, y=0, centering=True) -> tuple:
    """Lets the user select a piece"""

    while True:
      system('clear')
      playerString = '\n' + player.name + '\n'
      checkString = f"\033[41m{'CHECK' if self.checkCheck(player.color) else ''}\033[0m" + '\n'

      hoveringPiece = self.getPieceAt(x, y)
      pieceIsOwnColor = hoveringPiece != None and hoveringPiece.color == player.color

      menuString = self.draw({
        'highlightedBoxes': [(x, y)],
        'highlightedContent': Piece.possibleMoves(x, y, self) if pieceIsOwnColor else []
      }) + '\n'
      inputString = f"  W E\nA S D  <- Enter : "

      if centering:
        playerString = centerText(playerString)
        checkString = centerText(checkString)
        menuString = centerBlockText(menuString)
        inputString = centerBlockText(inputString)

      print(playerString)
      print(checkString)
      print(menuString)

      try:
        key = input(inputString)[0]
      except IndexError:   # Input was empty
        key = ''

      try:
        if move := determineMove(key, x, y, (0, 7)):
          x += move[0]
          y += move[1]
        elif key == 'e' \
          and hoveringPiece.color == player.color \
          and Piece.possibleMoves(x, y, self) != []:
          return (x, y)
      except AttributeError:   # Chosen tile contains no piece
        pass

  def selectMove(self, player, x, y, legalMoves, centering=True) -> Union[tuple, bool]:
    """Lets the user select a move to make from a graphic board"""

    while True:
      system('clear')
      playerString = '\n' + player.name + '\n'
      checkString = f"\033[41m{'CHECK' if self.checkCheck(player.color) else ''}\033[0m" + '\n'
      menuString = self.draw({
        'highlightedBoxes': [(x, y)],
        'highlightedContent': legalMoves
      }) + '\n'
      inputString = f"Q W E\nA S D  <- Enter : "

      if centering:
        playerString = centerText(playerString)
        checkString = centerText(checkString)   #TODO: Doesn't center because of escape chars
        menuString = centerBlockText(menuString)
        inputString = centerBlockText(inputString)

      print(playerString)
      print(checkString)
      print(menuString)

      try:
        key = input(inputString)[0]
      except IndexError:   # Input was empty
        key = ''

      if move := determineMove(key, x, y, (0, 7)):
        x += move[0]
        y += move[1]
      elif key == 'q':
        return False
      elif key == 'e' and (x, y) in legalMoves:
        return (x, y)

  def getPieceAt(self, x, y) -> Union[Piece, None]:
    """Gets a piece at a certain position"""
    try:
      return self.boardArray[y][x]
    except IndexError:   # Outside board
      return None

  def getPositionsWhere(self, condition: Callable[[Piece], bool]) -> Iterable[tuple]:
    """Returns a list of xy pairs of the pieces where a condition is met """

    result = []
    for y, row in enumerate(self.boardArray):
      for x, piece in enumerate(row):
        try:
          if condition(piece):
            result.append((x, y))
        except AttributeError:   # Position is None
          pass
    return result

  def checkCheck(self, color, simulation=False) -> bool:
    """Check whether a team is caught in check. The color is the color of the team to check"""
    king = self.getPositionsWhere(lambda piece: piece.type == 'k' and piece.color == color)[0]
    piecesToCheck = self.getPositionsWhere(lambda piece: piece.color != color)
    # Resend simulation status into possibleMoves in order to avoid indefinite recursion
    return any(
      king in Piece.possibleMoves(*piece, self, simulation=simulation) for piece in piecesToCheck)

  def getPositionsToProtectKing(self, color) -> Iterable[tuple]:
    """Get a list of the positions to protect in order to protect the king when in check. The color is the color of the team who's in check"""
    king = self.getPositionsWhere(lambda piece: piece.type == 'k' and piece.color == color)[0]
    piecesToCheck = self.getPositionsWhere(lambda piece: piece.color != color)

    # Get all pieces that threaten the king
    piecesToCheck = [piece for piece in piecesToCheck if king in Piece.possibleMoves(*piece, self)]

    # Add only self if piece is pawn, knight or king
    result = []
    for piece in piecesToCheck:
      result.append([piece])
      if self.getPieceAt(*piece).type not in ['p', 'n', 'k']:

        def getDirection(fromPosition, toPosition) -> tuple:
          """Get the direction as a tuple from the threatening piece to the king"""
          x = -1 if toPosition[0] > fromPosition[0] else \
            0 if toPosition[0] == fromPosition[0] else 1
          y = -1 if toPosition[1] > fromPosition[1] else \
            0 if toPosition[1] == fromPosition[1] else 1
          return (x, y)

        def getPositionsUntilKing(x, y, direction) -> Iterable[tuple]:
          """Return a list of every position until the king"""
          result = []
          x += direction[0]
          y += direction[1]
          while self.getPieceAt(x, y) == None:
            result.append((x, y))
            x += direction[0]
            y += direction[1]
          return result

        direction = getDirection(piece, king)
        result[-1] += getPositionsUntilKing(*king, direction)

    def getCommonValues(lst: Iterable[Iterable[tuple]]):
      """Combine lists so that only tuples in all the lists of threatening pieces are valid"""
      result = set(lst[0])
      for sublst in lst[1:]:
        result.intersection_update(sublst)
      return result

    return getCommonValues(result)

  def playerHasLegalMoves(self, color) -> bool:
    """ returns whether or not a player has any legal moves left"""
    enemyPieces = self.getPositionsWhere(lambda piece: piece.color == color)
    if self.checkCheck(color):
      getLegalMoves = lambda piece: Piece.possibleMoves(
        *piece, self, legalMoves=self.getPositionsToProtectKing(color))
    else:
      getLegalMoves = lambda piece: Piece.possibleMoves(*piece, self)

    return any(getLegalMoves(piece) != [] for piece in enemyPieces)

  def checkStaleMate(self, color) -> bool:
    """Check whether a team is caught in stalemate. The color is the color of the team to check"""
    return (not self.checkCheck(color)) and not self.playerHasLegalMoves(color)

  def checkCheckMate(self, color) -> bool:
    """Check whether a team is caught in checkmate. The color is the color of the team to check"""
    return self.checkCheck(color) and not self.playerHasLegalMoves(color)

  def movePiece(self, position, toPosition, piecesToRemove=[]):
    """ Move a piece from position to toPosition. In case of extra pieces to be removes, add them to the list piecesToRemove"""
    x, y = position
    toX, toY = toPosition
    self.boardArray[toY][toX] = self.boardArray[y][x]
    self.boardArray[y][x] = None

    for x, y in piecesToRemove:
      self.boardArray[y][x] = None
