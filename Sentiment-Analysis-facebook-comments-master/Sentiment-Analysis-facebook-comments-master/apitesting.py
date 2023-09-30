import requests
import pandas as pd
import json

page_id = '100091750780759'
post_id = '115664504835242'
access_token = 'EAAI386CsZBicBANtKpHpIGDwZC0bvsh3hZAI8P0CrwyToJcf6BneUmY3T6W0gyUTf84qW7sCIWpx6B26Qk9taAqg3LB4w1LDzlXZB7eaYZBroBkrnvHhGz1Fsjt9LhU2oNi6lSmSXxn6phHjSERsrCRAOjbBztKjHmRYLqWYX3OxvX228ZCc0y'

url = f'https://graph.facebook.com/v16.0/{page_id}_{post_id}/comments?access_token={access_token}'

response = requests.request("GET", url)

# save name, time, message in excel file
data = json.loads(response.text)

# create object with only name, time, message
def get_comment(comment):
    return {
        'name': comment.get('from', {}).get('name', ''),
        'time': comment.get('created_time', ''),
        'message': comment.get('message', '')
    }

excel_data = list(map(get_comment, data['data']))
df = pd.DataFrame(excel_data)
df.to_excel('comments.xlsx', index=False)
