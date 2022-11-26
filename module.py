import requests
import sqlite3
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from os import path

def connection():
    if not path.isfile('feed-rss.db'):
        connection = sqlite3.connect('feed-rss.db')
        cursor = connection.cursor()
        with open('table.sql') as table:
            scripts = table.read()

        for script in scripts.split(';'):
            cursor.execute(script)
    else:
        connection = sqlite3.connect('feed-rss.db')
        cursor = connection.cursor()
    return cursor

def feed_rss(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'xml')

    feed = []
    for item in soup.find_all('item'):
        feed.append({
            'title': item.title.string,
            'link': item.link.string
        })

    return feed


def create_error_image():
    with Image.open('static/jotaro.jpg').convert('RGBA') as base:

        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)

        font = ImageFont.truetype("static/RubikGlitch-Regular.ttf", 72)
        error = "Error 400"
        size = int(font.getlength(error))
        x = 250 - size//2

        d.text((x, 515), error, font=font, fill=(255, 0, 0, 255))

        out = Image.alpha_composite(base, txt)
        out.save('static/error.png', 'PNG')

        return out
