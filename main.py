import requests, json, re, praw, subprocess, os, time, traceback
import logging, random, schedule
from PIL import Image as PIL_Image
import imagehash

reddit = praw.Reddit()
reddit1= reddit

removed=[]
i=0
subreddit=reddit.subreddit("IndianDankMemes+dankinindia+SaimanSays")
last_utc=None
fetched_data=[]

logging.basicConfig(filename="log-RealTime.txt",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lprint(text):
    logger.info(text)
    # print(text)

hash_array_str=[]
with open("data/hashes.json", "r") as file:
    for item in json.load(file):
        hash_array_str.append(item)

def hash_check(file, add=True):
        hash = imagehash.average_hash(PIL_Image.open(file))
        if str(hash) in hash_array_str:
            lprint('images are similar')
            return False
        else:
            lprint('images are not similar')
            # hash_array.append(hash)
            if add==True:
              hash_array_str.append(str(hash))
              with open("data/hashes.json", "w+") as file:
                  file.write(json.dumps(hash_array_str, indent = 1))
            return True
def process_video(url, author):
    try:
      os.system("rm -rf *mp4")
      os.system("yt-dlp '" + url + "' -o raw_DankVersevideo.mp4 >> log.txt")
      subprocess.call(['ffmpeg', '-i', 'raw_DankVersevideo.mp4', '-ss', '00:00:01.000', '-vframes', '1', 'watthumb.png', '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      if hash_check('watthumb.png')==True:
        if os.path.getsize('raw_DankVersevideo.mp4') < 40453551:
            subprocess.call(f"time ffmpeg -i raw_DankVersevideo.mp4 -vf 'drawtext=:text='u/{author}':fontcolor=#e7e7e7@0.5:fontsize=h/60:x=(w-text_w)/4:y=(h-th)/1.5' -preset ultrafast -r 15 -codec:a copy DankVersevideo.mp4 -y", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            os.system("cp raw_DankVersevideo.mp4 DankVersevideo.mp4")
        return True
      else:
        return False
    except Exception as e:
      print(e)


def process_image(url, author):
    try:
      os.system("rm -rf *jpg")
      open('DankVerseimage.jpg', 'wb').write(requests.get(url).content)
      if hash_check('DankVerseimage.jpg')==True:
        # subprocess.call("ffmpeg -i raw_DankVerseimage.jpg -vf 'drawtext=:text='r\/DankVerse':fontcolor=#e7e7e7:fontsize=h/50:x=20:y=(h-text_h)/2:box=1:boxcolor=black@0.5:boxborderw=3:x=w-text_w:y=(h-text_h)/2,drawtext=:text='u\/" + author + "':fontcolor=#e7e7e7:fontsize=h/50:x=20:y=(h-text_h)/2+60:box=1:boxcolor=black@0.5:boxborderw=3:x=w-text_w:y=(h-text_h)/2+60' -codec:a copy DankVerseimage.jpg -y >> log.txt", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
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
          permalink="https://www.reddit.com/r/Dankverse/comments/"+submission.id
          print(permalink)
    elif bool(re.search("jpg|jpeg|imgur|i.red|png", url))==True:
        if process_image(url, author) ==True:
          submission=reddit.subreddit('DankVerse').submit_image(title, 'DankVerseimage.jpg')
          permalink="https://www.reddit.com/r/Dankverse/comments/"+submission.id
          print(permalink)
    if submission !=None:
        submission1 = reddit1.submission(submission.id)
        # submission1.mod.approve()
    return submission
  except Exception as e:
    print(e)
    traceback.print_exc()
    logger.exception(e)
    pass

done=['xujhv7', 'xujaq6', 'xuj2un', 'xuhikm', 'xuhibi', 'xugkr5', 'xugkgc', 'xugaff', 'xug046', 'xufjzg', 'xu2ztv', 'xujnno', 'xujifm', 'xujw36', 'xujsqs', 'xujyqi', 'xulamk', 'xulh1j', 'xulkeq', 'xulymc', 'xum24e', 'xumdk6', 'xumpud', 'xun907', 'xun7zv', 'xunrpj', 'xunt5n', 'xuo03b', 'xuo429', 'xuocjl', 'xuomkc', 'xup0m1', 'xup990', 'xupsa3', 'xuprsy', 'xupvqa', 'xuq1pm', 'xuqf3a', 'xuqn3l', 'xur78c', 'xurj82', 'xurx4x', 'xusbn3', 'xusqga', 'xuu257', 'xuvhjz', 'xuyp05', 'xv3qz2', 'xv45bx', 'xv4nb0', 'xv4nbb', 'xv6442', 'xv68qb', 'xv68ee', 'xv6dm6', 'xv6y8z', 'xv7kha', 'xv7zg3', 'xv6utj']
text="Title|Score|Flair|Post url|Reason \n :--|:--|:--|:--|:--\n"
text=""
real_submission = reddit.submission(id="y672p4")
wiki_page=reddit1.subreddit("DankVerse").wiki["removed_memes"]

with open("fetched_data.json", "r") as file:
    fetched_data=json.load(file)

with open("data/real_time_done.json", "r") as file:
    done=json.load(file)

with open("data/Real_Time_Text.txt", "r") as file:
    text=file.read()

downloaded=[]
def main():
    global last_utc, i, fetched_data, done, real_submission, text, downloaded
    i+=1
    current_fetch=[]
    for submission in subreddit.new(limit=200):
        id=submission.id
        created_utc=submission.created_utc
        if id not in current_fetch:
            current_fetch.append(id)
        if {"id": id, "created_utc":created_utc} not in fetched_data:
            fetched_data.append({"id": id, "created_utc":created_utc})
        last_utc=submission.created_utc
    with open("current_fetch.txt", "w+") as file:
        file.write(json.dumps(current_fetch))
    with open("fetched_data.json", "w+") as file:
        file.write(json.dumps(fetched_data))
    lprint(f"i: {str(i)} | last utc:{str(last_utc)} | done: {str(len(done))}")
    # lprint(str(done))
    for item_id in fetched_data :
        if item_id['id'] not in current_fetch and item_id['created_utc'] >= last_utc and item_id['id'] not in done:
            lprint(f"Not found in current_fetch = id: {item_id['id']}  created_utc: {str(item_id['created_utc'])}  last_utc: {str(last_utc)}")
            # if item_id['id'] not in current_fetch and item_id['created_utc'] >= last_utc and item_id['id'] not in downloaded:
            #     downloaded.append(item_id['id'])
            try:
                submission = reddit.submission(id=item_id['id'])
                url=submission.url
                score=submission.score
                removed_by_category=submission.removed_by_category
                is_robot_indexable=submission.is_robot_indexable
                title=submission.title.replace("|","").replace("]","").replace("[","").replace("/","")
                link_flair_text=submission.link_flair_text
                permalink=submission.permalink
                removed_in=int(time.time())-submission.created_utc
                removed_in_minutes=str(removed_in/60)
                h = (removed_in/3600)
                m = (removed_in -(3600*h))/60
                s = (removed_in -(3600*h)-(m*60))
                removed_in_minutes=str(f"{h} hours {m} minutes {s} seconds")
                # lprint(submission.permalink)
                if is_robot_indexable!=True:
                    if submission.link_flair_text==None:
                        link_flair_text="No Flair"
                    link_flair_text=link_flair_text.replace("|","").replace("]","").replace("[","").replace("/","")
                    done.append(item_id['id'])
                    link=None
                    if removed_by_category=='moderator':
                        removal_reason="Removed By Mod"
                        text=f"[{title}](https://www.reddit.com{permalink})|{str(score)}|{link_flair_text}|{removal_reason}\n"+text
                    elif removed_by_category == "deleted":
                        removal_reason="Deleted By User"
                    elif removed_by_category == "reddit":
                        removal_reason="Reddit Spam Filter"
                    else:
                        removal_reason="Other Reason"
                    # text=f"[{title}](https://www.reddit.com{permalink})|{str(score)}|{link_flair_text}|{removal_reason}\n"+text
                    # text=text+f"[{title}](https://www.reddit.com{permalink})|{str(score)}|{link_flair_text}|{removal_reason}\n"
                    # text = text.encode('utf-8','surrogatepass')
                    # text=text.decode('utf-8')
                    # lprint(text)
                    text=text.encode('ascii','backslashreplace').decode('utf-8')
                    
                    if submission.author==None:
                        author="deleted"
                    else:
                        author=str(submission.author)
                    if removed_by_category=='moderator' and score>100:
                        link=DankVerse(title, url, author)
                    if link !=None:
                        try:
                            logger.info("submit id: https://redd.it/" + link.id + "\n\n")
                            print("https://redd.it/" + link.id)
                            try:
                                # link=
                                comment=link.reply(body=f"**MainPostLink**: https://old.reddit.com{submission.permalink}\n\n**Score**: {str(submission.score)}\n\n**Author**: {author}\n\n**Removed In**:{str(removed_in_minutes)} Minutes\n\n\n**For [Removal Of This Post](https://new.reddit.com/message/compose?to=/r/DankVerse&subject=Removal%20Of%20My%20Post&body) Or for [Future exclusion of Your Posts](https://new.reddit.com/message/compose?to=/r/DankVerse&subject=Future%20Exclusion%20Of%20My%20Posts) You can contact Mods**\n\n I am Not a Bot")
                                # comment=link.reply(body="Hi u/  " + author + " Your post https://www.reddit.com" + permalink + " was removed by cuck mods\n\n**So we uploaded your video in r/DankVerse**\n\n\nPost url: https://redd.it/" + link.id + "\n\n Join r/DankVerse\n\n****For [Removal Of This Post](https://new.reddit.com/message/compose?to=/r/DankVerse&subject=Removal%20Of%20My%20Post&body) Or for [Future exclusion of Your Posts](https://new.reddit.com/message/compose?to=/r/DankVerse&subject=Future%20Exclusion%20Of%20My%20Posts) You can contact Mods**\n\n I am Not a Bot")
                                comment = reddit1.comment(comment.id)
                                # comment.mod.approve()
                                # reddit.redditor(author).message(subject="We uploaded your post", message="Hi u/" + author + " Your Post https://www.reddit.com" + permalink + " was removed \n\n**So we uploaded your video in r/DankVerse**\n\n\nPost url: https://redd.it/" + link.id + "\n\n Join r/DankVerse\n\n**For [Removal Of This Post](https://new.reddit.com/message/compose?to=/r/DankVerse&subject=Removal%20Of%20My%20Post&body) Or for [Future exclusion of Your Posts](https://new.reddit.com/message/compose?to=/r/DankVerse&subject=Future%20Exclusion%20Of%20My%20Posts) You can contact Mods**\n\n I am Not a Bot", from_subreddit="DankVerse")
                            except Exception as e:
                                print(e)
                                traceback.print_exc()
                                # comment=link.reply(body="Hi u/" + author + " Your Video was removed by cuck mods So we uploaded your video in R/DankVerse\nPost url: Linking to subreddits or Any post is not allowed\n\n Checkout R/DankVerse\n\n I am Not a Bot")
                                # reddit.redditor(author).message(subject="We uploaded your post", message="Hi u/" + author + " Your Video was removed So we uploaded your video in R/DankVerse\n\nPost url: https://redd.it/" + link.id + "\n Join R/DankVerse\n\n I am Not a Bot", from_subreddit="DankVerse")
                                # comment = reddit1.comment(comment.id)
                                # comment.mod.approve()
                        except Exception as e:
                            traceback.print_exc()
                            logger.exception(e)
                            pass
            except Exception as e:
                traceback.print_exc() 
                logger.exception(e)
                text=text+f"[id:-redd.it/{item_id['id']}|N/A|Removed|Removed By Reddit\n"
    try:
        # lprint(len(text))
        count=text.count('\n')
        main_text=f"count: {str(count)} \n\n\n Post |Score|Flair|Reason \n :--|:--|:--|:--\n"+text
        # if len(text)>=30000:
            # text="Title|Score|Flair|Post url|Reason \n :--|:--|:--|:--|:--\n"+f"[{title}](https://www.reddit.com{permalink})|{str(score)}|{link_flair_text}|{removal_reason}\n"
            # real_submission=reddit.subreddit("DankVerse").submit("Real Time Post Removal Of r/IndianDankmemes & r/DankInIndia", selftext="hi")
        lprint(f"main_text:{str(len(main_text))} | count: {str(count)}")
        # wiki_page.edit(content=main_text)
        # real_submission.edit(body=text)
    except:
        try:
            time.sleep(15)
            wiki_page.edit(content=main_text)
        except Exception as e:
            traceback.print_exc()
            lprint(e)
            lprint("Not edited comment")
            pass
    with open("data/real_time_done.json", "w") as file:
        file.write(json.dumps(done))
    with open("data/Real_Time_Text.txt", "w") as file:
        file.write(text)

main()
schedule.every(2).minutes.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
