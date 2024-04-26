from playwright.sync_api import Page, expect
import os 
from lib.database_connection import get_flask_database_connection
from lib.album_repository import *
from lib.album import *
from flask import Flask, request


# Tests for your routes go here

# === Example Code Below ===

"""
We can get an emoji from the /emoji page
"""
def test_get_emoji(page, test_web_address): # Note new parameters
    # We load a virtual browser and navigate to the /emoji page
    page.goto(f"http://{test_web_address}/emoji")

    # We look at the <strong> tag
    strong_tag = page.locator("strong")

    # We assert that it has the text ":)"
    expect(strong_tag).to_have_text(":)")


# === End Example Code ===

def test_get_albums(page, test_web_address, db_connection):
    db_connection.seed('seeds/albums_table.sql')
    page.goto(f"http://{test_web_address}/albums")
    div_tags = page.locator("div")
    expect(div_tags).to_have_text([f"Title: Doolittle\nReleased: 1989",
                                f"Title: Surfer Rosa\nReleased: 1988",
                                f"Title: Waterloo\nReleased: 1974",
                                f"Title: Super Trouper\nReleased: 1980",
                                f"Title: Bossanova\nReleased: 1990",
                                f"Title: Lover\nReleased: 2019",
                                f"Title: Folklore\nReleased: 2020",
                                f"Title: I Put a Spell on You\nReleased: 1965",
                                f"Title: Baltimore\nReleased: 1978",
                                f"Title: Here Comes the Sun\nReleased: 1971",
                                f"Title: Fodder on My Wings\nReleased: 1982",
                                f"Title: Ring Ring\nReleased: 1973"])
    
def test_get_artists(page, test_web_address, db_connection):
    db_connection.seed('seeds/albums_table.sql')
    page.goto(f"http://{test_web_address}/artists")
    div_tags = page.locator("div")
    expect(div_tags).to_have_text([f"Name: Pixies\nGenre: Rock",
                                f"Name: ABBA\nGenre: Pop",
                                f"Name: Taylor Swift\nGenre: Pop",
                                f"Name: Nina Simone\nGenre: Jazz"])



def test_get_album(db_connection, page, test_web_address):
    db_connection.seed("seeds/albums_table.sql")
    page.goto(f"http://{test_web_address}/albums/1")
    heading = page.locator("h1")
    expect(heading).to_have_text(f"Doolittle")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text(f"Release year: 1989\nArtist: Pixies")


# def test_get_album(db_connection, page, test_web_address):
#     db_connection.seed("seeds/albums_table.sql")
#     page.goto(f"http://{test_web_address}/albums/1")
#     heading = page.locator("h1")
#     expect(heading).to_have_text(f"Doolittle")
#     p_tags = page.locator("p")
#     expect(p_tags).to_have_text(f"Release year: 1989")


def test_visit_album_show_page(db_connection, page, test_web_address):
    db_connection.seed('seeds/albums_table.sql')
    page.goto(f"http://{test_web_address}/albums")
    page.click(f"text=Title: Doolittle\nReleased: 1989")
    heading = page.locator("h1")
    expect(heading).to_have_text(f"Doolittle")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text(f"Release year: 1989\nArtist: Pixies")

def test_get_artist(db_connection, page, test_web_address):
    db_connection.seed("seeds/albums_table.sql")
    page.goto(f"http://{test_web_address}/artists/1")
    heading = page.locator("h1")
    expect(heading).to_have_text(f"Pixies")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text(f"Genre: Rock")

# def test_get_artist_new(db_connection, page, test_web_address):
#     db_connection.seed('seeds/albums_table.sql')
#     page.set_default_timeout(1000)
#     page.goto(f"http://{test_web_address}/artists")
#     page.click('text="Add artist"')

#     page.fill('input[name=name]', "Test Name")
#     page.fill('input[name=genre]', "Test Genre")

#     page.click('text="Submit artist"')

#     # heading = page.locator("h1")
#     # expect(heading).to_have_text(f"Pixies")
#     # p_tags = page.locator("p")
#     # expect(p_tags).to_have_text(f"Genre: Rock")


def test_get_album_new(db_connection, page, test_web_address):
    db_connection.seed('seeds/albums_table.sql')
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/albums")
    page.click('text="Add album"')
    page.fill('input[name=title]', "Test Album")
    page.fill('input[name=release_year]', "1989")
    page.fill('input[name=artist_name]', "Pixies")
    page.click('text="Submit album"')
    heading = page.locator("h1")
    expect(heading).to_have_text(f"Test Album")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text(f"Release year: 1989\nArtist: Pixies")

