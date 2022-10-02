import pytest
from filter_urls import find_urls

def test_find_urls () :
    html = """
    <a href="#cite_note-verge-purchase-45" ></a>
    <a id =" some -id" href="/wiki/Studio_Ponoc#fragment"> </a>
    <a href="https://www.aftenposten.no/"> </a>
    <a href="https://en.wikipedia.org/wiki/Spirited_Away"> </a>
    """
    urls = find_urls(html, base_url ="https://en.wikipedia.org")

    assert urls == [
    "https://en.wikipedia.org/wiki/Studio_Ponoc",
    "https://www.aftenposten.no/",
    "https://en.wikipedia.org/wiki/Spirited_Away"]
