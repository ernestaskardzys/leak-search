import json

import requests
from bs4 import BeautifulSoup

from constants import suspicious_tags, well_known_hacker_forums

bing_key = open("bingKey.txt", "r")
SUBSCRIPTION_KEY = bing_key.read()
SEARCH_ENDPOINT = 'https://api.bing.microsoft.com/v7.0/search'
CALL_API = True
SEARCH_QUERY_KEYWORDS = [
    'leak'
]


#######################
# Search query construction
#######################
def build_queries(company: str):
    search_queries = []
    for keyword in SEARCH_QUERY_KEYWORDS:
        search_queries.append(build_search_query(company, keyword))

    return search_queries


def build_search_query(company: str, keyword: str):
    return company + ' ' + keyword


#######################
# Search using Bing
#######################
def search_bing(company_name, site=None):
    results = dict()
    queries = build_queries(company_name)
    for query in queries:
        final_query = ""
        if site is not None:
            site_query = build_site_query(site)
            final_query = f"{query}+{site_query}"

        results[query] = map_bing_search_results(search_bing_by_query(final_query))
    return results


def search_bing_by_query(search_query):
    if CALL_API:
        json_result = call_bing_api(search_query)
    else:
        # Example: "Citybee leak" to "citybee_leak"
        file_name = search_query.strip().lower().replace(' ', '_')
        json_result = load_local_bing_result(file_name)

    return json_result


def call_bing_api(query):
    params = {
        'q': query,
        'mkt': 'en-US'
    }
    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    try:
        response = requests.get(SEARCH_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as ex:
        raise ex


def load_local_bing_result(file_name: str):
    path = f'bing_results/{file_name}.json'
    with open(path) as file:
        return json.load(file)


def map_bing_search_results(response):
    results = []
    web_pages_json = response['webPages']['value']
    for web_page_json in web_pages_json:
        results.append(map_bing_search_result(web_page_json))
    return results


def map_bing_search_result(web_page_json):
    return web_page_json['url']


def build_site_query(site):
    return f'site:{site}'


#######################
# Scrap page
#######################
def soup_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_word_list(soup):
    for data in soup(['style', 'script']):
        data.decompose()
    only_text = ' '.join(soup.stripped_strings)
    return set(only_text.split())


def calculate_suspicious_tags_score(word_list):
    score = 0
    for word in word_list:
        word_weight = get_suspicious_weight(word)
        score = score + word_weight

    return score


def get_suspicious_weight(word: str):
    for row in suspicious_tags():
        tag = row[0]
        weight = row[1]
        if word.lower() in tag.lower():
            return int(weight)
        else:
            return 0


#######################
# Main
#######################
def scan_through_suspicious_urls(company_name: str):
    search_results_by_url = dict()
    suspicious_urls = well_known_hacker_forums()
    for suspicious_url in suspicious_urls:
        search_results = search_bing(company_name, suspicious_url)
        search_results_by_url[suspicious_url] = search_results
    return search_results_by_url