#!/usr/bin/env python3

CELL_SIZE = 10
CELL_BORDER = 1
CELL_OUTER_SIZE = CELL_SIZE + 2 * CELL_BORDER

def main():
    with open('state', 'r') as state_file:
        state = [[char != ' ' for char in line.strip('\n')] for line in state_file]
        if len(set(len(row) for row in state)) != 1 or len(state) == 0:
            exit(1)
    
    height = len(state)
    width = len(state[0])

    with open('game-of-life.svg', 'w') as state_file:
        state_file.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width * CELL_OUTER_SIZE}px" height="{height * CELL_OUTER_SIZE}px" viewBox="0 0 {width * CELL_OUTER_SIZE} {height * CELL_OUTER_SIZE}" version="1.1">\n')
        state_file.write('<rect width="100%" height="100%" fill="black"/>')
        for y in range(height):
            for x in range(width):
                state_file.write(f'<rect x="{x * CELL_OUTER_SIZE + CELL_BORDER}" y="{y * CELL_OUTER_SIZE + CELL_BORDER}" width="{CELL_SIZE}" height="{CELL_SIZE}"\nfill="{'white' if state[y][x] else 'black'}"\n/>\n')

        state_file.write('</svg>\n')

if __name__ == '__main__':
    main()