#When I add an album without any of the things filled in, get an error message
def test_get_album_new_with_errors(db_connection, page, test_web_address):
    db_connection.seed('seeds/albums_table.sql')
    page.set_default_timeout(30000)
    page.goto(f"http://{test_web_address}/albums")
    page.click('text="Add album"')
    page.fill('input[name=title]', "Test Album")
    page.fill('input[name=artist_name]', "Pixies")
    page.click('text="Submit album"')
    errors_tag = page.locator(".t-errors")
    expect(errors_tag).to_have_text("Release year can't be blank")

def test_try_to_add_album_without_artist(db_connection, page, test_web_address):
    db_connection.seed('seeds/albums_table.sql')
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/albums")
    page.click('text="Add album"')
    page.fill('input[name=title]', "Test Album")
    page.fill('input[name=release_year]', "1989")
    page.fill('input[name=artist_name]', "Lana Del Rey")
    page.click('text="Submit album"')
    heading = page.locator("h1")
    expect(heading).to_have_text(f"Artist is not currently in database")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text(f"Please add artist and try again!")

def test_get_artist_new(db_connection, page, test_web_address):
    db_connection.seed('seeds/albums_table.sql')
    page.set_default_timeout(30000)
    page.goto(f"http://{test_web_address}/artists")
    page.click('text="Add artist"')
    page.fill('input[name=name]', "Test Name")
    page.fill('input[name=genre]', "Test Genre")
    page.click('text="Submit artist"')
    heading = page.locator("h1")
    expect(heading).to_have_text(f"Test Name")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text(f"Genre: Test Genre")






# def test_new_album_successfully_created(web_client, db_connection):
#     db_connection.seed('seeds/albums_table.sql')
#     response = web_client.post('/albums', data={'title': 'Tortured Poets Society', 'release_year': 2024, 'artist_id': 3})
#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == 'New album successfully added!'
#     response = web_client.get('/albums')
#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == "Album(1, Doolittle, 1989, 1), Album(2, Surfer Rosa, 1988, 1), Album(3, Waterloo, 1974, 2), Album(4, Super Trouper, 1980, 2), Album(5, Bossanova, 1990, 1), Album(6, Lover, 2019, 3), Album(7, Folklore, 2020, 3), Album(8, I Put a Spell on You, 1965, 4), Album(9, Baltimore, 1978, 4), Album(10, Here Comes the Sun, 1971, 4), Album(11, Fodder on My Wings, 1982, 4), Album(12, Ring Ring, 1973, 2), Album(13, Tortured Poets Society, 2024, 3)"

# def test_get_albums_separate_method(web_client, db_connection):
#     db_connection.seed('seeds/albums_table.sql')
#     response = web_client.get('/albums')
#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == "Album(1, Doolittle, 1989, 1), Album(2, Surfer Rosa, 1988, 1), Album(3, Waterloo, 1974, 2), Album(4, Super Trouper, 1980, 2), Album(5, Bossanova, 1990, 1), Album(6, Lover, 2019, 3), Album(7, Folklore, 2020, 3), Album(8, I Put a Spell on You, 1965, 4), Album(9, Baltimore, 1978, 4), Album(10, Here Comes the Sun, 1971, 4), Album(11, Fodder on My Wings, 1982, 4), Album(12, Ring Ring, 1973, 2)" 

# def test_get_artists(web_client, db_connection):
#     db_connection.seed('seeds/albums_table.sql')
#     response = web_client.get('/artists')
#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == "Artist(1, Pixies, Rock), Artist(2, ABBA, Pop), Artist(3, Taylor Swift, Pop), Artist(4, Nina Simone, Jazz)"

# def test_new_artist_successfully_created(web_client, db_connection):
#     db_connection.seed('seeds/albums_table.sql')
#     response = web_client.post('/artists', data={'name': 'Wild nothing', 'genre': 'Indie'})
#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == "New artist successfully added!"
#     response = web_client.get('/artists')
#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == "Artist(1, Pixies, Rock), Artist(2, ABBA, Pop), Artist(3, Taylor Swift, Pop), Artist(4, Nina Simone, Jazz), Artist(5, Wild nothing, Indie)"
