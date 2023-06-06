import json_io
import time
import api_getter
import response_processor
post_data = json_io.load_data('post_data')

authors = set()
for post in post_data:
    authors.add(post["author"])

print(authors)   
    
start_time = time.perf_counter()
count = 0;
error_counter = 0;
user_details=[]
for author in authors:
    if author == "[deleted]": continue
    time.sleep(1)
    user_json = api_getter.get_user_details(author)
    while user_json is None: 
        time.sleep(10) 
        print('Waiting 10 and retrying')
        if error_counter > 5 : 
            print("5 consequent parse errors with waits skipping")
            break;
        user_json = api_getter.get_user_details(author)
        error_counter = error_counter + 1;
    error_counter = 0;
    if user_json is not None:   
        print(f"fetched {count} of {len(authors)} = {str(round(count/len(authors)*100,2))}%")
        if 'data' in user_json.keys():
            if user_json['data'] is not None:
                if 'is_suspended' in user_json['data'].keys():
                    user_details.append(response_processor.process_suspended_user(user_json['data']))
                else :
                    user_details.append(response_processor.process_user(user_json['data']))
    count = count + 1 
json_io.store_data(user_details,'post_author_data')
end_time = time.perf_counter()
print('Users fetching: time elapsed: ' + str(end_time-start_time) +"sec")
print(f"Fetched {len(authors)} users")