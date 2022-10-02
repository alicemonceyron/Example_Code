import re
import requests as req
from bs4 import BeautifulSoup
import os
from requesting_urls import get_html

def extract_events(url = "https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup"):
    """
    Finds the date, venue and discipline of each event

    Arguments
    ---------
    url (str): default is url for Alpine Ski World Cup

    Returns
    -------
    events (list): list containing a tuple of the date, venue and discipline for each event
    """
    disciplines = {"DH": " Downhill ",
                    "SL": " Slalom ",
                    "GS": " Giant Slalom ",
                    "SG": " Super Giant Slalom ",
                    "AC": " Alpine Combined ",
                    "PG": " Parallel Giant Slalom "}

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    calendar_header = soup.find(id = "Calendar_2")                #finds table for women
    calendar_table = calendar_header.find_all_next("table")[0]
    rows = calendar_table.find_all("tr")

    found_date = None
    found_venue = None
    found_discipline = None
    events = []

    colomns = rows[0].find_all("th")                #retrives the headers for the table, to find the lenght of one row
    full_row_length = len(colomns)                  #rows which does not share any cells with the one above
    short_row_length_type_1 = full_row_length - 1   #rows which share one cell with the one above
    short_row_length_type_2 = full_row_length - 2   #rows which share two cells with the one above

    for row in rows:
        #regex = r">([0-9a-zA-Z ]*)"
        cells = row.find_all("td")
        if len(cells) == 0:
            continue
        for idx, cell in enumerate(cells):
            cell_text = cell.text.strip()
            if len(cell_text)==0:
                cell_text = None
            cells[idx] = cell_text

        if len(cells) not in {full_row_length, short_row_length_type_1, short_row_length_type_2}:
            continue

        found_date = cells[2]

        if len(cells) == full_row_length:
            found_venue = cells[3]
            discipline_index = 5
        elif len(cells) == short_row_length_type_1:
            discipline_index = 5-1
        else:
            discipline_index = 5-2


        discipline = cells[discipline_index]
        disciplines_regex = r"[a-zA-Z]*"
        disciplines_match = re.search(disciplines_regex, discipline)

        if disciplines_match:
            found_discipline = disciplines[disciplines_match[0]]
        else:
            found_discipline = None

        if found_venue and found_date and found_discipline:
            events.append((found_date, found_venue, found_discipline))
    return events

def create_betting_slip(events, save_as):
    os.makedirs ("datetime_filter", exist_ok = True )

    with open ( f"./datetime_filter/{save_as}.md", "w") as out_file :
        out_file.write (f"# BETTING SLIP ({ save_as })\n\n Name :\n\n")
        out_file.write (" Date | Venue | Discipline | Who wins ?\n")
        out_file.write (" --- | --- | --- | --- \n")
        for e in events :
            date, venue, type = e
            out_file.write (f"{date} | {venue} | {type} | \n")


if __name__ == '__main__':
    events = extract_events()
    create_betting_slip(events, "betting_slip_empty")
