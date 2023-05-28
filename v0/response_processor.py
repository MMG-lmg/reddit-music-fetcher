import processed_types as types
import re
def prepare_more_comments(comments_data,more_comment_limit):
    for comment in comments_data[1]['data']['children']:
        if comment['kind'] == "more" : 
           for i in range(0,more_comment_limit):
               more_comment_ids = more_comment_ids + comment['data']['children'][i]+","
    more_comment_ids = more_comment_ids[:-1] #remove the last ','
    return more_comment_ids

def process_post(post_data):
    post = types.Post()
    #post[data]
    post.title = post_data['title']
    if(post_data['link_flair_richtext'] != []) : 
        post.flair = post_data['link_flair_richtext'][0]['t']
    else:
        post.flair = 'none'
    post.subreddit = post_data['subreddit']
    post.downvotes = post_data['downs']
    post.upvotes = post_data['ups']
    post.id = post_data['id']
    post.total_awards = post_data['total_awards_received']
    post.is_original_content = post_data['is_original_content']
    post.score = post_data['score']
    post.created_utc = post_data['created_utc']
    for award_data in post_data['all_awardings']:
        award = types.Award()
        award.name = award_data['name']
        award.coin_price = award_data['coin_price']
        award.days_of_premium = award_data['days_of_premium']
        award.description = award_data['description']
        award.count = award_data['count']
        post.awards.append(award)
    post.author = post_data['author']
    post.num_comments = post_data['num_comments']
    post.url = "https://www.reddit.com" + post_data['permalink']
    post.num_crossposts = post_data['num_crossposts']
    post.is_music_post, artist_h,song_h, genres_h=process_music_title(post.title)
    if post.is_music_post:
       post.artist = artist_h
       post.song_title = song_h
       post.genre = genres_h
       post.media_url = post_data['url']
    return post

def process_music_title(title):
    title = title.replace(',', '/')
    pattern = r"^([^-/]+)\s*-\s*([^-/]+)\s*\[\s*([^-/]+(?:\s*/\s*[^-/]+)*)\]\s*(.*)$"
    match = re.match(pattern, title)
    if match:
        artist = match.group(1)
        song_title = match.group(2)
        genres = match.group(3).split('/')
        return True,artist,song_title,genres
    return False,'','',[]
    
def process_comment(comment_data):
    comment = types.Comment()
    comment.subreddit = comment_data['subreddit']
    comment.author = comment_data['author']
    comment.created_utc = comment_data['created_utc']
    comment.total_awards = comment_data['total_awards_received']
    for award_data in comment_data['all_awardings']:
        award = types.Award()
        award.name = award_data['name']
        award.coin_price = award_data['coin_price']
        award.days_of_premium = award_data['days_of_premium']
        award.description = award_data['description']
        award.count = award_data['count']
        comment.awards.append(award)
    comment.downvotes = comment_data['downs']
    comment.upvotes = comment_data['ups']
    comment.parent_id = comment_data['link_id']
    comment.body = comment_data['body']
    comment.upvote_ratio = comment_data['upvote_ratio']
    comment.url = "https://www.reddit.com" + comment_data['permalink']
    comment.score = comment_data['score']
    return comment;
    
def process_user(user_data):
    user = types.User()
    #user[data]
    user.id = user_data['id']
    user.verified = user_data['verified']
    user.mod = user_data['is_mod']
    user.gold = user_data['is_gold']
    user.awarder_karma =user_data['awarder_karma'] 
    user.total_karma = user_data['total_karma'] 
    user.link_karma = user_data['link_karma']
    user.name = user_data['name']
    user.created_utc = user_data['created_utc']
    user.comment_karma = user_data['comment_karma']
    return user
    
def prepare_user_ids(comments):
    user_ids=[]
    for comment in comments:
        if comment['kind'] == "t1":
            user_ids.append(comment['data']['author'])
    return user_ids