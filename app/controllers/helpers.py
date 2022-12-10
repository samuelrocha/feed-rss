import requests
import io
import base64
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from os import path
from flask import render_template
from sqlalchemy.exc import NoResultFound
from app import db
from requests.exceptions import MissingSchema
from flask_login import current_user
from sqlalchemy import select
from app.models.tables import Feed, Category
from datetime import datetime


def feed_rss(smtm):

    smtm = select(Feed).where(Feed.user_id ==
                              current_user.id)
    feeds = get_feed(smtm)

    items = []
    for feed in feeds:
        category = get_category(feed[0].category_id)
        xml = get_xml(feed[0].url)
        for item in xml.find_all('item'):
            pub_date = datetime.strptime(item.pubDate.string, "%a, %d %b %Y %H:%M:%S %z")
            items.append({
                'title': item.title.string,
                'link': item.link.string,
                'portalname': feed[0].portalname,
                'category': category,
                'post_date': pub_date
            })

    items = sorted(items, key=lambda item: item['post_date'], reverse=True)

    return items

def get_category(id):
    
    smtm = select(Category.name).where(Category.id == id)
    row = db.session.execute(smtm).one()
    name = row[0]
    return name

def get_xml(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        return soup
    except MissingSchema:
        return False


def get_feed(smtm):
    try:
        row = db.session.execute(smtm).all()
        return row
    except NoResultFound:
        return False


def apology(msg, status=400):
    with Image.open('app/static/img/jotaro.jpg').convert('RGBA') as base:

        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)

        error = f'error {str(status)}'
        font1 = ImageFont.truetype(
            "app/static/fonts/RubikGlitch-Regular.ttf", 72)
        size1 = int(font1.getlength(error))

        px = 48
        while True:
            font2 = ImageFont.truetype(
                "app/static/fonts/RubikGlitch-Regular.ttf", px)
            size2 = int(font2.getlength(msg))
            if size2 < 500:
                break
            px -= 10

        x1 = 250 - size1//2
        x2 = 250 - size2//2

        d.text((x1, 515), error, font=font1, fill=(255, 0, 0, 255))
        d.text((x2, 50), msg, font=font2, fill=(0, 0, 0, 255))

        # convert the image to base64
        out = Image.alpha_composite(base, txt)
        img_byte_arr = io.BytesIO()
        out.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base = base64.b64encode(img_byte_arr)
        img = base.decode()

        return render_template('error.html', img=img)
