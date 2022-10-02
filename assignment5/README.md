## README.md Assignment5

## Task 5.1

### Prerequisites

No prerequisites

### Functionality
The file `requesting_urls.py` has a function `get_html` which receives a url and the optional arguments of parameters
and output file name. If an output file name is given, the function will write the html code of the given url to a txt-file.
If an output file name is not given, the function will return a string of the html code

### Missing Functionality

There are no missing functionalities

### Usage

To make a file with the html code, one need to give a functioning url, a string with the desired file name and a dictionary with parameters if necessary.
To only make the function return a string, one can omit the output file name.
```bash
get_html(url (str), params (dictionary)(optional), output (str)(optional))

```

To run in the terminal
```bash
python requesting_urls.py
```

## Task 5.2
### Prerequisites

No prerequisites

### Functionality
The file `filter_urls.py` has two functions, `find_urls` and `find_article`.
`find_urls` finds all the urls in a given string of html code.
`find_article` find all the wikipedia articles on a wikipedia page, and writes their urls to a file

### Missing Functionality

There are no missing functionalities

### Usage

To find all the urls in some html code, one has to give `find_urls` said html code as a string, and if there is a known base url that, one can supply that as well.
To find all the urls of wikipedia articles within another wikipedia article, one has to give a the html code of the article as a string, and to write all the urls to a file, one also has to supply an output file name. The urls and the original html code is saved in separate files in the folder filter_urls

```bash
find_urls(html_str, "https://base")
find_article(html_str, "filename.txt")

```

To run in the terminal
```bash
python filter_urls.py
```

## Task 5.4

### Prerequisites

One need to have installed BeautifulSoup

### Functionality

The test file, `time_planner.py`, has to functions, `extract_events` and `create_betting_slip`.
`extract_events` finds all the dates, venues and discipline of each event in a skiing tournament.
`create_betting_slip` creates a .md file containing a betting slip.

### Missing Functionality

No missing functionalities

### Usage

To get a list of all events from one only needs to call the function `extract_events`.
To make a betting slip one need to give a list of events, with tuples of date, venue and discipline, and an output file name. One can use the output from `extract_events` as an argument.
```bash
events = extract_events()
create_betting_slip(events, "betting_slip")
```
To run in the terminal
```bash
python time_planner.py
```

## Task 5.5

### Prerequisites

One need to have installed BeautifulSoup

### Functionality

The class Stats, finds team names and urls, finds all the players in each team, finds the three best players in each team and plots the three best players from each team over points per game, blocks per game and rebounds per game and saves the images in the folder NBA_player_statistics

### Missing Functionality

There is no module/function which allow the user to scale an image.

### Usage

To plot the best players over ppg, bpg ang rpg one needs to make an instance of the class and call the class method `plot`
```bash
stat = Stats()
stat.plot()
```
To run in the terminal
```bash
python fetch_player_statistics.py
```
