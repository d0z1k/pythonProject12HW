import json

from classes.exeptions import DataSourceBrokenException


class DataManager:

    def __init__(self, path):
        self.path = path

    def load_data(self):
        """
        Загружает данные из файла
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except(FileNotFoundError, json.JSONDecodeError):
            raise DataSourceBrokenException("Файл с данными повреждён")
        return data

    def save_data(self, data):
        """
        сохраняет загруженные данные
        """

        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_all(self):
        """
        загружает полный список данных
        """

        data = self.load_data()
        return data

    def search(self, substring):
        """
        поиск постов по сабстрингу
        """

        posts = self.load_data()
        matching_posts = [post for post in posts if substring in post["content"].lower()]

        return matching_posts

    def add(self, post):
        """
        добавляет пост в хранилище
        """

        if type(post) != dict:
            raise TypeError("должен быть словарь")

        posts = self.load_data()
        posts.append(post)
        self.save_data(posts)
