#!/usr/bin/env python3

import sys

CELL_SIZE = 10
CELL_BORDER = 1
CELL_OUTER_SIZE = CELL_SIZE + 2 * CELL_BORDER

def increment_state():
    with open('resources/state', 'r') as state_file:
        state = [[char != ' ' for char in line.strip('\n')] for line in state_file]
        if len(set(len(row) for row in state)) != 1 or len(state) == 0:
            sys.stderr.write('Failed to read state file\n')
            exit(1)
    
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

    with open('resources/state', 'w') as state_file:
        state_file.write('\n'.join([''.join(['*' if cell else ' ' for cell in row]) for row in new_state]))

    return new_state

def generate_svg(state):
    height = len(state)
    width = len(state[0])

    with open('resources/game-of-life.svg', 'w') as output_svg:
        output_svg.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width * CELL_OUTER_SIZE}px" height="{height * CELL_OUTER_SIZE}px" viewBox="0 0 {width * CELL_OUTER_SIZE} {height * CELL_OUTER_SIZE}" version="1.1">\n')
        output_svg.write('<rect width="100%" height="100%" fill="black"/>')
        for y in range(height):
            for x in range(width):
                output_svg.write(f'<rect x="{x * CELL_OUTER_SIZE + CELL_BORDER}" y="{y * CELL_OUTER_SIZE + CELL_BORDER}" width="{CELL_SIZE}" height="{CELL_SIZE}"\nfill="{'white' if state[y][x] else 'black'}"\n/>\n')

        output_svg.write('</svg>\n')

def main():
    state = increment_state()
    generate_svg(state)

if __name__ == '__main__':
    main()
