from bs4 import BeautifulSoup
import requests

from bot_connect import bot


def get_all_news(message):
    url = 'https://kipu-rc.ru'

    requests.get(url)

    pages = requests.get(url)
    soup = BeautifulSoup(pages.text, 'lxml')

    name = soup.find_all('h2', class_='gkTitle')

    for i in range(0, len(name)):
        bot.send_message(message.chat.id, f'{name[i].text}\n'
                                          'Более подробная информация представлена по [ссылке]'
                                          f'(https://kipu-rc.ru{name[i].a.get("href")})',
                         parse_mode='Markdown', disable_web_page_preview=True)

