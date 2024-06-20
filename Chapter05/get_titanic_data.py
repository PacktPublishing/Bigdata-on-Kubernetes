import os
import requests

urls_dict = {
    "titanic.csv": "https://raw.githubusercontent.com/neylsoncrepalde/titanic_data_with_semicolon/main/titanic.csv",
}


def get_titanic_data(urls):
    for title, url in urls.items():
        response = requests.get(url, stream=True)
        with open(f"data/titanic/{title}", mode="wb") as file:
            file.write(response.content)
    return True


os.makedirs('data/titanic', exist_ok=True)
get_titanic_data(urls_dict)
