#!/usr/bin/env python3

import os
import asyncio
import sys
import aiohttp
from datetime import datetime, timezone
import matplotlib.pyplot as plt

AGE_WEIGHT = 0.9
LENGTH_WEIGHT = 0.5
EXCLUDE = ['Shell', 'Batchfile', 'Makefile', 'CMake', 'Meson', 'Roff', 'HTML', 'CSS', 'Vim Script', 'M4']
MAX_COUNT = 12

QUERY = '''
{
  viewer {
    repositories(first: 100, isFork: false) {
      nodes {
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
        pushedAt
      }
    }
  }
}
'''

SPACING = 0.005
HEIGHT = 0.4

def generate_graph(data):
    _, ax = plt.subplots(figsize=(10, 3))
    plt.gca().set_facecolor('none')
    plt.gcf().set_facecolor('#0d1117')

    left = 0

    for label, width, color in data:
        ax.barh(0, max(width - SPACING, 0), HEIGHT, left=left, color=color, label=label)
        left += width

    ax.axis('off')
    ax.set_ylim(1 - HEIGHT, 0)
    ax.legend(bbox_to_anchor=(0, 0, 1, HEIGHT), loc='lower center', ncols=3, frameon=False, fontsize=14, labelcolor='#f0f6fc')
    ax.margins(x=0)

    plt.savefig('resources/language-graph.svg', bbox_inches='tight')

async def main():
    access_token = os.getenv('ACCESS_TOKEN')
    if not access_token:
        sys.stderr.write('No ACCESS_TOKEN received\n')
        exit(1)

    async with aiohttp.ClientSession() as session:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await session.post('https://api.github.com/graphql', headers=headers, json={'query': QUERY})
        raw_results = await response.json()
        
    languages = {}
    repos = raw_results.get('data', {}).get('viewer', {}).get('repositories', {}).get('nodes', [])
    if len(repos) == 0:
        sys.stderr.write('Repository list empty\n')
        exit(1)
    
    for repo in repos:
        pushed_at = repo.get('pushedAt', '')
        seconds_since_push = (datetime.now(timezone.utc) - datetime.fromisoformat(pushed_at)).total_seconds()
        weeks_since_push = seconds_since_push / 7 / 24 / 60 / 60
        weight = AGE_WEIGHT ** weeks_since_push

        for lang in repo.get('languages', {}).get('edges', []):
            name = lang.get('node', {}).get('name', 'Other')
            color = lang.get('node', {}).get('color', 'black')

            if name in EXCLUDE:
                continue

            size = lang.get('size', 0) ** LENGTH_WEIGHT * weight

            language_info = languages.get(name, (0, color))
            languages[name] = (language_info[0] + size, color)
    
    top_n_languages = sorted(languages.items(), key=lambda x: x[1][0], reverse=True)[:MAX_COUNT]
    total_size = sum(map(lambda l: l[1][0], top_n_languages))
    top_n_languages = list(map(lambda l: (l[0], l[1][0] / total_size, l[1][1]), top_n_languages))

    generate_graph(top_n_languages)

if __name__ == '__main__':
    asyncio.run(main())
