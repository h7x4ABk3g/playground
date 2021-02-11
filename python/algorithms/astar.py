from math import inf, sqrt
from typing import Tuple

class BoolGrid:
  """
  A grid representing a coordinate system with blocked off squares.
  """

  def __init__(self, boolgrid):
    self.boolgrid = boolgrid

  def __str__(self):
    return "\n".join(
      "".join("." if b else "#" for b in row)
      for row in self.boolgrid
    )

  def __iter__(self):
    for row in self.boolgrid:
      yield row

  def y_len(self):
    return len(self.boolgrid)

  def x_len(self):
    return len(self.boolgrid[0])

  def get_bool_at(self, x, y) -> bool:
    return self.boolgrid[y][x]


class AStarNode:
  """
  Data structure for a node in the A* algorithm

  Attributes:
    h - the physical length from this node to the end point
    g - the minimum amount of steps needed to get to this node
    f - the sum of h and g

  Note: The f attribute is automatically generated based on h and g. DO NOT TRY TO SET THE F VALUE
  """

  def __init__(self, h):
    self.h = h
    self.g = inf
    self.parent_coords = None

  @property
  def f(self):
    return self.h + self.g


def main(boolgrid, start, end):


  def distance_between(coord1, coord2) -> float:
    """
    Calculate the H distance between two coordinates
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # return abs(x2-x1) + abs(y2-y1)


  def make_node_list():
    """
    Generate a list of nodes based on the length of the boolgrid
    """
    return [[ AStarNode(distance_between((x,y), end))
                if b else None
              for x, b   in enumerate(row)]
              for y, row in enumerate(boolgrid)]


  node_list = make_node_list()

  def get_node_at(x,y) -> AStarNode:
    """
    Fetches a node at the specified coordinate
    """

    if y in range(len(node_list)) and x in range(len(node_list[0])):
      return node_list[y][x]
    else:
      return None


  get_node_at(*start).g = 0

  open_list = [start]
  closed_list = []

  def print_node_list(path=[]):
    """
    Prints a map of the board to the terminal.
    If path is specified, it draws a path over the board
    """

    def node_string(node):
      clear_color    = "\033[0m"
      closed_color   = "\033[31m" # red
      open_color     = "\033[32m" # green
      special_color  = "\033[5;34m" # blue
      obstacle_color = "\033[33m" # yellow
      return \
        f'{obstacle_color}#{clear_color}' if get_node_at(*node) == None else \
        f'{special_color}S{clear_color}' if node == start else \
        f'{special_color}E{clear_color}' if node == end else \
        f'{special_color}*{clear_color}' if node in path else \
        f'{open_color}x{clear_color}' if node in open_list else \
        f'{closed_color}x{clear_color}' if node in closed_list else \
        'x'
    y_len = boolgrid.y_len()
    x_len = boolgrid.x_len()
    coordinates = [[(x,y) for x in range(x_len)]
                          for y in range(y_len)]
    
    print(
      "\n".join("".join(node_string(node) for node in row) for row in coordinates), '\n'
    )


  def update_neighbours(parent_coords):
    """
    Update all neighbours for a node with potential new shortest paths
    """

    px,py = parent_coords
    for x,y in [(1,0), (-1,0), (0,-1), (0,1)]:
      node_coords = (px+x, py+y)
      if get_node_at(*node_coords) is not None:
        calculate_node_values(node_coords, parent_coords)
    open_list.remove(parent_coords)
    closed_list.append(parent_coords)


  def calculate_node_values(node_coords, parent_coords) -> bool:
    """
    Add new shortest path to node and update values if it finds new shortest path.

    Returns whether it found a new shortest path
    """

    node = get_node_at(*node_coords)
    parent = get_node_at(*parent_coords)

    g = parent.g + 1
    if g < node.g: # This path is better.
      update_node(node_coords, parent_coords)


  def update_node(node_coords, parent_coords):
    """
    Update node values based on parent values and reinsert the node into open_list
    """

    node = get_node_at(*node_coords)
    parent = get_node_at(*parent_coords)

    node.parent_coords = parent_coords
    node.g = parent.g + 1

    # open_list = [coords for coords in open_list if coords != node_coords]
    insert_to_open_list(node_coords)


  def insert_to_open_list(node_coords):
    """
    O(n) function to insert node into open_list.
    """

    node = get_node_at(*node_coords)

    i = 0
    open_length = len(open_list)
    while node.f > get_node_at(*open_list[i]).f:
      if i + 1 == open_length:
        open_list.append(node_coords)
        return;
      i += 1
    open_list.insert(i, node_coords)


  def resolve_path(start_node_coords, end_node_coords) -> list[Tuple[int, int]]:
    """
    Get the list of coords from the start point to the end point
    """

    node = get_node_at(*end_node_coords)
    path = [end_node_coords]

    while node != get_node_at(*start_node_coords):
      node_coords = node.parent_coords
      path.insert(0, node_coords)
      node = get_node_at(*node_coords)

    return path

  while True:
    # print("\n".join(f"{coord} {get_node_at(*coord).__dict__}" for coord in open_list))
    #print_node_list()

    #input("enter")
    current_node_coords = open_list[0]
    if current_node_coords == end:
      print_node_list(resolve_path(start,end))
      return resolve_path(start, end)
    update_neighbours(current_node_coords)

if __name__ == '__main__':
  boolgrid = BoolGrid([[True, True, True, True],
                       [True, False, True, True],
                       [True, False, True, True],
                       [True, True, True, True]])

  cond = lambda a,b: all([
      not(a in range(70,80) and b in range(12,24)),
      not(a in range(0,40) and b in range(8,70)),
      not(a in range(40,70) and b in range(3,6)),
  ])
  bg = [[cond(a,b) for a in range(100)]for b in range(100)]

  print(main(BoolGrid(bg), (0,0), (81,80)))
