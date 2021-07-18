from flask import Flask,render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', books=get_books())

@app.route('/import', methods=['GET', 'POST'])
def import_books():
    return render_template('import.html')

def get_books():
    books = [
        {
        'title': "Don Quixote",
        'author': "Miguel de Cervantes",
        'date': "10-11-2012",
        'isbn': "9788320717501",
        'pages': 100,
        'language': 'polish',
        'frontPage': "https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/don_quixote.jpg"
        },
        {
        'title': "As I Lay Dying",
        'author': "William Faulkner",
        'date': "10-11-2012",
        'isbn': "9788320717501",
        'pages': 100,
        'language': 'polish',
        'frontPage': "https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/as_I_lay.jpg"
        },
        {
        'title': "Things Fall Apart",
        'author': "Miguel de Cervantes",
        'date': "10-11-2012",
        'isbn': "9788320717501",
        'pages': 100,
        'language': 'polish',
        'frontPage': "https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/things_fall_apart.jpg"
        }
    ]

    return books

if __name__ == '__main__':
    app.run(debug=True)