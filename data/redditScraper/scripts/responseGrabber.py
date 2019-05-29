#NOTE: runs with python2.7
#SEE: /home/sbailey6/sbailey6/work/redditscraper/scripts/subreddit_csv_maker.py for examples of scraping an entire subreddit

import numpy as np
import urllib, json
import datetime as dt

hub_directory = "/home/sbailey6/Desktop/textGenerator/paraphraseGen/data/AA/script/"
comment_ids_URL = "https://api.pushshift.io/reddit/submission/comment_ids/"
comment_extraction_URL = "https://api.pushshift.io/reddit/search/comment/?ids="
submission_extraction_URL = "https://api.pushshift.io/reddit/search/submission/?ids="

#start by extracting all page ids were original post mentions relapse or struggle
def getPageIds():
    page_ids = set()

    subreddit = raw_input("Enter the subreddit you want to collect data from: ")
    vocab = map(str.strip, raw_input("Enter comma separated list of words that you require in a submission's text: ").split(','))

    total = 1001
    before_field = "0d"
    while(total > 1000):
        url = urllib.urlopen("https://api.pushshift.io/reddit/submission/search?subreddit=" + subreddit + "&metadata=true&before=" + before_field + "&limit=1000&sort=desc")
        user_data = json.loads(url.read().decode())
        sub_num = user_data["metadata"]["results_returned"]
        total = user_data["metadata"]["total_results"]
        for j in range(0, sub_num):
            submission = user_data["data"][j]
            try:
                title = '' .join([i if ord(i) < 128 else ' ' for i in submission["title"].replace(u"\u2019", "'").replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")])
                body = '' .join([i if ord(i) < 128 else ' ' for i in submission["selftext"].replace(",", "").replace(u"\u2019", "'").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")])
                for word in vocab:
                    if word in title.lower() or word in body.lower():
                        page_ids.add(submission["id"])
            except KeyError:
                pass
            if(j == sub_num -1):
                before_field = str(user_data["data"][sub_num - 1]["created_utc"])
    print("Finished extracting " + str(len(page_ids)) + " relevant submission posts from " + subreddit + "\n\n")
    return page_ids

def getImmediateResponses(page_id):
    
    url = urllib.urlopen(comment_ids_URL + page_id)
    response_ids = json.loads(url.read().decode())["data"]
    comment_num = len(response_ids)
    url.close()

    comment_str = ""
    for comment_id in response_ids:
        comment_str += comment_id + ","
    comment_str = comment_str[:-1]

    responses = []

    url = urllib.urlopen(comment_extraction_URL + comment_str)
    reply = json.loads(url.read().decode())["data"]
    for j in range(0, comment_num):
        if(reply[j]["parent_id"][3:] != page_id):
            continue
        response_body = reply[j]["body"]
        responses.append(response_body)
    
    return responses


def main():
    page_ids = getPageIds()
    count = 0
    mul = 10
    for page_id in page_ids:
        count+= 1
        if(count*100 / len(page_ids) >= mul):
            print(str(mul) + "%\t")
            mul += 10
        responses = getImmediateResponses(page_id)
        file = open(page_id + ".txt", 'w')
        file.write("-------original submission--------\n\n")
        url = urllib.urlopen(submission_extraction_URL + page_id)
        reply = json.loads(url.read().decode())["data"][0]
        
        try:
            sub_body = reply["selftext"]
            link = "reddit.com" + reply["permalink"]
        except:
            continue
        
        url.close()
        file.write("link: " + '' .join([i if ord(i) < 128 else ' ' for i in link.replace(u"\u2019", "'").replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + "\n\n")
        file.write('' .join([i if ord(i) < 128 else ' ' for i in sub_body.replace(u"\u2019", "'").replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + "\n")
        file.write("----------immediate responses--------\n\n")
        for entry in responses:
            file.write('' .join([i if ord(i) < 128 else ' ' for i in entry.replace(u"\u2019", "'").replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + "\n")
        file.close()
    print("\n")
main()
    