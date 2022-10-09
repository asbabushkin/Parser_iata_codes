import requests

from bs4 import BeautifulSoup
from fill_database import fill_airportcodes


def get_airport_codes(url):
    """
    Получить данные о международных аэропортах России со страницы
    https://aviateka.su/all-airports/russia-all-airports/
    и сохранить их в словарь с ключами: 'airport_name', 'country', 'city', 'iata_code', 'icao_code',
    'rus_code', 'type', 'webpage'.
    """
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    keys = ['airport_name', 'country', 'city', 'iata_code', 'rus_code', 'icao_code', 'type', 'webpage']
    data = [[cell.text for cell in row.find_all('td')] for row in soup.find_all('tr') if row.find('td')]
    webpages = [row.find('a', class_='avt-bold-link')['href'] for row in soup.find_all('tr') if row.find('td')]
    for w in webpages:
        response = requests.get(w)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('i', class_='fa fa-globe fa-lg orange-txt')
        links.append(link.find_next().text.strip())

    links[47] = 'https://avia.gazprom.ru/ostafevo'
    data[41][1] = 'Аэропорт Нижний Новгород Стригино'
    data[76][1] = 'Аэропорт Южно-Сахалинск Хомутово'

    for i in range(len(data)):
        del data[i][0]
        data[i].insert(1, 'Россия')
        data[i].append('международный')
        data[i][0] = data[i][0].split('\n')[0]
        data[i].append(webpages[i])

    return [dict(zip(keys, data[i])) for i in range(len(data))]


def get_city_codes(url):
    """
    Получить авиационные коды городов со страницы
    https://aviakassir.info/tools/citycode/country.html?country=RU
    вернуть словарь с ключами city_eng, city_rus, code_eng, code_rus
    """

    keys = ['city_eng', 'code_eng', 'city_rus', 'code_rus']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = [[cell.text for cell in row.find_all('td')] for row in soup.find_all('tr') if row.find('td')][3:]
    for row in range(len(data)):
        data[row][0] = data[row][0][0] + data[row][0][1:].lower()
        for cell in range(len(data[row])):
            data[row][cell] = data[row][cell].replace(r'\xa0', '')
            data[row][cell] = data[row][cell].strip()

    return [dict(zip(keys, data[i])) for i in range(len(data))]


if __name__ == '__main__':
    airport_codes = get_airport_codes('https://aviateka.su/all-airports/russia-all-airports/')
    print(airport_codes)
    city_codes = get_city_codes('https://aviakassir.info/tools/citycode/country.html?country=RU')
    print(city_codes)
    fill_airportcodes(airport_codes)
