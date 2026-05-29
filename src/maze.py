#!/usr/bin/env python3
import argparse
import random

# program to generate a maze.
#
# a maze is an n (rows) x k (columns) array of cells.
#
#   each cell is a place where a person (or monster!) can live.
#   each cell has an above, below, left, and right wall.
#
#   try it on a 1x1 maze!  You need 2x1 horizontal walls and 1x2 vertical walls!
#
#   because there are n rows, we have n above-walls and 1 extra below walls.
#   because there are k cols, we have k left-walls and 1 right walls.
#
#   so the maze needs (n+1) above/below walls (times k columns)
#   and the maze needs (k+1) left/right walls (times n rows)

DEFAULT_ROWS = 30
DEFAULT_COLS = 30

def rand():
  return random.random() < 0.45

def always():
  return 1

def new_random_maze(rows, cols, func):
  #              === columns ===      x   == rows ===
  hwall = [ [ func() for i in range(cols)] for j in range(rows+1) ]
  vwall = [ [ func() for i in range(cols+1)] for j in range(rows) ]
  return hwall, vwall

def new_perfect_maze(rows, cols, debug = False):
  # a perfect maze has only ONE path from point A to point B.
  # we start with a maze that is 100% filled with walls !!
  hwall, vwall = new_random_maze(rows, cols, always)
  #
  # now we make an n x k matrix with a unique number in each cell.
  # the number represents where we can walk from here (nowhere).
  grid = [ [ 0 for i in range(cols) ] for j in range(rows) ] if debug else None
  # use 3-digit markers ("count") so debug mazes < 900 cells have all cells 3 chars wide.
  count = 100
  if debug:
    for i in range(rows):
      for j in range(cols):
        grid[i][j] = count
        count = count + 1
  #
  # these compass points represent an adjacent cell.  direction =
  #    north(0), south(1), east(2), west(3)
  NORTH = 0
  SOUTH = 1
  EAST = 2
  WEST = 3

  # we will pick one of these 4 compass points and this is
  # how the cell changes (row,col) for each of the 4 dirs NSEW:
  #         north   south     east   west
  deltas = [(-1, 0), (1, 0), (0, 1), (0, -1)]

  parent = [i for i in range(rows * cols)]

  def cell_id(row, col):
    return row * cols + col

  def find(cell):
    while parent[cell] != cell:
      parent[cell] = parent[parent[cell]]
      cell = parent[cell]
    return cell

  def union(cell, other):
    cell_root = find(cell)
    other_root = find(other)
    if cell_root == other_root:
      return False
    parent[cell_root] = other_root
    return True

  if (debug):
    print_maze(rows, cols, hwall, vwall, grid, debug = True)

  walls = []
  for row in range(rows):
    for col in range(cols):
      if row > 0:
        walls.append((row, col, NORTH))
      if col > 0:
        walls.append((row, col, WEST))
  random.shuffle(walls)

  remaining_groups = rows * cols
  while remaining_groups > 1:
    (row, col, direction) = walls.pop()
    (delta_row, delta_col) = deltas[direction]
    adjacent_row = row + delta_row
    adjacent_col = col + delta_col

    # is there already a path from (row,col) to the adjacent cell?
    if not union(cell_id(row, col), cell_id(adjacent_row, adjacent_col)):
      continue

    # else find and delete the wall separating both cells.
    if direction == NORTH:
      hwall[row][col] = 0
    if direction == SOUTH:
      hwall[row+1][col] = 0
    if direction == EAST:
      vwall[row][col+1] = 0
    if direction == WEST:
      vwall[row][col] = 0

    if (debug):
      # Merge debug markers so the printed trace shows connected regions.
      marker = grid[row][col]
      new_marker = grid[adjacent_row][adjacent_col]
      print("combining ", marker, new_marker)
      for i in range(rows):
        for j in range(cols):
          if grid[i][j] == marker:
            grid[i][j] = new_marker

      print('')
      print_maze(rows, cols, hwall, vwall, grid, True)
    remaining_groups = remaining_groups - 1

  return hwall, vwall, grid

def add_walls(rows, cols, hwall, vwall):
  for i in range(rows):
    vwall[i][0] = 1
    vwall[i][len(vwall[0]) - 1] = 1

  for i in range(cols):
    hwall[0][i] = 1
    hwall[len(hwall) - 1][i] = 1

def print_maze(rows, cols, hwall, vwall, grid = None, debug = False):
  for row in range(0, rows + 1):
    for col in range(0, cols):
      print('+', end='')
      print( '===' if hwall[row][col] > 0 else '   ', end='')
    print('+')

    if row != rows:      # there are only n rows of vertical walls.
      for col in range(0, cols + 1):
        if not debug:
          print( '|   ' if vwall[row][col] > 0 else '    ', end='')
        else:
          if col < cols:
            if vwall[row][col] > 0:
              print('|' + str(grid[row][col]), end='')
            else:
              print(' ' + str(grid[row][col]), end='')
          else:
            print( '|   ' if vwall[row][col] > 0 else '    ', end='')
      print('')


def positive_int(value):
  try:
    number = int(value)
  except ValueError:
    raise argparse.ArgumentTypeError("must be an integer")
  if number < 1:
    raise argparse.ArgumentTypeError("must be at least 1")
  return number

def parse_args():
  parser = argparse.ArgumentParser(description="Generate random mazes.")
  parser.add_argument("rows", nargs="?", type=positive_int, default=DEFAULT_ROWS)
  parser.add_argument("cols", nargs="?", type=positive_int, default=DEFAULT_COLS)
  parser.add_argument("maze_type", nargs="?", choices=["perfect", "random"], default="perfect")
  return parser.parse_args()

def main():
  args = parse_args()

  if (args.maze_type == 'random'):
    hwall, vwall = new_random_maze(args.rows, args.cols, rand)
    grid = None
  else:
    hwall, vwall, grid = new_perfect_maze(args.rows, args.cols, False)

  add_walls(args.rows, args.cols, hwall, vwall)
  print_maze(args.rows, args.cols, hwall, vwall, grid)

if __name__ == "__main__":
  main()
