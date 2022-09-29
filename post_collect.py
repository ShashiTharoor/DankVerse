'''
This Script is used to collect posts of a few dank meme subreddits.

it collects the posts and save them in json files.
Later that data is used in Main script.

You need to run This Script 24x7.
If You wanna collect post of a hig traffic subreddit then change sleep time. 
schedule.every(10).minutes.do(main)  accordingly
'''

import praw, json, time, logging, traceback, re
import schedule


reddit = Your Credentials
done = []
last_created_utc=int(time.time())
created_utc=last_created_utc
count=0
i=1


logging.basicConfig(filename="post_collect_log.txt",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

feeds=[]
subs="IndianDankMemes+dankinindia+SaimanSays+dankrishu+sunraybee"
subreddit=reddit.subreddit(subs)
date=int(time.strftime('%d'))
def main():
    try:
        global i, last_created_utc, subs, created_utc, count, feeds, date
        count+=1
        logger.info("count "+str(count)+" : "+ str(done))
        for submission in subreddit.new(limit=25):
            if count==0:
                done.append(submission.id)
                body = {"id": submission.id, "url": submission.url, "author": submission.author.name, "sub": re.split('/', submission.permalink)[2]}
                feeds.append(body)
            else:
              if submission.id not in done:
                done.append(submission.id)
                body = {"id": submission.id, "url": submission.url, "author": submission.author.name, "sub": re.split('/', submission.permalink)[2]}
                feeds.append(body)
                if date!=int(time.strftime('%d')):
                    i+=1
                    logger.info(str(i) + '_dank.json dumped data')
                    date=int(time.strftime('%d'))
                    feeds=[]
                with open(str(i) + '_dank.json', mode='w+', encoding='utf-8') as feedsjson:
                    json.dump(feeds, feedsjson, indent = 1)
    except Exception as e:
      traceback.print_exc()
      logger.exception(e)
      print(e)

def main2():
    try:
        global i
        logging.basicConfig(filename="dank-log.txt",
                            format='%(asctime)s %(message)s',
                            filemode='a')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        date=int(time.strftime('%d'))
        feeds=[]
        for submission in reddit.subreddit("IndianDankMemes+dankinindia+SaimanSays+dankrishu+sunraybee").stream.submissions(skip_existing=True):
            # logger.info('sub: ' + submission.subreddit.name)
            body = {"id": submission.id, "url": submission.url, "author": submission.author.name, "sub": re.split('/', submission.permalink)[2]}
            feeds.append(body)
            if date!=int(time.strftime('%d')):
                i+=1
                logger.info(str(i) + '_dank.json dumped data')
                with open(str(i) + '_dank.json', mode='w+', encoding='utf-8') as feedsjson:
                    json.dump(feeds, feedsjson)
                    break
    except Exception as e:
      traceback.print_exc()
      logger.exception(e)
      print(e)



# while True:
#     main()

main()
schedule.every(10).minutes.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
