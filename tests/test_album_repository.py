from lib.album_repository import *
from lib.album import *

"""
When I call the all method on the AlbumRepository
I get all albums back in a list
"""

def test_list_all_albums(db_connection):
    db_connection.seed("seeds/albums_table.sql")
    repository = AlbumRepository(db_connection)
    albums = repository.all()
    assert albums == [
        Album(1, 'Doolittle', 1989, 1), 
        Album(2,'Surfer Rosa', 1988, 1), 
        Album(3, 'Waterloo', 1974, 2), 
        Album(4, 'Super Trouper', 1980, 2), 
        Album(5,'Bossanova', 1990, 1), 
        Album(6, 'Lover', 2019, 3), 
        Album(7, 'Folklore', 2020, 3), 
        Album(8, 'I Put a Spell on You', 1965, 4), 
        Album(9, 'Baltimore', 1978, 4), 
        Album(10, 'Here Comes the Sun', 1971, 4), 
        Album(11, 'Fodder on My Wings', 1982, 4), 
        Album(12, 'Ring Ring', 1973, 2)
        ]


"""
When we call AlbumRepository#find
We get a single Album object reflecting the seed data.
"""
def test_get_single_record(db_connection):
    db_connection.seed("seeds/albums_table.sql")
    repository = AlbumRepository(db_connection)

    album = repository.find(3)
    assert album == Album(3, 'Waterloo', 1974, 2)

"""
When we call AlbumRepository#create
We get a new record in the database.
"""
def test_create_record(db_connection):
    db_connection.seed("seeds/albums_table.sql")
    repository = AlbumRepository(db_connection)

    repository.create(Album(None, "Red", 2017, 5))

    albums = repository.all()
    assert albums == [
        Album(1, 'Doolittle', 1989, 1), 
        Album(2,'Surfer Rosa', 1988, 1), 
        Album(3, 'Waterloo', 1974, 2), 
        Album(4, 'Super Trouper', 1980, 2), 
        Album(5,'Bossanova', 1990, 1), 
        Album(6, 'Lover', 2019, 3), 
        Album(7, 'Folklore', 2020, 3), 
        Album(8, 'I Put a Spell on You', 1965, 4), 
        Album(9, 'Baltimore', 1978, 4), 
        Album(10, 'Here Comes the Sun', 1971, 4), 
        Album(11, 'Fodder on My Wings', 1982, 4), 
        Album(12, 'Ring Ring', 1973, 2), 
        Album(13, "Red", 2017, 5)
        ]


"""
When we call ArtistRepository#delete
We remove a record from the database.
"""
def test_delete_record(db_connection):
    db_connection.seed("seeds/albums_table.sql")
    repository = AlbumRepository(db_connection)
    repository.delete(13) # Apologies to Taylor Swift fans

    albums = repository.all()
    assert albums == [
        Album(1, 'Doolittle', 1989, 1), 
        Album(2,'Surfer Rosa', 1988, 1), 
        Album(3, 'Waterloo', 1974, 2), 
        Album(4, 'Super Trouper', 1980, 2), 
        Album(5,'Bossanova', 1990, 1), 
        Album(6, 'Lover', 2019, 3), 
        Album(7, 'Folklore', 2020, 3), 
        Album(8, 'I Put a Spell on You', 1965, 4), 
        Album(9, 'Baltimore', 1978, 4), 
        Album(10, 'Here Comes the Sun', 1971, 4), 
        Album(11, 'Fodder on My Wings', 1982, 4), 
        Album(12, 'Ring Ring', 1973, 2)
        ]
