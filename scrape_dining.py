import requests
import re
import datetime
import cPickle as pickle


now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
menu_today = {}

try:
    archive = pickle.load(open("data/archive.p", "rb"))
except:
    archive = {}

list_colleges = {
    'Berkeley': 1,
    'Branford': 2,
    'Calhoun': 3,
    'Commons': 11,
    'Davenport': 4,
    'Hall of Graduate Studies': 12,
    'Jonathan Edwards': 6,
    'Marigolds': 15,
    'Morse': 5,
    'Pierson': 7,
    'Saybrook': 23,
    'Silliman': 8,
    'Stiles': 24,
    'Timothy Dwight': 9,
    'Trumbull': 10
}


def fix_special_chars(item):
    #Removes the special icon
    item = re.sub(' <img.*', '', item)
    #Fixes the accent on the e
    item = re.sub('\xc3\xa9', 'e', item)
    #Fixes the Ampersand
    item = re.sub('&amp;', 'and', item)
    return item


def get_items(meal):
    food_marker = '<div class="recipe">\r\n\t\t\t\t\t\r\n               \t\t<h2>.*</h2>'
    #Cuts off the html tags
    list_items = [item[50:-6] for item in re.findall(food_marker, meal)]
    #Fixes specific problems
    list_items = map(fix_special_chars, list_items)
    return list_items


#Subset webpage to menu
def get_menu(webpage):
    menu_start = re.search('<!-- menu start -->', webpage).end()
    menu_end = re.search('<!-- menu end -->', webpage).start()
    return webpage[menu_start:menu_end]


#Get list of meals
def get_meals(menu):
    all_meals = []
    for meal_start, meal_end in zip(re.finditer('<!-- start meal -->', menu), re.finditer('<!-- end course -->', menu)):
        all_meals.append(menu[meal_start.end():meal_end.start()])
    return all_meals


def get_meal_names(all_meals):
    college = {}
    for meal in all_meals:
        find_name = re.search('<h1>.*</h1>', meal)
        meal_name = meal[find_name.start()+4:find_name.end()-5]
        college[meal_name] = meal
    return college


def get_dishes(college):
    for meal in college:
        college[meal] = get_items(college[meal])
    return college


all_colleges = {}
for name_college in list_colleges.keys():
    url = 'http://www.yaledining.org/menu.cfm?mDH='+str(list_colleges[name_college])
    r = requests.get(url)
    #Get menu
    menu = get_menu(r.content)
    #Find how many meals there were
    all_meals = get_meals(menu)
    #Getting names of meals
    college = get_meal_names(all_meals)
    #Get names of dishes
    college = get_dishes(college)
    #Add these to dict.
    all_colleges[name_college] = college

menu_today[date] = all_colleges
archive[date] = all_colleges

pickle.dump(menu_today, open("data/menu_today.p", "wb"))
pickle.dump(archive, open("data/archive.p", "wb"))
