
import json

with open('./searchapp/repository/data/users.json') as f:
    users = json.load(f)

new_users = users
for i in range(1, 1000):
    temp = [{**user, "_id": 75 + (75*i) + j + 1} for j, user in enumerate(users)]
    new_users = [*new_users, *temp]
    
with open('./new_users.json', 'w') as f:
    json.dump(new_users, f)
