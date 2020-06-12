# maze
Generate random perfect mazes

In middle school we all wanted to write a dungeon game and that starts
with generating a maze.

A simple way to do it is to turn on walls randomly using random chance
but no matter what threshold you use the mazes end up looking spotty.

My mentor, Rob Kolstad, suggested and implemented an algorithm to
generate a perfect maze and tonight I reproduced it for my son, Liam,
who is teaching a programming class to middle schoolers this summer.

The algorithm is documented in the code itself.

Usage:

$ maze.py 20 40          # produces a 20x40 maze

$ maze.py 20 20 random   # produces a random maze with 55% of edges present.
