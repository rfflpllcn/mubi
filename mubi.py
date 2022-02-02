import json
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlencode, urljoin

_URL_MUBI = "http://mubi.com"
_URL_MUBI_SECURE = "https://mubi.com"
_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19"

_mubi_urls = {
    "login": urljoin(_URL_MUBI_SECURE, "login"),
    "session": urljoin(_URL_MUBI_SECURE, "session"),
    "search": urljoin(_URL_MUBI,
                      "services/films/search.json?term=%s"),
    "programs": urljoin(_URL_MUBI, "cinemas"),
    "single_program": urljoin(_URL_MUBI, "programs"),
    "video": urljoin(_URL_MUBI, "films/%s/secure_url"),
    "prescreen": urljoin(_URL_MUBI, "films/%s/prescreen"),
    "list": urljoin(_URL_MUBI, "watch"),
    "person": urljoin(_URL_MUBI, "cast_members/%s"),
    "logout": urljoin(_URL_MUBI, "logout"),
    "filmstill": "http://s3.amazonaws.com/auteurs_production/images/film/%s/w448/%s.jpg",
    "shortdetails": urljoin(_URL_MUBI,
                            "/services/films/tooltip?id=%s&country_code=US&locale=en_US"),
    "fulldetails": urljoin(_URL_MUBI, "films/%s"),
    "watchlist": urljoin(_URL_MUBI, "/users/%s/watchlist.json"),
    "portrait": "http://s3.amazonaws.com/auteurs_production/images/cast_member/%s/original.jpg"
}

MUBI_URL = "list"
_session = requests.session()
_session.headers = {'User-Agent': _USER_AGENT}

soup = BS(_session.get(_mubi_urls[MUBI_URL]).content, features="html.parser")

films = json.loads(soup.find_all(id="__NEXT_DATA__")[0].contents[0])['props']['initialState']['filmProgramming'][
    'filmProgrammings']

out = []
for _film in films:
    film = _film['film']
    title = film['title']
    year = film['year']
    img = film['stills']['standard']
    popularity = film['popularity']
    average_rating_out_of_ten = film['average_rating_out_of_ten']
    number_of_ratings = film['number_of_ratings']
    directors = '& '.join([_['name'] for _ in film['directors']])

    out.append([directors, title, average_rating_out_of_ten])
    # print("{directors}, {title} ({rating})".format(directors=directors, title=title, rating=average_rating_out_of_ten))

out_sorted = sorted(out, key=lambda x: x[2], reverse=True)

s = "Director(s), title, average rating:\n\n"
for row in out_sorted:
    s+="{directors}, {title} ({rating})\n".format(directors=row[0], title=row[1], rating=row[2])

print(s)
