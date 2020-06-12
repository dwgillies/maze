from __future__ import print_function
import random
import sys

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

n = 40     # maze of 20 rows, 30 columns
k = 40

def rand():
  return random.getrandbits(10) > 900

def always():
  return 1

def new_maze(func):
  global vwall, hwall

  #              === columns ===                          x   == rows ===
  hwall = [ [ func() for i in range(k)] for j in range(n+1) ]
  vwall = [ [ func() for i in range(k+1)] for j in range(n) ]

def new_perfect_maze(debug = False):
  global vwall, hwall
  # a perfect maze has only ONE path from point A to point B.
  # we start with a maze that is 100% filled with walls !!
  new_maze(always)
  #
  # now we make an n x k matrix with a unique number in each cell.
  # the number represents where we can walk from here (nowhere).
  global map
  map = [ [ 0 for i in range(k) ] for j in range(n) ]
  count = 100
  for i in range(n):
    for j in range(k):
      map[i][j] = count
      count = count + 1
  #
  # now pick a random pair of adjecnt cell.  direction =
  #    north(0), south(1), east(2), west(3)
  NORTH = 0
  SOUTH = 1
  EAST = 2
  WEST = 3

  # we will pick one of these 4 compass points and this is
  # how the cell changes (row,col) for each of the 4 dirs NSEW:
  #         north   south     east   west
  deltas = [(-1, 0), (1, 0), (0, 1), (0, -1)]

  if (debug):
    print_maze(debug = True)

  while (count > 101):
    # pick a random cell
    row = random.randrange(0, n)
    col = random.randrange(0, k)

    # pick a random 4-compass points direction
    direction = random.randrange(0, 3)

    # get the change to the adjacent cell
    (delta_row, delta_col) = deltas[direction]

    # would the adjacent cell take us off the map?
    if row + delta_row not in range(0, n): continue
    if col + delta_col not in range(0, k): continue

    # is there already a path from (row,col) to the adjacent cell?
    if map[row][col] == map[row + delta_row][col + delta_col]:
      continue

    # else figure out where it is and delete the wall.
    if direction == NORTH:
      hwall[row][col] = 0
    if direction == SOUTH:
      hwall[row+1][col] = 0
    if direction == EAST:
      vwall[row][col+1] = 0
    if direction == WEST:
      vwall[row][col] = 0

    # now merge the markers of both cells, to yield 1 less marker.
    # whatever marker we find in map[row,col], it will replace the
    # all markers fo the type map[row + delta_row, col + delta_col]
    # indicating there is now a path from each cell on one side of the
    # wall to each cell on the other side of the deleted wall.
    marker = map[row][col]
    new_marker = map[row + delta_row][col + delta_col]
    if (debug):
      print("combining ", marker, new_marker)

    for i in range(n):
      for j in range(k):
        if map[i][j] == marker:
          map[i][j] = new_marker

    if (debug):
      print('')
      print_maze(True)
    count = count - 1

def add_walls():
  global vwall, hwall

  for i in range(n):
    vwall[i][0] = 1
    vwall[i][len(vwall[0]) - 1] = 1

  for i in range(k):
    hwall[0][i] = 1
    hwall[len(hwall) - 1][i] = 1

def print_maze(debug = False):
  global vwall, hwall

  for row in range(0, n + 1):
    for col in range(0, k):
      print('+', end='')
      print( '===' if hwall[row][col] > 0 else '   ', end='')
    print('+')

    if row != n:      # there are only n rows of vertical walls.
      for col in range(0, k + 1):
        if not debug:
          print( '|   ' if vwall[row][col] > 0 else '    ', end='')
        else:
          if col < k:
            if vwall[row][col] > 0:
              print('|' + str(map[row][col]), end='')
            else:
              print(' ' + str(map[row][col]), end='')
          else:
            print( '|   ' if vwall[row][col] > 0 else '    ', end='')
      print('')


# new_maze(rand)
if len(sys.argv) > 1:
  n = int(sys.argv[1])
if len(sys.argv) > 2:
  k = int(sys.argv[2])

new_perfect_maze(False)
add_walls()
print_maze()
