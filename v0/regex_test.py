import re
import json
pattern = r"^([^-/]+)\s*-\s*([^-/]+)\s*\[\s*([^-/]+(?:\s*/\s*[^-/]+)*)\]\s*(.*)$"

with open("post_data.json", "r") as content:
  json_data = json.load(content)

for post in json_data:
    if '[' in post['title']: print(post['title'])
    match = re.match(pattern, post['title'])

    if match:
        first_string = match.group(1)
        second_string = match.group(2)
        middle_strings = match.group(3).split('/')
        remaining_text = match.group(4)

        print("First String:", first_string)
        print("Second String:", second_string)
        print("Middle Strings:", middle_strings)
        print("Remaining Text:", remaining_text)