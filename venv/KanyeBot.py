# import the random library to help us generate the random numbers
import random
import re
import requests
from auxpack import intro
# Create the KanyeBot Class
class KanyeBot:

    # Create a constant that contains the default text for the message
    KANYE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                random.choice(intro) + "\n\n"
            ),
        },
    }

    # The constructor for the class. It takes the channel name as the a
    # parameter and then sets it as an instance variable
    def __init__(self, channel, band):
        self.channel = channel
        self.band = band

    # random.choice(list) to get random song from album
    # count = get number of pages in playlist
    # random(0,count)
    # random(0, number of items on page)
    # get title, id and stick it into youtube_video hyperlink and return it
    def _find_song(self, band):
        # prefix for youtube video url
        youtube_video_prefix = "https://www.youtube.com/watch?v="
        # base page of playlist
        #yelist = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&pageToken=CDIQAQ&playlistId=PLiz939OBsRP_UdcXTU1BrcY7QQHXQMy2z&key=AIzaSyBXIMj-Pg8YYb3z1DqFpUQnsUTWjOA1bXY"
        yelist = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId=INSERT+ID+HERE&key=AIzaSyBXIMj-Pg8YYb3z1DqFpUQnsUTWjOA1bXY"
        yeSearch = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={band}&type=playlist&key=AIzaSyCH1u7Y1V7hm9kJwp1FRDl0H1s0e--WA9E"
        print(yeSearch)
        yeSON_search = requests.get(yeSearch).json()
        #yeSON_search = get_search(band)
        first_playlist_id = yeSON_search["items"][0]["id"]["playlistId"]
        print(f"first playlistId on page {first_playlist_id}")
        # current page of playlist used during iterations through the pages of the playlist
        yelist = re.sub(r'(.*playlistId=).*(&key.*)', r'\1'+first_playlist_id+r'\2', yelist)
        print(f"playlist link: {yelist}")
        curr_page = yelist
        # json file of playlist
        yeSON = requests.get(curr_page).json()
        total_results = yeSON["pageInfo"]["totalResults"]
        print(f"total results: {total_results}")
        if total_results == 50:
            total_pages = 0
        else:
            total_pages = (total_results // 50)
        page_turns = 0
        # edge case: there's exactly 50 pages on the last page
        if (total_results > 50 and total_results % 50 != 0):
            total_pages -= 1
        print(f"total pages: {total_pages}")

        if total_pages != 0:
            pageToken = "pageToken=" +yeSON["nextPageToken"]
            print(f"firsts pageToken: {pageToken}")
            page_turns = random.randint(0, total_pages - 1)
            curr_page = re.sub(r'(maxResults=50&).*(playlistId=.*)', r'\1' + pageToken + r'&\2', yelist)
            print(f"curr_page: {curr_page}")
            yeSON = requests.get(curr_page).json()
        # get to the right page
        print(f"turn {page_turns} pages")

        for i in range(total_pages):
            pageToken = yeSON["nextPageToken"]
            print(f"pagetoken {i} = {pageToken}")
            # use regex to set curr_page to our randomly chose page
            curr_page = re.sub(r'(.*pageToken=).*(&playlist.*)', r'\1' + pageToken + r'&\2', curr_page)
            print(f"json link for page {i}: {curr_page}")
            print(f"{i} pages turned")
            yeSON = requests.get(curr_page).json()
            print(f"song 1 page {i} " + yeSON["items"][0]["snippet"]["title"])

        # get random index from page and use it to get random song title, and id to build hyperlink with youtube video url
        length = len(yeSON["items"]) - 1
        print(length)

        index = random.randint(0, length)
        print(f"lets go to index: {index}")

        title = yeSON["items"][index]["snippet"]["title"]
        print(title)

        song_id = yeSON["items"][index]["contentDetails"]["videoId"]
        print(song_id)

        href = youtube_video_prefix + song_id
        print(href)

        text = f"<{href}|{title}>"


        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self, band):
        return {
            "channel": self.channel,
            "blocks": [
                self.KANYE_BLOCK,
                *self._find_song(band),
            ],
        }