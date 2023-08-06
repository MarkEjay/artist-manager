import requests
import json
import os
import base64
import spotipy
from spotipy.oauth2 import SpotifyPKCE
import pandas as pd

# TICKETMASTER_KEY="yR57NIPjhMofAacNGhhmqKhT6tdUKDYM"
# url= f"https://app.ticketmaster.com/discovery/v2/events?apikey={TICKETMASTER_KEY}&locale=*&countryCode=CA"
# url +="&keyword=rema"
# # concert_artists.append(url)
# response=requests.get(url)
# json_response = response.json()
# print(json_response["_embedded"]["events"][1]["_embedded"]["venues"][0]["name"])

SPOTIPY_CLIENT_ID = ""
SPOTIPY_REDIRECT_URI = ""
TICKETMASTER_KEY=""



def top_artists():
    scope = "user-library-read"
    scope = "user-top-read"

    sp = spotipy.Spotify(SpotifyPKCE(
        SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI, scope=scope).get_access_token())
    # user = sp.current_user()
    top = sp.current_user_top_artists()

    artists = []
    artistsID=[]
    key = ["name"]
    for x in top["items"]:
        artists.append(x['name'])
        artistsID.append(x['id'])
        df = pd.DataFrame({
            "Artists Name": artists,
            "Artists ID":artistsID
        })

        df.index.name = "ID"
    df.to_csv("my_top_artists(past_6_months).csv")
    # print(artistsID)
    return artists


def find_concert(artist):
    concert_artists=[]
    # url= f"https://app.ticketmaster.com/discovery/v2/events?apikey={TICKETMASTER_KEY}&locale=*&countryCode=CA"
    # url +="&keyword="+artist

    # print(url)
    concert_dates=[]
    artist_with_concerts=[]
    concert_name=[]
    public_sales_date=[]
    venue=[]
    for x in artist:
        url= f"https://app.ticketmaster.com/discovery/v2/events?apikey={TICKETMASTER_KEY}&locale=*&countryCode=CA"
        url +="&keyword="+x
        concert_artists.append(url)
        response=requests.get(url)
        json_response = response.json()
        if "_embedded" in json_response:
            artist_with_concerts.append(x)
            concert_dates.append(json_response["_embedded"]["events"][0]["dates"]["start"]["localDate"])
            concert_name.append(json_response["_embedded"]["events"][0]["name"])
            public_sales_date.append(json_response["_embedded"]["events"][0]["sales"]["public"]["startDateTime"])
            df = pd.DataFrame({
            "Artists Name": artist_with_concerts,
            "Concert Date":concert_dates,
            "Concert Name":concert_name,
            "Public Sales Date":public_sales_date
        })

        df.index.name = "ID"
        df.to_csv("top_artists_concerts.csv")


    


find_concert(top_artists())


