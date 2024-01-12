import json
import random
from datetime import date, timedelta

models_dict = {
    "Board": [],
    "Section": [],
    "Tag": [],
    "Card": [],
}


def populateBoard():
    for i in range(1, 4):
        obj = {}
        obj["id"] = i
        obj["title"] = f"Board {i}"
        obj["description"] = f"This is Board {i}"
        if i == 1:
            obj["owner"] = 1
        else:
            obj["owner"] = 2
        models_dict["Board"].append(obj)


def populateSection():
    for i in range(1, 7):
        obj = {}
        obj["id"] = i
        if 1 <= i <= 3:
            obj["title"] = f"Section {i}"
            obj["description"] = f"This is description for Section {i}"
            obj["board"] = 1
        elif 4 <= i <= 5:
            obj["title"] = f"Section {i-3}"
            obj["description"] = f"This is description for Section {i-3}"
            obj["board"] = 2
        else:
            obj["title"] = f"Section {i-5}"
            obj["description"] = f"This is description for Section {i-5}"
            obj["board"] = 3
        models_dict["Section"].append(obj)


def populateTag():
    for i in range(1, 17):
        obj = {}
        obj["id"] = i
        if i <= 10:
            obj["title"] = f"Tag {i}"
            obj["description"] = f"This is Tag {i}"
            obj["board"] = 1
            models_dict["Tag"].append(obj)
        else:
            obj["title"] = f"Tag {i-10}"
            obj["description"] = f"This is Tag {i-10}"
            obj["board"] = 2
            models_dict["Tag"].append(obj)


def populateCard():
    for i in range(1, 11):
        obj = {}
        obj["id"] = i
        if 1 <= i <= 5:
            obj["priority"] = random.randint(1, 3)
            obj["title"] = f"Card {i}"
            obj["description"] = f"This is description for Card {i}"
            obj["tags"] = random.sample(range(1, 11), random.randint(0, 5))
            obj["section"] = 1
            obj["completed"] = bool(random.randint(0, 1))
            # date_format = "%Y-%m-%d"
            # obj["deadline"] = d.strftime(date_format)
        elif 6 <= i <= 8:
            obj["priority"] = random.randint(1, 3)
            obj["title"] = f"Card {i-5}"
            obj["description"] = f"This is description for Card {i-5}"
            obj["tags"] = random.sample(range(1, 11), random.randint(0, 5))
            obj["section"] = 2
            # obj["completed"] = bool(random.randint(0, 1))
            d = date.today() + timedelta(random.randint(1, 3))
            date_format = "%Y-%m-%d"
            obj["deadline"] = d.strftime(date_format)
        else:
            obj["priority"] = random.randint(1, 3)
            obj["title"] = f"Card {i-8}"
            obj["description"] = f"This is description for Card {i-8}"
            obj["tags"] = random.sample(range(1, 11), random.randint(0, 5))
            obj["section"] = 3
            # obj["completed"] = bool(random.randint(0, 1))
            d = date.today() + timedelta(random.randint(4, 5))
            date_format = "%Y-%m-%d"
            obj["deadline"] = d.strftime(date_format)
        models_dict["Card"].append(obj)


def generate_data(file_path):
    random.seed(85)
    populateBoard()
    populateSection()
    populateTag()
    populateCard()
    json_object = json.dumps(models_dict, indent=4)
    json_file = file_path
    with open(json_file, "w+") as outfile:
        outfile.write(json_object)
