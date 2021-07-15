from bs4 import BeautifulSoup
import requests
from datetime import datetime

# example url for datetime filtering
# https://www.jao.eu/api/news/all?page=1&roles_target_id_group=tso&created%5Bmin%5D=04/01/2021%2000:00:00&created%5Bmax%5D=07/31/2021%2023:59:59

BASEURL = "https://www.jao.eu/api/news/all?roles_target_id_group={group}"
# in below string the dates need to be format %m/%d/%Y
DATE_FILTER = "&created%5Bmin%5D={d_from}%2000:00:00&created%5Bmax%5D={d_to}%2023:59:59"
PAGE_FILTER = "&page={page}"


def _message_parser(info):
    def _document_parser(docinfo):
        soup_document = BeautifulSoup(docinfo, 'lxml')
        return {
            "url": "https://jao.eu" + soup_document.find('a').attrs['href'],
            'name': soup_document.find('a').get_text().strip()
        }

    soup_title = BeautifulSoup(info['nothing'], 'lxml')
    soup_body = BeautifulSoup(info['body'], 'lxml')

    return {
        'title': soup_title.find('h2').text,
        'author': soup_title.find('span', class_='tso').text.replace("by ", ""),
        'published': datetime.strptime(soup_title.find('time').attrs["datetime"], "%d/%m/%Y | %H:%M"),
        'body': soup_body.get_text(),
        'documents': [_document_parser(doc_info) for doc_info in info['documents']]
    }


def _fetch_messages(url):
    r = requests.get(url, headers={
        'user-agent': 'JAO-messageboard-parser'
    })
    if r.status_code != 200:
        raise RuntimeError(f"Url {url} could not be retrieved with error code {r.status_code}")

    return [_message_parser(info) for info in r.json()]


def JAO_get_messages_from_dates(d_from, d_to, group="tso"):
    if group not in ["tso", "jao", "all"]:
        raise RuntimeError("Please choose group from: tso, jao, all")

    return _fetch_messages(BASEURL.format(group=group) + DATE_FILTER.format(d_from=d_from.strftime("%m/%d/%Y"), d_to=d_to.strftime("%m/%d/%Y")))


def JAO_get_messages_from_pages(p_from, p_to, group="tso"):
    if group not in ["tso", "jao", "all"]:
        raise RuntimeError("Please choose group from: tso, jao, all")
    messages = []
    for i in range(p_from, p_to+1):
        messages += _fetch_messages(BASEURL.format(group=group) + PAGE_FILTER.format(page=i))
    return messages