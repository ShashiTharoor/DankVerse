'''
This script used the post_collect data indentify which posts were removed then analyse its score and if its score is more than 50 then it posts that post in r/Dankverse

'''


import requests, json, re, praw, subprocess, os, time, traceback
import logging, random, schedule
from PIL import Image as PIL_Image
import imagehash


reddit1 = praw.Reddit(username="NewTonJhatka-")
reddit = praw.Reddit(username="Diligent_Ad9316")
removed=[]

hash_array_str=[]
with open("hashes.json", "a+") as file:
    for item in json.load(file):
        hash_array_str.append(item)

logging.basicConfig(filename="log-DankVerse.txt",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def hash_check(file, add=True):
        hash = imagehash.average_hash(PIL_Image.open(file))
        if str(hash) in hash_array_str:
            print('images are similar')
            return False
        else:
            print('images are not similar')
            # hash_array.append(hash)
            if add==True:
              hash_array_str.append(str(hash))
              with open("hashes.json", "w+") as file:
                  file.write(json.dumps(hash_array_str, indent = 1))
            return True

def process_video(url, author):
    try:
      os.system("rm -rf *mp4")
      os.system("yt-dlp '" + url + "' -o raw_DankVersevideo.mp4 >> log.txt")
      subprocess.call(['ffmpeg', '-i', 'raw_DankVersevideo.mp4', '-ss', '00:00:01.000', '-vframes', '1', 'watthumb.png', '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      # if os.path.getsize('raw_DankVersevideo.mp4') < 40453551:
      #   subprocess.call("ffmpeg -i raw_DankVersevideo.mp4 -vf 'pad=height=ih+30:x=0:y=0:color=black, drawtext=fontfile=/path/to/font.ttf:text='r\/DankVerse':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-th-5,drawtext=:text='r\/DankVerse':fontcolor=#e7e7e7:fontsize=h/50:x=20:y=(h-text_h)/2:box=1:boxcolor=black@0.5:boxborderw=3:x=w-text_w:y=(h-text_h)/2,drawtext=:text='u\/" + author + "':fontcolor=#e7e7e7:fontsize=h/50:x=20:y=(h-text_h)/2+60:box=1:boxcolor=black@0.5:boxborderw=3:x=w-text_w:y=(h-text_h)/2+60' -codec:a copy DankVersevideo.mp4 -y >> log.txt", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      # else:
      if hash_check('watthumb.png')==True:
        os.system("cp raw_DankVersevideo.mp4 DankVersevideo.mp4")
        return True
      else:
        return False
    except Exception as e:
      print(e)


def process_image(url, author):
    try:
      os.system("rm -rf *jpg")
      open('raw_DankVerseimage.jpg', 'wb').write(requests.get(url).content)
      if hash_check('raw_DankVerseimage.jpg')==True:
        subprocess.call("ffmpeg -i raw_DankVerseimage.jpg -vf 'drawtext=:text='r\/DankVerse':fontcolor=#e7e7e7:fontsize=h/50:x=20:y=(h-text_h)/2:box=1:boxcolor=black@0.5:boxborderw=3:x=w-text_w:y=(h-text_h)/2,drawtext=:text='u\/" + author + "':fontcolor=#e7e7e7:fontsize=h/50:x=20:y=(h-text_h)/2+60:box=1:boxcolor=black@0.5:boxborderw=3:x=w-text_w:y=(h-text_h)/2+60' -codec:a copy DankVerseimage.jpg -y >> log.txt", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
      else:
        return False
    except Exception as e:
      print(e)


def DankVerse(title, url, author):
  global logger
  permalink='Not uploaded'
  try:
    submission=None
    if bool(re.search("gif|gyfcat|.mp4|v.red", url))==True:
        if process_video(url, author) ==True:
          submission=reddit.subreddit('DankVerse').submit_video(title, video_path='DankVersevideo.mp4', thumbnail_path='watthumb.png')
          submission = reddit1.submission(submission.id)
          submission.mod.approve()
          permalink="https://www.reddit.com/r/Dankverse/comments/"+submission.id
          print(permalink)
    elif bool(re.search("jpg|jpeg|imgur|i.red|png", url))==True:
        if process_image(url, author) ==True:
          submission=reddit.subreddit('DankVerse').submit_image(title, 'DankVerseimage.jpg')
          submission = reddit1.submission(submission.id)
          submission.mod.approve()
          permalink="https://www.reddit.com/r/Dankverse/comments/"+submission.id
          print(permalink)
    return submission
  except Exception as e:
    print(e)
    traceback.print_exc()
    logger.exception(e)
    pass
  

i=1
def main():
    global i, logger
    i+=1
    logger.info(f"value of i is {str(i)}")
    done=[]
    for a3 in open("done-id.txt","r").read().splitlines():
      done.append(a3)
#      a3.close()
    file1=open('done-id.txt', 'a+')
    file2=open('removed-dank.json', 'a+')
    file=str(i) + "_dank.json"
    jso = json.load(open(file))
    for post in jso:
      id=post['id']
      print(id, end=", ")
      if id not in done:
        time.sleep(1)
        submission = reddit.submission(id=id)
        url=submission.url
        score=submission.score
        is_removed=submission.removed_by_category
        # print(is_removed)
        title=submission.title
        author='DankVerse'
        done.append(submission.id)
        if submission.author==None:
          author='deleted'
        else:
          author=submission.author.name
        body={"title": submission.title, "url": submission.url, "id": submission.id, "score": submission.score, "permalink": submission.permalink, "author": author}
        if is_removed=='moderator':
          if score>50 or bool(re.search("i.redd.it", submission.url, re.IGNORECASE)) == True:
            print(body)
            removed.append(body)
            file2.write(json.dumps(body) + ',\n')
          else:
            print(body)
    post_removed(removed, i)
    file1.close()
    file2.close()


def post_removed(removed, i):
  global logger
  removed_len=len(removed)
  print(removed_len)
  file1=open('done-id.txt', 'a+')
  for item in removed:
    try:
      permalink=item['permalink']
      title=item['title']
      url=item['url']
      author=item['author']
      id=item['id']
      print("uploading https://reddit.com/" + permalink)
      logger.info("uploading https://reddit.com/" + permalink + "\n")
      # time.sleep(60)
      file1.write(id + '\n')
      link=DankVerse(title, url, author)
      if link !=None:
        logger.info("submit id: https://redd.it/" + link.id + "\n\n")
        print("https://redd.it/" + link.id)
        try:
          try:
            comment=link.reply(body="Hi u/" + author + " Your post reddit.com" + permalink + " was removed by cuck mods\n\n**So we uploaded your video in r/DankVerse**\n\n\nPost url: https://redd.it/" + link.id + "\n\n Join r/DankVerse\n\n**For Removal Of This Post You can contact Mods**\n\n I am Not a Bot")
            comment = reddit1.comment(comment.id)
            comment.mod.approve()
            reddit1.redditor(author).message(subject="We uploaded your post", message="Hi u/" + author + " Your Post reddit.com" + permalink + " was removed \n\n**So we uploaded your video in r/DankVerse**\n\n\nPost url: https://redd.it/" + link.id + "\n\n Join r/DankVerse\n\n**For Removal Of This Post You can contact Mods**\n\n I am Not a Bot", from_subreddit="DankVerse")
          except:
            comment=link.reply(body="Hi u/" + author + " Your Video was removed by cuck mods So we uploaded your video in R/DankVerse\nPost url: Linking to subreddits or Any post is not allowed\n\n Checkout R/DankVerse\n\n I am Not a Bot")
            reddit1.redditor(author).message(subject="We uploaded your post", message="Hi u/" + author + " Your Video was removed So we uploaded your video in R/DankVerse\n\nPost url: https://redd.it/" + link.id + "\n Join R/DankVerse\n\n I am Not a Bot", from_subreddit="DankVerse")
            comment = reddit1.comment(comment.id)
            comment.mod.approve()
        except Exception as e:
            traceback.print_exc()
            logger.exception(e)
            pass
      time.sleep(64800/removed_len)
    except Exception as e:
          traceback.print_exc()
          logger.exception(e)
  file1.close()  
  print("processed todays data")




schedule.every().day.at("05:10:00").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)

