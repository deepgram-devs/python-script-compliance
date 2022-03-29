import asyncio
from deepgram import Deepgram
from dotenv import load_dotenv
from typing import Dict
from tabulate import tabulate
from colorama import init 
from colorama import Fore
import os

init()

load_dotenv()

PATH_TO_FILE = 'gettysburg.wav'

flagged_words = {
   "and": "This is a flagged word!",
   "are": "This is another flagged word!",
   "um": "This is a filler word!"
}

search_words = ["engaged in a great civil war", "new nation", "Ok I see"]

score_card = [] 

async def script_compliance(transcript_data: Dict) -> None:
    if 'results' in transcript_data:
        transcript = transcript_data['results']['channels'][0]['alternatives'][0]['transcript']

        # find the flagged words
        data = []

        for key,value in flagged_words.items():
            score_flagged_words = transcript.count(key) # number of occurences of key
            if score_flagged_words: # if there is a key, if it finds the key
                data.append([key, value]) # create a list of lists to hold our data in our table

            score_card.append(score_flagged_words)

        print(Fore.RED, tabulate(data, headers=["Flagged Word", "Warning Message"]))

        print()         

        # find the search words
        words = []
        for item in search_words:
            if item in transcript:
                words.append(["Yes", item])
            else:
                words.append(["No", item])

        print(Fore.GREEN, tabulate(words, headers=["Word(s) Found", "item"]))

        print()
    
        print(Fore.YELLOW, tabulate([[sum(score_card), len([w for w in words if w[0] == "Yes"])]], headers=["Flagged Word Count", "Search Word Count"]))

async def main():
    deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

    with open(PATH_TO_FILE, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        transcription = await deepgram.transcription.prerecorded(source, {'punctuate': True })

        speakers = await script_compliance(transcription)
    

asyncio.run(main())