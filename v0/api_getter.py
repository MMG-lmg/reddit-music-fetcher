import requests
import json
subreddit = 'music'
limit = 100
timeframe = 'all' #hour, day, week, month, year, all
listing = 'top' # controversial, best, hot, new, random, rising, top

def get_posts(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()

def get_sequential_posts(subreddit,listing,limit,timeframe,after,count):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}&after={after}&count={count}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()

def get_multiple_posts(number,subreddit,listing,limit,timeframe):
    print(f'Fetching {number} posts from r/{subreddit}')
    posts =[]
    if number < 100:
        posts.append(get_posts(subreddit,listing,number,timeframe))
        return posts;
    posts.append(get_posts(subreddit,listing,limit,timeframe))
    count=100
    for i in range (1,number//100):
        posts.append(get_sequential_posts(subreddit,listing,limit,timeframe,posts[-1]['data']['after'],count))
        print('Progress: '+ str(round(count/number*100)) +'%');
        count = count + 100
    if number - count > 0:
        posts.append(get_sequential_posts(subreddit,listing,(number - count),timeframe,posts[-1]['data']['after'],count))   
    print('Progress: 100%');
    return posts

r = get_multiple_posts(780,subreddit,listing,limit,timeframe)

counter = 0
for post_set in r:
    for post in post_set['data']['children']:
        print(post['data']['title'])
        counter = counter + 1
        
print(f'Fetched {counter} posts')
        