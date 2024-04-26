from lib.album import Album

"""
When I construct an Album
With the fields id, title, release year and artist id 
They are reflected in the instance properties
"""

def test_constructs_with_fields():
    album = Album(1, "Red", 2012, 2)
    assert album.id == 1
    assert album.title == "Red"
    assert album.release_year == 2012
    assert album.artist_id == 2
"""
When I construct two Albums with the same fields they are equal 
"""
def test_equality():
    album_1 = Album(1, "Red", 2017, 2)
    album_2 = Album(1, "Red", 2017, 2)
    assert album_1 == album_2


"""
We can format artists to strings nicely
"""
def test_albums_format_nicely():
    album = Album(1, "Test Album", 2000, 4)
    assert str(album) == "Album(1, Test Album, 2000, 4)"