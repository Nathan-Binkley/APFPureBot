import praw
import keys
import time
import praw.exceptions
from apscheduler.schedulers.blocking import BlockingScheduler

reddit = praw.Reddit(client_id=keys.client, 
                    client_secret=keys.secret,
                    user_agent="APFPureBot",
                    username=keys.username,
                    password=keys.password)

reddit.validate_on_submit = True

APF = reddit.subreddit('ActualPublicFreakouts')
PF = reddit.subreddit('PureFreakout')
PFS = reddit.subreddit('PublicFreakout')
def cycle():

    submitted = loadSubmitted()

    # APF stuff
    for sub in APF.top(time_filter='day', limit=10):
        print("Cycling APF")
        if sub.score > 500 and sub.url not in submitted:
            try:
                post(sub.url)
                submitted.append(sub.url)
            except praw.exceptions:
                pass
        
    randomSub = APF.random()
    randomStuff = randomSub.url

    if randomSub.score > 500 and randomSub.url not in submitted:
            post(randomSub.url)
            submitted.append(randomSub.url)


    for sub in PFS.top(time_filter='day',limit=10):
        print("Cycling PF")
        if sub.score > 500 and sub.url not in submitted:
            try:
                post(sub.url)
                submitted.append(sub.url)
            except praw.exceptions:
                pass

    randomSub = PFS.random()
    randomStuff = randomSub.url

    if randomSub.score > 500 and randomSub.url not in submitted:
            post(randomSub.url)
            submitted.append(randomSub.url)

    saveSubmitted(submitted)
    print('-----------------------------------')

def post(url):
    PF.submit("Freakout", url=url)

def loadSubmitted():
    submitted = []
    with open('submitted.txt', 'r') as f:
        line = f.read()
    for i in line.split('\n'):
        submitted.append(i)
    return submitted

def saveSubmitted(li):
    with open('submitted.txt','w') as f:
        f.write("\n".join(li))

scheduler = BlockingScheduler()
scheduler.add_job(cycle,'interval', minutes=30)
scheduler.start()