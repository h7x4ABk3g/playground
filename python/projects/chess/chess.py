#!/bin/python3

from os import system
from dataclasses import dataclass

from board import Board
from piece import Piece


@dataclass
class Player:
  name: str
  color: str


class Chess:

  def __init__(self, players):
    self.players = players
    self.board = Board()

  def win(self, player):
    if player.color == 'white':
      print('''
░█░█░█░█░▀█▀░▀█▀░█▀▀░░░█░█░▀█▀░█▀█
░█▄█░█▀█░░█░░░█░░█▀▀░░░█▄█░░█░░█░█
░▀░▀░▀░▀░▀▀▀░░▀░░▀▀▀░░░▀░▀░▀▀▀░▀░▀
      ''')
    else:
      print('''
░█▀▄░█░░░█▀█░█▀▀░█░█░░░█░█░▀█▀░█▀█
░█▀▄░█░░░█▀█░█░░░█▀▄░░░█▄█░░█░░█░█
░▀▀░░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░▀░▀▀▀░▀░▀
      ''')
    input('Press any button to exit...')
    exit(0)

  def tie(self):
    print('''
░█▀▀░▀█▀░█▀█░█░░░█▀▀░█▄█░█▀█░▀█▀░█▀▀
░▀▀█░░█░░█▀█░█░░░█▀▀░█░█░█▀█░░█░░█▀▀
░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀
    ''')
    input('Press any button to exit...')
    exit(0)

  def promoteIfPossible(self, player, position):
    promoteY = 0 if player.color == 'white' else 7
    if (piece := self.board.getPieceAt(*position)).type == 'p' and position[1] == promoteY:
      while True:
        answer = input('What would you like your pawn to become? (q,b,r or n) ')
        if answer in 'qbrn' and len(answer) == 1:
          break
        else:
          print('\nCouldn\'t parse input. Try again')

      piece.type = answer


  def makeMove(self, player):
    # Get the first piece belonging to the player
    currentPlayersPiece = lambda piece: piece.color == player.color
    chosenTile = self.board.getPositionsWhere(currentPlayersPiece)[0]
    while True:
      piece = self.board.selectPiece(player, *chosenTile)
      chosenTile = piece
      possibleMoves = Piece.possibleMoves(*piece, self.board)
      if move := self.board.selectMove(player, *piece, possibleMoves):
        break
    self.board.movePiece(piece, move)
    self.promoteIfPossible(player, move)

  def turn(self, playerNum):
    system('clear')
    self.makeMove(players[playerNum])
    # 1 - 1 = 0 and 1 - 0 = 1
    if self.board.checkCheckMate(players[1 - playerNum].color):
      self.win(players[playerNum])
    elif self.board.checkStaleMate(players[1 - playerNum].color):
      self.tie()

  def loop(self):
    while True:
      self.turn(0)
      self.turn(1)


if __name__ == "__main__":

  players = (
    Player('Player 1', 'white'),
    Player('Player 2', 'black'),
  )

  game = Chess(('Player 1', 'Player 2'))
  game.loop()
