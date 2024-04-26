from lib.artist import Artist

class ArtistRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all artists
    def all(self):
        rows = self._connection.execute('SELECT * from artists')
        artists = []
        for row in rows:
            item = Artist(row["id"], row["name"], row["genre"])
            artists.append(item)
        return artists

    # Find a single artist by their id
    def find(self, artist_id):
        rows = self._connection.execute(
            'SELECT * from artists WHERE id = %s', [artist_id])
        row = rows[0]
        return Artist(row["id"], row["name"], row["genre"])
    
    # Find a single artist by their name, return error message if not found and return artist_id if found
    def findbyname(self, name):
        rows = self._connection.execute(
            'SELECT * from artists WHERE name = %s', [name])
        if rows:
            row = rows[0]
            return row["id"]
        else:
            return "Artist not found"

    # Create a new artist
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, artist):
        rows = self._connection.execute('INSERT INTO artists (name, genre) VALUES (%s, %s) RETURNING id', [
                                 artist.name, artist.genre])
        row = rows[0]
        artist.id = row["id"]
        return artist 

    # Delete an artist by their id
    def delete(self, artist_id):
        self._connection.execute(
            'DELETE FROM artists WHERE id = %s', [artist_id])
        return None
