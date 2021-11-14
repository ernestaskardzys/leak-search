# Installation

In order to install the project, you need install its dependencies:

```bash
$ pip3 install -r requirements.txt
```

Add your Bing API key to `bingKey.txt` file.

# Configuration

To configure the project, open `bing.py` file:

- `CALL_API` constant controls if we should call real, Bing API or to use already saved responses in `bing_results` directory. Please note, that free Bing Search account limits number of requests you can make.  
- `SEARCH_QUERY_KEYWORDS` controls what Bing search keywords to use

To configure list of well known hacker forums or list of suspicious tags to use, edit `constants.py` file.

# Running the project

To run the project, please execute:

```bash
$ python3 main.py
```

Or use Docker:

```bash
$ docker build -t leak-search .
$ docker run -it -p 4444:4444 leak-search   
```

And to test, simply:

```bash
$ curl "localhost:4444/search?entity=robinhood"
$ curl "http://localhost:4444/scan/in/suspicious-urls"
```

If no entity provided, `citybee` will be used

# Idea

Problem: 
- How can legal entity get advance warning about its data leak?
- How can natural person access if company's data has been already leaked?

Currently, we search by search tags, but later search could be improved using machine learning and by searching on dark web.

Algorithm:
- Define a legal entity to search information for - citybee, robinhood, twitch etc.
- Use hardcoded list of keywords (e.g. data leak + company)
- Search by them across the world
- Download each web page, parse search for specific actions in it - download, zip, buy
- In the top trends by country, search for the specific keywords (#1) if some search is booming, it might be a leak

## Level 1. Notification

- Search company name in search engine, look for its mentioning together with "data leak", "leak keywords".
- Inform customer or company

## Level 2. Hacker forum search

- Search for leaks on a well known hacker forums
- Calculate leak probability score

## Level 3. Trends

- Increase of search trends related to data leak in a specific country. 