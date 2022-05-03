
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>AJAX demo</h1><ul><li><a href='suggest'>jQuery version</a></li><li><a href='suggest_raw'>raw Javascript version</a></li></ul>"


@app.route('/suggest')
def suggest():
    return render_template('ajaxdemo.html')


@app.route('/suggest_raw')
def suggest_raw():
    return render_template('ajaxdemo_raw.html')


a = ["Anna",
    "Anthony",
    "Brittany",
    "Cinderella",
    "Diana",
    "Eva",
    "Fiona",
    "Gunda",
    "Hege",
    "Inga",
    "Johanna",
    "Kitty",
    "Linda",
    "Nina",
    "Ophelia",
    "Petunia",
    "Amanda",
    "Raquel",
    "Cindy",
    "Doris",
    "Eve",
    "Evita",
    "Sunniva",
    "Tove",
    "Unni",
    "Violet",
    "Liza",
    "Elizabeth",
    "Ellen",
    "Wenche",
    "Vicky",
    "Andrew",
    "Anita"]


@app.route('/suggestnames')
def suggestnames():
    query = request.args.get('q').lower()
    hint = None
    # lookup all hints from array if length of q>0
    l = len(query)
    if l > 0:
        for i in a:
            j = i.lower()
            if query == j[:l]:
                if hint is None:
                    hint = i
                else:
                    hint = f"{hint}, {i}"

    # Set output to "no suggestion" if no hint were found
    # or to the correct values
    if hint is None:
        response = "no suggestion"
    else:
        response = hint

    return response
