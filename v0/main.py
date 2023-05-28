import response_processor
import api_getter
import auth
import time
import json
import json_io 
reddit_username = '';
reddit_password = '';

def main():

    post_sets = api_getter.get_multiple_posts(number = 350,subreddit='music',listing='top',limit = 100, timeframe='all')
    print(type(post_sets))
    
    post_ids = []
    converted_posts=[]
    for post_set in post_sets:
        for post in post_set['data']['children']:
            print(post['data']['title'] + ' - ' + post['data']['id'])
            post_ids.append(post['data']['id'])
            converted_posts.append(response_processor.process_post(post['data']))
    print(post_ids)
    print(len(post_ids))
    #time.sleep(2)
    
    json_io.store_data(converted_posts)
    
    """
    for post_set in post_sets:
        for post in post_set:
    """
    """
    more_comment_limit = 100
    more_comment_ids = "";
    json = api_getter.get_first_comments('music',post_id)
    for comment in json[1]['data']['children']:
        if comment['kind'] == "t1":
            #this is a real comment
            print(comment['data']['body'])
        if comment['kind'] == "more" : 
           for i in range(0,more_comment_limit):
               more_comment_ids = more_comment_ids + comment['data']['children'][i]+","
    more_comment_ids = more_comment_ids[:-1] #remove the last ','
    print(more_comment_ids)           
    
    time.sleep(2)
    more_comments_json = api_getter.get_more_comments(post_id,more_comment_ids)
    print(more_comments_json) 
    """

if __name__ == "__main__":
    main()
