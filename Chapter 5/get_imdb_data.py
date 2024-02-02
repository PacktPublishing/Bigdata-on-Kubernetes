import os
import requests

urls_dict = {
    "names.tsv.gz": "https://datasets.imdbws.com/name.basics.tsv.gz",
    "basics.tsv.gz": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "crew.tsv.gz": "https://datasets.imdbws.com/title.crew.tsv.gz",
    "principals.tsv.gz": "https://datasets.imdbws.com/title.principals.tsv.gz",
    "ratings.tsv.gz": "https://datasets.imdbws.com/title.ratings.tsv.gz"
}


def get_imdb_data(urls):
    for title, url in urls.items():
        response = requests.get(url, stream=True)
        with open(f"data/imdb/{title}", mode="wb") as file:
            file.write(response.content)
    return True


os.makedirs('data/imdb', exist_ok=True)
get_imdb_data(urls_dict)
