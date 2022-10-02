import re
import requests as req
import os
from requesting_urls import get_html

def find_urls(html_str: str, base_url=None):
    """
    Finds urls in a string of html code. If a base url is given, all relative paths will be reformated

    Arguments
    ---------
    html_str (str): a string of html code
    base_url (str): a base url to a relative path

    Returns
    -------
    urls (list): a list of all urls
    """
    regex = r"href=[\'\"]?([^\'\" >]+)"
    matches = re.findall(regex, html_str)
    urls = []
    for str in matches:
        #switch the names!!!
        remove_line = r"^#.*"
        modify_line = r".*#.*"
        add_base = r"^\/.*"
        not_allowed = re.findall(remove_line, str)
        has_to_change = re.findall(modify_line,str)
        relative_path = re.findall(add_base, str)

        if len(not_allowed) != 0:  #removing fragment
            continue

        if len(has_to_change)!=0:  #removing fragment
            new_url = str.split("#")
            new_url = new_url[0]
            if len(relative_path) != 0:
                if base_url == None:
                    urls.append(new_url)
                    continue
                new_url = base_url + new_url
            urls.append(new_url)
            continue

        if len(relative_path) != 0:
            if base_url == None:
                urls.append(str)
                continue
            new_url = base_url + str
            urls.append(new_url)
            continue
        urls.append(str)
    return urls


def find_article(html_str: str, output = None):
    """
    Finds all the wikipedia urls in a string of html code and either writes the html and urls to a file,
    if an output file name is given, or returns a list of the urls

    Arguments
    ---------
    html_str (str): string of html code
    output (str): file name of an output file, default set to None

    Returns
    -------
    If output == None
        wiki_urls (list): a list of all wikipedia urls
    """
    urls = find_urls(html_str, "https://en.wikipedia.org")
    regex = r".*wikipedia\.org.*"
    wiki_urls = []
    output_urls = output[:-4] + "_urls.txt"
    for str in urls:
        if ":" in str[6:]:
            continue
        matches = re.findall(regex, str)
        wiki_urls = wiki_urls + matches

    if output != None:
        dir = os.getcwd()
        path = dir + "\\filter_urls"
        output_urls = output[:-4] + "_urls.txt"
        output_html = output[:-4] + "_html.txt"
        save_urls_in = os.path.join(path, output_urls)
        save_html_in = os.path.join(path, output_html)

        file = open(save_urls_in, "w", encoding='utf-8')
        for url in wiki_urls:
            L = [f"{url}\n"]
            file.writelines(L)
        file.close

        file = open(save_html_in, "w", encoding='utf-8')
        L = [html_str]
        file.writelines(L)
        file.close
    else:
        return wiki_urls


if __name__ == '__main__':
    str_1 = get_html("https://en.wikipedia.org/wiki/Nobel_Prize")
    find_article(str_1, "Nobel_Prize_wiki.txt")

    str_2 = get_html("https://en.wikipedia.org/wiki/Bundesliga")
    find_article(str_2, "Bundesliga_wiki.txt")

    str_3 = get_html("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup")
    find_article(str_3, "FIS_Alpine_Ski_wiki.txt")
