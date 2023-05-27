import api_getter
import auth
import time
reddit_username = '';
reddit_password = '';

def main():

    post_set = api_getter.get_posts('music','top',1,'top')
    print(post_set)
    post_id = ''
    for post in post_set['data']['children']:
        print(post['data']['title'] + ' - ' + post['data']['id'])
        post_id = post['data']['id']
    time.sleep(2)
    
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
    

if __name__ == "__main__":
    main()
