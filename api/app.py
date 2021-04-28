from flask import Flask, jsonify, make_response, session, request
from gensim.models.keyedvectors import KeyedVectors
from Article.Collation.comparison import DocSim
from Article.Collation.utils import getData
from Article.output import analyseArticles, compareHeadlines
import pandas
import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "hello"

@app.route('/api/v1.0/search', methods=['GET'])
def collationSearch():
    """Return a sanity check response from the Cloud SQL db in JSON format"""
    # User input keywords and a date
    keywords = request.args.get('keywords')
    date = request.args.get('date')
    extra_days = request.args.get('extra_days')

    # Store the input terms to be used in later requests
    search_vars = {'keywords': keywords, 'date': date, 'extra_days': extra_days}
    session['search_data'] = search_vars

    # Get articles from each source containing keywords at the given date
    queried_sources = getData(keywords, date, extra_days)
    data = {}

    for source in queried_sources:
        source_name = source.get('name').lower().replace(' ', '_')
        source_data = source.get('data').reset_index().to_dict(orient='records')
        data['{}'.format(source_name)] = source_data
    
    response = make_response(jsonify(data))

    # Add Access-Control-Allow-Origin header to allow cross-site request
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    

    # Mozilla provides good references for Access Control at:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Server-Side_Access_Control

    return response

@app.route('/api/v1.0/compare', methods=['GET'])
def collationResults():     

    keywords = session.get('search_data').get('keywords')
    date = session.get('search_data').get('date')
    extra_days = session.get('search_data').get('extra_days')
    root_source_input = int(request.args.get('source'))
    root_article_input = int(request.args.get('article'))

    results = compareHeadlines(keywords, date, extra_days, root_source_input, root_article_input)
    response = make_response(jsonify(results))

    # Add Access-Control-Allow-Origin header to allow cross-site request
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

    return response

@app.route('/api/v1.0/results', methods=['GET'])
def analysisResults():     

    link1 = request.args.get('link1')
    link2 = request.args.get('link2')
    output = analyseArticles(link1, link2)
    response = make_response(jsonify(output))

    # Add Access-Control-Allow-Origin header to allow cross-site request
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

    return response