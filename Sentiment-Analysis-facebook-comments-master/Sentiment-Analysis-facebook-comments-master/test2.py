import requests
token = "EAAI386CsZBicBANtKpHpIGDwZC0bvsh3hZAI8P0CrwyToJcf6BneUmY3T6W0gyUTf84qW7sCIWpx6B26Qk9taAqg3LB4w1LDzlXZB7eaYZBroBkrnvHhGz1Fsjt9LhU2oNi6lSmSXxn6phHjSERsrCRAOjbBztKjHmRYLqWYX3OxvX228ZCc0y"
post_ids =  115664504835242
page_id = 100091750780759

# Making a GET request
url = (f'https://graph.facebook.com/v16.0/{page_id}_{post_ids}/comments?access_token={token}')

response = requests.request("GET", url)


# check status code for response received
# success code - 200
print(response.status_code)

# print content of request
print(response.text)

