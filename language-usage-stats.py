#!/usr/bin/env python3

import os
import asyncio
import sys
import aiohttp
from datetime import datetime, timezone

AGE_WEIGHT = 0.8
LENGTH_WEIGHT = 0.5
EXCLUDE = ['Shell', 'Batchfile', 'Makefile', 'CMake', 'Meson', 'Roff', 'HTML', 'CSS', 'Vim Script']
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

    for name, info in top_n_languages:
        print(f'{name},{info[0] / total_size:.3f},{info[1]}')

if __name__ == '__main__':
    asyncio.run(main())
