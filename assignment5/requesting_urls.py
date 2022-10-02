import requests as req
import os
import time

def get_html(url, params = None, output = False):
    """
    Reads the html code from a given url and gives out the code as a string

    Arguments
    ---------
    url (str): any url
    params (dictionary): default set to None
    output (str): file name of an output file, default set to None

    Returns
    -------
    r.text (str): a string of html code
    """
    r = req.get(url, params = params)
    msg = f"{r.status_code}, url: {url}"
    assert r.status_code==200, msg
    if output is not False:
        dir = os.getcwd()
        path = dir + "\\requesting_urls"
        save_in = os.path.join(path, output)
        file = open(save_in, "w", encoding='utf-8')
        L = [f"{url}\n {r.text}"]
        file.writelines(L)
        file.close
        print("file has been saved with website content")
    else:
        return r.text




if __name__ == '__main__':
    get_html("https://en.wikipedia.org/wiki/Studio_Ghibli", output="Studio_Ghibli_wiki.txt")
    get_html("https://en.wikipedia.org/wiki/Star_Wars", output = "Star_Wars_wiki.txt")
    params = {"title":"Main_Page", "action":"info"}
    get_html("https://en.wikipedia.org/wiki/Main_Page", params, output = "Main_Page_wiki.txt")
