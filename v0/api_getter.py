import requests
import json
import praw
subreddit = 'music'
limit = 100
timeframe = 'all' #hour, day, week, month, year, all
listing = 'top' # controversial, best, hot, new, random, rising, top

def get_posts(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'r/music-fetcher by u/ludikonj35'})
    except:
        print('An Error Occured')
    return request.json()

def get_sequential_posts(subreddit,listing,limit,timeframe,after,count):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}&after={after}&count={count}'
        request = requests.get(base_url, headers = {'User-agent': 'r/music-fetcher by u/ludikonj35'})
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

def get_first_comments(subreddit,post_id):
    print(f'Fetching first comments from r/{subreddit} for post {post_id}')
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/comments/{post_id}.json'
        request = requests.get(base_url, headers = {'User-agent': 'r/music-fetcher by u/ludikonj35'})
    except:
        print("Error occured")
    return request.json()

def get_more_comments(post_id,more_ids,only_requested='true'):
    print(f'Fetching more comments from for post {post_id}')
    #more_ids => comma separated list of links
    fullname = 't3_'+post_id
    try:
        base_url = f'https://api.reddit.com/api/morechildren?api_type=json&showmore=true&link_id={fullname}&children={more_ids}&limit_children={only_requested}'
        print(base_url)
        request = requests.post(base_url, headers = {'User-agent': 'r/music-fetcher by u/ludikonj35'})
    except:
        print("Error occured")
    return request.json()

def get_comments_auth(post_id,sort,auth_token,limit=100,threaded = 'false'):
    try:
        base_url = f'http://oauth.reddit.com/comments/{post_id}?sort={sort}&threded={threaded}'
        print(base_url)
        request = requests.get(base_url, headers={'Authorization': 'Bearer {access_token}'})
    except Exception as e:
        print(e)
        print('An Error Occured')
    return request.text

def get_comments_praw(post_id,client_id,client_secret):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="r/music-fetcher by u/ludikonj35",
    )
    print("created instance, fetching post")
    submission = reddit.submission(post_id)
    print("fetched posts, fetching comments")
    print(submission.title)
    submission.comments.replace_more(limit=25)
    for top_level_comment in submission.comments:
        type(top_level_comment)
        print(top_level_comment)
      
def get_user_details(username):
    print(f'Fetching details from for user {username}')
    try:
        base_url = f'https://www.reddit.com/user/{username}/about.json'
        request = request = requests.get(base_url, headers = {'User-agent': 'r/music-fetcher by u/ludikonj35'})
    except Exception as e:
        print(e)
        print('An Error Occured')
    return request.json()
"""   
r = get_multiple_posts(1940,subreddit,listing,limit,timeframe)
counter = 0
for post_set in r:
    for post in post_set['data']['children']:
        print(post['data']['title'])
        counter = counter + 1
        
print(f'Fetched {counter} posts')
"""
