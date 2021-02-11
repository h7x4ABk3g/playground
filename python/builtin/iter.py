class Grid:
  def __init__(self, grid):
    self.grid = grid

  def __iter__(self):
    for row in self.grid:
      yield row

if __name__ == "__main__":
  myGrid = Grid([[(a,b) for a in range(3)] for b in range(3)])
  for x in myGrid:
    print(x)
