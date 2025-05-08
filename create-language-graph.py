#!/usr/bin/env python3
import matplotlib.pyplot as plt
import sys

SPACING = 0.005
HEIGHT = 0.4

def main():
    _, ax = plt.subplots(figsize=(10, 3))
    plt.gca().set_facecolor('none')
    plt.gcf().set_facecolor('#0d1117')

    def to_tuple(s: str):
        fields = s.split(',')
        return (fields[0], float(fields[1]), fields[2])

    try:
        data = list(map(to_tuple, sys.stdin.read().strip('\n').split()))
        assert(len(data) > 0)
    except:
        sys.stderr.write('No suitable data received\n')
        exit(1)

    left = 0

    for label, width, color in data:
        ax.barh(0, max(width - SPACING, 0), HEIGHT, left=left, color=color, label=label)
        left += width

    ax.axis('off')
    ax.set_ylim(1 - HEIGHT, 0)
    ax.legend(bbox_to_anchor=(0, 0, 1, HEIGHT), loc='lower center', ncols=3, frameon=False, fontsize=14, labelcolor='#f0f6fc')

    plt.savefig('language-graph.svg', bbox_inches='tight')

if __name__ == '__main__':
    main()
