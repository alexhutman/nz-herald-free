from lxml import html
from argparse import ArgumentParser
import re
import requests


def verify_url(url):
    new_url = url
    if url[:4] == "http" and url[4] != "s":
        new_url = "https" + url[4:]
    regex = "https://(www\.)?nzherald\.co\.nz/[a-zA-Z]+/news/article\.cfm\?c_id=\d&objectid=\d{8}"
    assert re.match(regex, new_url), "Please enter a valid nzherald.co.nz link."


def parse_args():
    parser = ArgumentParser(description="Read the full article of a premium NZ Herald article.")
    parser.add_argument("url", type=str, nargs=1, help="The URL of the premium NZ Herald article you wish to read. "
                                                       "You will probably have to surround it in quotes.")
    args = parser.parse_args()
    url = args.url[0]
    verify_url(url)
    return url


def get_html_from_page(url):
    return requests.get(url).content


def parse_html(html_content):
    tree = html.fromstring(html_content)
    assert "premium-content" in tree.xpath('//div[@id="article-body"]/div/@class'), "This is not a premium page."
    return tree.xpath('//div[@id="article-content"]')[0].text_content()


def main():
    url = parse_args()
    html = get_html_from_page(url)
    print(parse_html(html))


if __name__ == "__main__":
    main()
