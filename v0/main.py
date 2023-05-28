import response_processor
import api_getter
import auth
import time
import json
import json_io 
reddit_username = '';
reddit_password = '';

def main():

    post_sets = api_getter.get_multiple_posts(number = 25,subreddit='music',listing='top',limit = 100, timeframe='all')
    print(type(post_sets))
    
    post_ids = []
    converted_posts=[]
    start_time = time.perf_counter()
    for post_set in post_sets:
        for post in post_set['data']['children']:
            post_ids.append(post['data']['id'])
            converted_posts.append(response_processor.process_post(post['data']))
    print(len(post_ids))
    json_io.store_data(converted_posts,'post_data')
    end_time = time.perf_counter()
    print('Post fetching: time elapsed: ' + str(end_time-start_time) +"sec");
    
    authors=set()
    more_comment_limit = 10
    m_comment_bundles=[]
    processed_comments = []
    start_time = time.perf_counter()
    count = 1;
    for post_id in post_ids:
        print(f"fetched {count} of {len(post_ids)} = {str(round(count/len(post_ids)*100,2))}%")
        more_comment_ids = "";
        json = api_getter.get_first_comments('music',post_id)
        for comment in json[1]['data']['children']:
            if comment['kind'] == "t1":
                #this is a real comment
                authors.add(comment['data']['author'])
                processed_comments.append(response_processor.process_comment(comment['data']))
            if comment['kind'] == "more" : 
                if len(comment['data']['children']) < more_comment_limit : range_upper = len(comment['data']['children'])
                else: range_upper = more_comment_limit
                for i in range(0,range_upper):
                    more_comment_ids = more_comment_ids + comment['data']['children'][i]+","
        more_comment_ids = more_comment_ids[:-1] #remove the last ','
        m_comment_bundles.append([post_id,more_comment_ids])         
        count = count+1 
    
    end_time = time.perf_counter()
    print('First comment fetching: time elapsed: ' + str(end_time-start_time) +"sec");
    
    time.sleep(2)
    start_time = time.perf_counter()
    count = 1
    for m_comment_bundle in m_comment_bundles:
        print(f"fetched {count} of {len(m_comment_bundles)} = {str(round(count/len(m_comment_bundles)*100,2))}%")
        if m_comment_bundle[1] == [] : continue
        more_comments_json = api_getter.get_more_comments(m_comment_bundle[0],m_comment_bundle[1])
        if not 'data' in more_comments_json['json'].keys() or not 'things' in more_comments_json['json']['data'].keys(): continue
        for more_comment in more_comments_json['json']['data']['things']:
            if more_comment['kind'] != 'more':
                processed_comments.append(response_processor.process_comment(more_comment['data']))
                authors.add(more_comment['data']['author'])
        count = count + 1 
     
    end_time = time.perf_counter()
    print('More comments fetching: time elapsed: ' + str(end_time-start_time) +"sec");   
    print(f"Fetched {len(processed_comments)} comments");
    #print(authors)
    
    json_io.store_data(processed_comments,'comment_data')
    
    user_details=[]
    count=1;
    for author in authors:
        if author == "[deleted]": continue
        #time.sleep(1)
        user_json = api_getter.get_user_details(author)
        print(f"fetched {count} of {len(authors)} = {str(round(count/len(authors)*100,2))}%")
        if 'is_suspended' in user_json['data'].keys():
            user_details.append(response_processor.process_suspended_user(user_json['data']))
        else :
            user_details.append(response_processor.process_user(user_json['data']))
        count = count + 1 
    json_io.store_data(user_details,'user_data')
    
if __name__ == "__main__":
    main()
