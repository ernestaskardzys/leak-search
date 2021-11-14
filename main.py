import flask
from flask import request, jsonify

# Local function imports
from bing import search_bing, soup_page, get_word_list, calculate_suspicious_tags_score, scan_through_suspicious_urls

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/search', methods=['GET'])
def search_web():
    entity = request.args.get('entity', default='citybee', type=str)
    app.logger.info('Searching for legal entity: ' + entity)
    search_results = search_bing(entity)
    response = { "key": entity, "values" : [] }

    for main_entry in search_results:
        for url in search_results[main_entry]:
            html = soup_page(url)
            word_list = get_word_list(html)
            suspicious_tag_score = calculate_suspicious_tags_score(word_list)
            if suspicious_tag_score > 0:
                print("Check this URL: " + url + " with score " + suspicious_tag_score.__str__())
                row = { "url": url, "score": suspicious_tag_score.__str__() }
                response.get("values").append(row)

    app.logger.info('Done searching for legal entity: ' + entity)
    return response


@app.route("/scan/in/suspicious-urls", methods=['GET'])
def scan_in_suspicious_urls():
    entity = request.args.get('entity', default='citybee', type=str)
    results = scan_through_suspicious_urls(entity)
    return __map_suspicious_urls_response(results)


def __map_suspicious_urls_response(results):
    response = []
    for result in results:
        response_row = {
            "website": "",
            "search_result": []
        }

        print(results[result])

        website = result
        response_row["website"] = website
        for query in results[website]:
            response_row.get("search_result").append({
                "query": query,
                "urls": results[website][query]
            })
        response.append(response_row)
    return jsonify(response)


if __name__ == '__main__':
    from waitress import serve

    app.logger.info("Staring system on port 4444")
    serve(app, host='0.0.0.0', port=4444)