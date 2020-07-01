from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from celery.task import periodic_task
from celery.schedules import crontab
from datetime import timedelta

from core.serializers import CategorySerializer


class StaticField:
    empty_site = 0
    last_filled_page = 1


def parsing(index=1):
    from core.models import Recipe
    from core.models import Category
    url = 'http://thermomix-recipe.ru/recepty/' + str(index)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    name = soup.find('h1', itemprop='name')
    if name is None:
        StaticField.empty_site += 1
        return
    name = name.text
    im = soup.find('img', alt=name)
    recipes = soup.find('div', itemprop='description').text
    date = soup.find('span', class_="creation_date").text
    date = date.split(" ")
    datetime = ''
    for i in date:
        if i in "создан:":
            continue
        datetime += i
    accesoire = soup.find_all("span", class_="accessoire-text")
    acc = ''
    for i in accesoire:
        acc += i.text
    hint = soup.find('div', id='tip-final').text
    category_name = soup.find('span', class_="global-active row").text
    try:
        category = Category.objects.get(name=category_name)
    except:
        category = Category.objects.create(name=category_name)
    model = soup.find('div', class_="thermomix-model-name").text
    ingredients = soup.find_all("div", id="ingredient-blocks-wrapper-final")
    ing = ''
    difficulty = soup.find('span', class_="difficulty-word").text
    for i in ingredients:
        ing += i.text
    rating = soup.find('input', class_="rating").get('value')
    if im is not None:
        image = 'http://thermomix-recipe.ru/' + im.get('src')
        Recipe.objects.create(name=name, image=image, stars=rating, ingredients=ing, time=datetime,
                              recipes=recipes, accessorizes=acc,
                              hint=hint, category=category, model=model, difficulty=difficulty)
    else:
        Recipe.objects.create(name=name, stars=rating, ingredients=ing, time=datetime,
                              recipes=recipes, accessorizes=acc,
                              hint=hint, category=category, model=model, difficulty=difficulty)
    StaticField.last_filled_page = index


def parsing2(index=1):
    from core.models import Recipe
    from core.models import Category
    url = 'https://my.thermomixrecipes.com/thmrecipes/' + str(index)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    name = soup.find('span', itemprop='name')
    if name is None:
        StaticField.empty_site += 1
        return
    name = name.text
    img = soup.find('div', class_="recipebanner").get('style')
    ok = False
    image = ''
    for i in img:
        if i == ')':
            ok = False
        if ok:
            image += i
        if i == '(':
            ok = True
    cooking = soup.find_all("div", class_="content")
    recipes = ''
    for i in cooking:
        recipes += i.text.replace('\n', ' ')
    category_name = soup.find('div', class_="categories").text
    try:
        category = Category.objects.get(name=category_name)
    except:
        category = Category.objects.create(name=category_name)
    difficulty = soup.find('li', class_="difficulty-icon").text
    device = soup.find('li', class_="device").text
    ingredients = soup.find_all("ol")
    ing = ''
    for i in ingredients:
        ing += i.text
    ing = ing[:len(ing) // 2]
    rating = soup.find('img', class_="post-ratings-image").get('title')
    rating_n = ''
    digit = False
    for i in rating:
        if i == " ":
            digit = False
        if digit:
            rating_n += i
        if i == ":":
            digit = True
    try:
        rating = float(rating_n)
    except:
        rating = 1
    if image is not None:
        Recipe.objects.create(name_en=name, image=image, stars=rating, ingredients_en=ing,
                              recipes_en=recipes, accessorizes="",
                              hint="", category_en=category, model=device, difficulty_en=difficulty)
    else:
        Recipe.objects.create(name_en=name, stars=rating, ingredients_en=ing,
                              recipes_en=recipes, accessorizes="",
                              hint="", category_en=category, model=device, difficulty_en=difficulty)
    StaticField.last_filled_page = index


@periodic_task(run_every=crontab(minute=0, hour=0))
def post_data():
    file = open("last_page.txt", 'r+')
    StaticField.last_filled_page = int(file.read())
    i = 1
    while True:
        if StaticField.empty_site >= 10:
            break
        parsing(i)
        i += 1
    print(StaticField.last_filled_page)
    file.seek(0)
    file.truncate()
    file.write(str(StaticField.last_filled_page))
    file.close()

    file2 = open("last_page2.txt", 'r+')
    StaticField.last_filled_page = int(file2.read())
    i = 1
    while True:
        if StaticField.empty_site >= 10:
            break
        parsing2(i)
        i += 1
    print(StaticField.last_filled_page)
    file2.seek(0)
    file2.truncate()
    file2.write(str(StaticField.last_filled_page))
    file2.close()
