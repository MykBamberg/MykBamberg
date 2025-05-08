#!/usr/bin/env python3

import random

def main():
    with open('state', 'r') as state_file:
        state = [[char != ' ' for char in line.strip('\n')] for line in state_file]
        if len(set(len(row) for row in state)) != 1 or len(state) == 0:
            state = [[random.choice((True, False)) for _ in range(16)] for _ in range(16)]
    
    height = len(state)
    width = len(state[0])

    def new_cell(x, y):
        offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        count = 0

        for offx, offy in offsets:
            cellx = (offx + x) % width
            celly = (offy + y) % height
            if state[celly][cellx]:
                count += 1

        if state[y][x]:
            return count in [2, 3]
        else:
            return count in [3]

    new_state = [[new_cell(x, y) for x in range(width)] for y in range(height)]

    with open('state', 'w') as state_file:
        state_file.write('\n'.join([''.join(['*' if cell else ' ' for cell in row]) for row in new_state]))

if __name__ == '__main__':
    main()
