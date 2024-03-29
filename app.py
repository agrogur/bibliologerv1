import requests
import os
import pyrebase
from datetime import datetime
from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)

config = {
  'apiKey': "AIzaSyDIWINaH8Q7cBshxqzDcHphJKLWvRRELQc",
  'authDomain': "blissful-cell-393422.firebaseapp.com",
  'projectId': "blissful-cell-393422",
  'storageBucket': "blissful-cell-393422.appspot.com",
  'messagingSenderId': "208919849448",
  'appId': "1:208919849448:web:f03dd4ad2812f3b81f5c5d",
  'measurementId': "G-D9FPTHTPYW",
  'databaseURL': " "
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'secret'



reading_history = []

def fetch_book_info(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key=AIzaSyDIWINaH8Q7cBshxqzDcHphJKLWvRRELQc"
    response = requests.get(url)
    
    if response.status_code == 200:
        book_data = response.json()  

        # Debug print to see the structure of book_data
        print(book_data)

        # Accessing data based on updated structure
        items = book_data.get('items', [])
        if items:
            volume_info = items[0].get('volumeInfo', {})
            title = volume_info.get('title', 'Unknown Title')
            authors = volume_info.get('authors', ['Unknown Author'])
            num_pages = volume_info.get('pageCount', 0)
            image_links = volume_info.get('imageLinks', {})
            small_thumbnail = image_links.get('smallThumbnail', '')
            thumbnail = image_links.get('thumbnail', '')
            
            
            
        return {
            'title': title,
            'author': ", ".join(authors),
            'num_pages': num_pages,
            'small_thumbnail': small_thumbnail,
            'thumbnail': thumbnail,
        }
    else:
        return {
            'title': 'Unknown Title',
            'author': 'Unknown Author',
            'num_pages': 0,
            'small_thumbnail': '',
            'thumbnail': '',
        }

def download_image(url):
    # Function to download and save the image locally
    if not url:
        return ''

    response = requests.get(url)

    if response.status_code == 200:
        # Generate a unique filename based on the URL
        filename = os.path.basename(url)
        filename = "".join(x for x in filename if x.isalnum() or x in ('.', '-', '_'))

        print(f"Downloading image from URL: {url}")
        print(f"Saving to filename: {filename}")

        filepath = os.path.join("static/images", filename)

        with open(filepath, "wb") as file:
            file.write(response.content)
        return f"images/{filename}"
    else:
        return ''

@app.route('/')
def index():
    current_date = datetime.now()
    return render_template('index.html', reading_history=reading_history, current_date=current_date)
   
   
        
@app.route('/login')
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
           user = auth.sign_in_with_email_and_password(email, password)
           session['user'] = 'email'
        except:
            return 'Failed to login'
        return render_template('index.html')

    
@app.route('/reset')
def reset():
    return render_template('reset.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

# Route for logout
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user session to log out
    session.pop('user', None)
    return render_template('login.html')


@app.route('/add_book', methods=['POST'])
def add_book():
    book_title = request.form.get('book_title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    book_info = fetch_book_info(isbn)

    if 'progress' in book_info and book_info['progress'] == 100:
        status = f'Finished {datetime.now().strftime("%m/%d/%Y")}'
    else:
        status = 'Reading'
    
  

    # Add the book with the status
    reading_history.append({
        'title': book_info.get('title', book_title),
        'author': book_info.get('author', author),
        'num_pages': book_info.get('num_pages', 0),
        'progress': book_info.get('progress', 0),
        'pages_read': book_info.get('pages_read', 0),
        'status': status,
        
    })

    return redirect(url_for('index'))




@app.route('/update_progress/<int:index>', methods=['POST'])
def update_progress(index):
    pages_read = int(request.form.get('pages_read'))
    num_pages = reading_history[index]['num_pages']

    if 0 <= pages_read <= num_pages - reading_history[index]['pages_read']:
        reading_history[index]['pages_read'] += pages_read
        reading_history[index]['progress'] = (reading_history[index]['pages_read'] / num_pages) * 100

        if reading_history[index]['progress'] == 100:
            book = reading_history.pop(index)
            book['progress'] = 100
            reading_history.append(book)
    else:
        # Handle invalid pages_read value later (you can show an error message)
        pass

    return redirect(url_for('index'))

@app.route('/delete_book/<int:index>', methods=['POST'])
def delete_book(index):
    if 0 <= index < len(reading_history):
        del reading_history[index]
    return redirect(url_for('index'))



#The endpoint that scrobble books from Kindle Cloud Reader
@app.route("/scrobble_kindle_cloud_reader")
def scrobble_kindle_cloud_reader():
    # Get the client ID and client secret from the request.
    client_id = request.form["client_id"]
    client_secret = request.form["client_secret"]

    # Use the client ID and client secret to get the user's Kindle Cloud Reader library.
    library = get_kindle_cloud_reader_library(client_id, client_secret)

    # Scrobble the books that the user has read.
    scrobble_books(library)

    return "Books scrobbled!"

if __name__ == '__main__':
    app.run(debug=True)