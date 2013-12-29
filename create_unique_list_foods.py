import pickle

z = pickle.load(open('data/menu_today.p', 'rb'))

try:
    list_of_all_foods = pickle.load(open('data.list_of_all_foods.p', 'rb'))
except:
    list_of_all_foods = []


for day in z:
    for college in z[day]:
        for meal in z[day][college]:
            for item in z[day][college][meal]:
                if item not in list_of_all_foods:
                    list_of_all_foods.append(item)

list_of_all_foods = sorted(list_of_all_foods)

pickle.dump(list_of_all_foods, open("data/list_of_all_foods.p", "wb"))
