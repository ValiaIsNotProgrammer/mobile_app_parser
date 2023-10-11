import csv
import os

from mitmproxy import http
import json


class MyAddon:
    """
    Необходимые данные:

    id товара из сайта/приложения : id

    наименование : title

    ссылка на товар : webpage

    регулярная цена : price[actual]

    промо цена : price[subscribe]

    бренд. : pass
    """
    _keys = ["id", "title", "webpage", "actual", "subscribe"]
    _json = {}

    def request(self, flow: http.HTTPFlow) -> None:
        if "https://4lapy.ru/" in flow.request.url:
            pass

    def response(self, flow: http.HTTPFlow) -> None:
        if "https://4lapy.ru/" in flow.request.url:
            raw_data = flow.response.content.decode("utf-8", errors='ignore')
            try:
                data = json.loads(raw_data)["data"]
            except json.decoder.JSONDecodeError:
                return
            self.__save(self.__parse_json(data))

    def done(self, *args, **kwargs):
        print("Загрузка завершена")

    def __parse_json(self, data: dict):
        new_data = []
        try:
            for goods in data["goods"]:
                new_data.append(self.__remove_other_keys(goods))
        except KeyError:
            return {}
        print("Добавлены новые товары")
        return new_data

    def __remove_other_keys(self, old_data: dict):
        new_data = {}
        for key in old_data.keys():
            if key in self._keys:
                new_data[key] = old_data[key]
            if type(old_data[key]) == dict:
                new_data |= self.__remove_other_keys(old_data[key])
        return new_data

    def __save(self, data: list):
        print(f"Загруженно {len(data)} товаров")
        file_name = "data.csv"
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = self._keys
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if os.stat(file_path).st_size == 0:
                writer.writeheader()

            for row in data:
                writer.writerow(row)


addons = [
    MyAddon()
]
