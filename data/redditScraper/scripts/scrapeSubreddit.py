import urllib, json
import datetime as dt

subreddit = raw_input("Enter the subreddit you want to completely collect data from: ")

sub_csv = open(subreddit + '_submissions.csv', 'w')
sub_csv.write("author, title, body, score, id, url, num_comments(approx.), created \n")
total = 1001
before_field = "0d"
while(total > 1000):
	url = urllib.urlopen("https://api.pushshift.io/reddit/submission/search?subreddit=" + subreddit + "&metadata=true&before=" + before_field + "&limit=1000&sort=desc")
	user_data = json.loads(url.read().decode())
	sub_num = user_data["metadata"]["results_returned"]
	total = user_data["metadata"]["total_results"]
	for j in range(0, sub_num):
		submission = user_data["data"][j]
		sub_csv.write('' .join([i if ord(i) < 128 else ' ' for i in submission["author"].replace(u"\u2019", "'").replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		sub_csv.write('' .join([i if ord(i) < 128 else ' ' for i in submission["title"].replace(u"\u2019", "'").replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		try:
			sub_csv.write('' .join([i if ord(i) < 128 else ' ' for i in submission["selftext"].replace(",", "").replace(u"\u2019", "'").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		except KeyError:
			sub_csv.write("[none],")
		sub_csv.write(str(submission["score"]) + ",")
		sub_csv.write('' .join([i if ord(i) < 128 else ' ' for i in submission["id"].replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		sub_csv.write('' .join([i if ord(i) < 128 else ' ' for i in submission["url"].replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		sub_csv.write('' .join([i if ord(i) < 128 else ' ' for i in str(submission["num_comments"]).replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		sub_csv.write(dt.datetime.fromtimestamp(submission["created_utc"]).isoformat() + "\n")
		if(j == sub_num -1):
			before_field = str(user_data["data"][sub_num - 1]["created_utc"])
sub_csv.close()

comment_csv = open(subreddit + '_comments.csv', 'w')
comment_csv.write("redditor, submission_id, parent_id, body, id, created, score \n")
total = 1001
before_field = "0d"
while(total > 1000):
	url = urllib.urlopen("https://api.pushshift.io/reddit/comment/search?subreddit=" + subreddit + "&metadata=true&before=" + before_field + "&limit=1000&sort=desc")
	user_data = json.loads(url.read().decode())
	comment_num = user_data["metadata"]["results_returned"]
	total = user_data["metadata"]["total_results"]
	for j in range(0, comment_num):
		comment = user_data["data"][j]
		comment_csv.write('' .join([i if ord(i) < 128 else ' ' for i in comment["author"].replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		comment_csv.write('' .join([i if ord(i) < 128 else ' ' for i in comment["link_id"].replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		comment_csv.write('' .join([i if ord(i) < 128 else ' ' for i in str(comment["parent_id"]).replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		comment_csv.write('' .join([i if ord(i) < 128 else ' ' for i in comment["body"].replace(",", "").replace(u"\u2019", "'").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		comment_csv.write('' .join([i if ord(i) < 128 else ' ' for i in comment["id"].replace(",", "").replace(r"\r\n", ".").replace("\r", ".").replace("\n", ".")]) + ",")
		comment_csv.write(dt.datetime.fromtimestamp(comment["created_utc"]).isoformat() + ",")
		comment_csv.write(str(comment["score"]) + "\n")
		if(j == comment_num - 1):
			before_field = str(user_data["data"][comment_num - 1]["created_utc"])
comment_csv.close()