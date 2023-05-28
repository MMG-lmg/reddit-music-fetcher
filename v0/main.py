import response_processor
import api_getter
import auth
import time
import json
import json_io 
reddit_username = '';
reddit_password = '';

def main():

    post_sets = api_getter.get_multiple_posts(number = 1,subreddit='music',listing='top',limit = 100, timeframe='all')
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
    json_io.store_data(converted_posts,'post_data')
    
    
    authors=set()
    more_comment_limit = 100
    m_comment_bundles=[]
    processed_comments = []
    for post_id in post_ids:
        more_comment_ids = "";
        json = api_getter.get_first_comments('music',post_id)
        for comment in json[1]['data']['children']:
            if comment['kind'] == "t1":
                #this is a real comment
                authors.add(comment['data']['author'])
                processed_comments.append(response_processor.process_comment(comment['data']))
            if comment['kind'] == "more" : 
                for i in range(0,more_comment_limit):
                    more_comment_ids = more_comment_ids + comment['data']['children'][i]+","
        more_comment_ids = more_comment_ids[:-1] #remove the last ','
        m_comment_bundles.append([post_id,more_comment_ids])          
    
    time.sleep(2)
    
    for m_comment_bundle in m_comment_bundles:
        more_comments_json = api_getter.get_more_comments(m_comment_bundle[0],m_comment_bundle[1])
        for more_comment in more_comments_json['json']['data']['things']:
            print(more_comment['kind'])
            if more_comment['kind'] != 'more':
                processed_comments.append(response_processor.process_comment(more_comment['data']))
                authors.add(more_comment['data']['author'])
        
    print(authors)
    json_io.store_data(processed_comments,'comment_data')
    
    user_details=[]
    for author in authors:
        if author == "[deleted]": continue
        time.sleep(1)
        user_json = api_getter.get_user_details(author)
        if 'is_suspended' in user_json['data'].keys():
            user_details.append(response_processor.process_suspended_user(user_json['data']))
        else :
            user_details.append(response_processor.process_user(user_json['data']))
    json_io.store_data(user_details,'user_data')
    
if __name__ == "__main__":
    main()
