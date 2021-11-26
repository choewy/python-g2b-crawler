import json


def get_search_keywords():
    with open("json/search_keywords.json", "r", encoding="utf-8") as file:
        load = json.load(file)
        file.close()
        return load


def set_search_keywords(keywords):
    with open("json/search_keywords.json", "w", encoding="utf-8") as file:
        json.dump(keywords, file, ensure_ascii=False, indent="\t")
        file.close()


def get_except_keywords():
    with open("json/except_keywords.json", "r", encoding="utf-8") as file:
        load = json.load(file)
        file.close()
        return load


def set_except_keywords(keywords):
    with open("json/except_keywords.json", "w", encoding="utf-8") as file:
        json.dump(keywords, file, ensure_ascii=False, indent="\t")
        file.close()
