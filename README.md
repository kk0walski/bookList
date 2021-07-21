# Book List app

### Install packages
```
pip install -r requirements.txt
```

### Development server
```
export FLASK_APP=backend/src/app.py
flask run
```

### Productin server
```
gunicorn backend.src.app:app
```

### Run tests
```
cd backend
python setup.py test
```

### Heroku address

https://flask-book-list.herokuapp.com