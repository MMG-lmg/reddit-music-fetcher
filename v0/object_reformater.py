import json_io
import processed_types
from datetime import datetime
post_data = json_io.load_data('post_data')
comment_data = json_io.load_data('comment_data')
user_data = json_io.load_data('user_data')
post_user_data=json_io.load_data('post_author_data')

print('Building dictionary for faster access on comment authors') 
post_user_dict = {} 
for item in post_user_data:
    if item['is_suspended'] != True: 
        item["created_utc"] = datetime.utcfromtimestamp(int(item["created_utc"])).strftime('%Y-%m-%d %H:%M:%S')
    post_user_dict[item["name"]] = item
    
print('Building dictionary for faster access on post authors') 
comment_user_dict = {} 
for item in user_data:
    if item['is_suspended'] != True: 
        item["created_utc"] = datetime.utcfromtimestamp(int(item["created_utc"])).strftime('%Y-%m-%d %H:%M:%S')
    comment_user_dict[item["name"]] = item
    
post_dict = {}  
print('Processing post authors')
print('Building dictionary for faster access on posts')  
for count in range(1,len(post_data)):
    post = post_data[count-1]
    print(f"Processed {count} of {len(post_data)} = {str(round(count/len(post_data)*100,2))}%")
    #process author
    if post["author"] != '[deleted]':
        author = post_user_dict.get(post["author"], False)
        if author != False:
            post["author"] = author
        else: 
            author = processed_types.User()
            author.name = '[deleted]'
            post["author"] = author
    else:
        author = processed_types.User()
        author.name = '[deleted]'
        post["author"] = author
    #build an dictionary for faster access
    post["created_utc"] = datetime.utcfromtimestamp(int(post["created_utc"])).strftime('%Y-%m-%d %H:%M:%S')
    post_dict[post['id']] = post
    post_dict[post['id']]['comments'] = []
      
print('Processing comment authors and appending post comments')    
for count in range(1,len(comment_data)):
    print(f"Processed {count} of {len(comment_data)} = {str(round(count/len(comment_data)*100,2))}%")
    comment = comment_data[count-1]
    #process author
    if comment["author"] != '[deleted]':
        author = post_user_dict.get(comment["author"], False)
        if author != False:
            comment["author"] = author
        else: 
            author = processed_types.User()
            author.name = '[deleted]'
            comment["author"] = author
    else:
        author = processed_types.User()
        author.name = '[deleted]'
        post["author"] = author
    #add to dictionary
    comment["created_utc"] = datetime.utcfromtimestamp(int(comment["created_utc"])).strftime('%Y-%m-%d %H:%M:%S')
    post_id = comment['parent_id'].split('_')[1] #post_id
    post_dict[post_id]['comments'].append(comment)

json_ready_list = []
json_ready_list.extend(post_dict.values())
json_io.store_data(json_ready_list,'reformated_posts')
