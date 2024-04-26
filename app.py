import os
from flask import Flask, request, redirect, render_template
from lib.database_connection import get_flask_database_connection
from lib.album_repository import AlbumRepository
from lib.album import *
from lib.artist import *
from lib.artist_repository import ArtistRepository


# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==


# == Example Code Below ==

# GET /emoji
# Returns a smiley face in HTML
# Try it:
#   ; open http://localhost:5001/emoji
@app.route('/emoji', methods=['GET'])
def get_emoji():
    # We use `render_template` to send the user the file `emoji.html`
    # But first, it gets processed to look for placeholders like {{ emoji }}
    # These placeholders are replaced with the values we pass in as arguments
    return render_template('emoji.html', emoji=':)')


# This imports some more example routes for you to see how they work
# You can delete these lines if you don't need them.
from example_routes import apply_example_routes
apply_example_routes(app)

# == End Example Code ==

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.

    
@app.route('/albums')
def get_albums():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    albums = repository.all()
    return render_template("albums/index.html", albums=albums)

@app.route('/artists')
def get_artists():
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    artists = repository.all()
    return render_template("artists/index.html", artists=artists)


@app.route('/albums/<int:id>', methods=['GET'])
def get_album(id):
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    album = repository.find(id)
    repository = ArtistRepository(connection)
    artist = repository.find(album.artist_id)
    return render_template('albums/show.html', album=album, artist=artist)


# @app.route('/albums/<int:id>', methods=['GET'])
# def get_album(id):
#     connection = get_flask_database_connection(app)
#     repository = AlbumRepository(connection)
#     album = repository.find(id)
#     return render_template('albums/show.html', album=album)

@app.route('/artists/<int:id>', methods=['GET'])
def get_artist(id):
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    artist = repository.find(id)
    return render_template('artists/show.html', artist=artist)

@app.route('/albums/new', methods=['GET'])
def get_album_new():
    return render_template('albums/new.html')

@app.route('/albums', methods=['POST'])
def create_album():
    connection = get_flask_database_connection(app)
    album_repository = AlbumRepository(connection)
    title = request.form['title']
    release_year = request.form['release_year']
    artist_name = request.form['artist_name']
    artist_repository = ArtistRepository(connection)
    artist_id = artist_repository.findbyname(artist_name)
    if artist_id != "Artist not found":
        album = Album(None, title, release_year, artist_id)
        if not album.is_valid():
            errors = album.generate_errors()
            return render_template('albums/new.html', errors=errors)
        elif album.is_valid():
            album_repository.create(album)
            return redirect(f"/albums/{album.id}")
    else:
        return render_template('/albums/error.html')
    
    
@app.route('/albums/error', methods=['GET'])
def error_page_create_artist():
    return render_template('/albums/error.html')

    
@app.route('/artists/new', methods=['GET'])
def get_artist_new():
    return render_template('artists/new.html')

@app.route('/artists', methods=['POST'])
def create_artist():
    connection = get_flask_database_connection(app)
    artist_repository = ArtistRepository(connection)
    name = request.form['name']
    genre = request.form['genre']
    artist = Artist(None, name, genre)
    artist_repository.create(artist)
    return redirect(f"/artists/{artist.id}")


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))


# @app.route('/artists', methods=['GET'])
# def get_artists():
#     connection = get_flask_database_connection(app)
#     repository = ArtistRepository(connection)
#     artists = repository.all()
#     response = ''
#     for i, artist in enumerate(artists):
#         response += f"{artist}"
#         if i < len(artists) - 1:
#             response += ", "
#     return response

# @app.route('/albums', methods=['GET'])
# def get_albums():
#     connection = get_flask_database_connection(app)
#     repository = AlbumRepository(connection)
#     albums = repository.all()
#     response = ''
#     for i, album in enumerate(albums):
#         response += f"{album}"
#         if i < len(albums) - 1:
#             response += ", "
# #     return response

# @app.route('/artists', methods=['POST'])
# def create_new_artist():
#     connection = get_flask_database_connection(app)
#     repository = ArtistRepository(connection)
#     name = request.form['name']
#     genre = request.form['genre']
#     artist = Artist(None, name, genre)
#     repository.create(artist)
#     return "New artist successfully added!"

# @app.route('/artists', methods=['GET'])
# def get_artists():
#     connection = get_flask_database_connection(app)
#     repository = ArtistRepository(connection)
#     artists = repository.all()
#     response = ''
#     for i, artist in enumerate(artists):
#         response += f"{artist}"
#         if i < len(artists) - 1:
#             response += ", "
#     return response

# @app.route('/albums', methods=['POST'])
# def create_new_album():
#     connection = get_flask_database_connection(app)
#     repository = AlbumRepository(connection)
#     title = request.form['title']
#     release_year = request.form['release_year']
#     artist_id = request.form['artist_id']
#     album = Album(None, title, release_year, artist_id)
#     repository.create(album)
#     return "New album successfully added!"


# @app.route('/albums', methods=['POST'])
# def create_album():
#     connection = get_flask_database_connection(app)
#     album_repository = AlbumRepository(connection)
#     title = request.form['title']
#     release_year = request.form['release_year']
#     artist_name = request.form['artist_name']
#     artist_repository = ArtistRepository(connection)
#     artist_id = artist_repository.findbyname(artist_name)
#     if artist_id != "Artist not found":
#         album = Album(None, title, release_year, artist_id)
#         album_repository.create(album)
#         return redirect(f"/albums/{album.id}")
#     else:
#         return "Not found"
#         # POST artists method 
#         print("Corresponding artist does not exist. Please add artist first.")

    # PUT THIS AFTER ARTIST NAME if title == "" or release_year == "" or artist_name == "":
    #     errors = "There are errors in your submission. Inputs can't be blank."
    #     return render_template('albums/new.html', errors=errors)