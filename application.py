from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, jsonify
import requests
import numpy as np
import urllib
from urllib.parse import urlencode
import json
import validators

url = 'https://neutrinoapi.net/bad-word-filter'
params = {
    'user-id': 'naren81',
    'api-key': 'M4IbR5AwsH29MhiMGiJmDDyq0d01shupkPRRP0coQEG69vb9',
    'content': 'https://en.wikipedia.org/wiki/Profanity'
}


def _get_profane_prob(prob):
    return prob[1]


application = Flask(__name__)  # initializing a flask app
app = application


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


# route to show the predictions in a web UI
@app.route('/predict', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        # try:
        te = []
        #  reading the inputs given by the user
        gre_score = (request.form['gre_score'])
        te.append(gre_score)
        is_research = request.form['research']
        if(is_research == 'TEXT'):

            encoded_search = urllib.parse.quote(gre_score)

            text_url = "https://neutrinoapi-bad-word-filter.p.rapidapi.com/bad-word-filter"

            payload = f"content={encoded_search} & censor-character=,*"
            headers = {

                'content-type': "application/x-www-form-urlencoded",
                'x-rapidapi-host': "neutrinoapi-bad-word-filter.p.rapidapi.com",
                'x-rapidapi-key': "171078cc74mshcece1182e710d91p1508f8jsn185172894b07"
            }

            response = requests.request(
                "POST", text_url, data=payload, headers=headers)

            print(response.text)
            return render_template('results.html', prediction=response.text)

        if(is_research == 'URL'):
            if validators.url(gre_score) == True:
                gre_score = (request.form['gre_score'])
                params['content'] = gre_score
                encoded_params = urlencode(params).encode('utf8')
                response = urllib.request.urlopen(url, data=encoded_params)
                result = json.loads(response.read())
                if result['is-bad'] == True:
                    t = result['bad-words-list']
                    st = ",".join(t)
                    prediction = "Url is abusive and it contains following abusive words " + st
                    return render_template('results.html', prediction=prediction)
                else:
                    prediction = 'Url is not abusive'
                    return render_template('results.html', prediction=prediction)
            else:
                prediction = "Not Valid Url"
                return render_template('results.html', prediction=prediction)

    else:
        return render_template('index.html')


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)  # running the app
