import facebook
import json
token = "EAAI386CsZBicBANtKpHpIGDwZC0bvsh3hZAI8P0CrwyToJcf6BneUmY3T6W0gyUTf84qW7sCIWpx6B26Qk9taAqg3LB4w1LDzlXZB7eaYZBroBkrnvHhGz1Fsjt9LhU2oNi6lSmSXxn6phHjSERsrCRAOjbBztKjHmRYLqWYX3OxvX228ZCc0y"

graph = facebook.GraphAPI(token)




# Define a list of post IDs to retrieve information for
post_ids = [115664504835242]

# Define the fields to retrieve for each post
fields = 'id,message,created_time'

# Create a list of dictionaries containing the request parameters for each post
requests = [{'method': 'GET', 'relative_url': f'{post_id}?fields={fields}'} for post_id in post_ids]

# Create the batch request parameters dictionary
batch_params = {'batch': json.dumps(requests), 'include_headers': False}

# Send the batch request and retrieve the responses
responses = graph.request('', method='GET', args=batch_params)

# Process the responses as needed
for response in responses:
    response_json = json.loads(response['body'])
    post_id = response_json['id']
    message = response_json.get('message', '')
    created_time = response_json.get('created_time', '')
    print(f'Post ID: {post_id}, Message: {message}, Created Time: {created_time}')








