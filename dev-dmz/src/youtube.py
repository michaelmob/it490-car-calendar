#!/usr/bin/env python3
import os, json, requests, html


def search(query):
    """
    Search YouTube by query.
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = f'?key={api_key}&part=snippet&q={html.escape(query)}'
    response = requests.get(url + params)

    try:
        result = json.loads(response.content)
        return result.get('items')
    except Exception as e:
        raise e
