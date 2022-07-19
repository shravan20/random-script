import json
import sys
import random
import requests
import json
from datetime import date, datetime

with open('credentials.json', 'r') as f:
  credentials = json.load(f)

employees_url = credentials['employees_url']
slack_hook_url = credentials['slack_hook_url']
employee_data = []


def get_employee_list():
    bamboohr_headers = {'Accept':'application/json', 'Content-Type':'application/json'}
    url = employees_url
    response = requests.get(url, headers=bamboohr_headers)
    return response.json()
    
def customizer():
    #Getting random bot name
    with open('bot_name.txt', 'r') as f:
         name_data = f.read()
    name_data = name_data.split("\n")
    bot_name = random.choice(name_data)

    #Getting random slack emoji
    with open('emoji_id.txt', 'r') as f:
         emoji_data = f.read()
    emoji_data = emoji_data.split("\n")
    emoji_id = random.choice(emoji_data)

    #Generating random hex color code
    hex_number = random.randint(1118481, 16777215)
    hex_number = str(hex(hex_number))
    hex_number = '#' + hex_number[2:]

    return bot_name, emoji_id, hex_number

def wish_happy_birthday(slack_hook_url, customizer, name, wishes):
    url = slack_hook_url
    bot_name, emoji_id, hex_number = customizer()
    title = (f"Birthday Wishes {emoji_id}")
    
    message = random.choice(wishes['bday']['message'])
    emoji = random.choice(wishes['bday']['emoji'])
    wish = message + " " + name + " " + emoji
    
    '''
    Data Preparation for creating custom wishes
    '''
    slack_data = create_wish(wish)
    
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    else:
        print("Birthday wishes successfully!!!")

def create_wish(wish):
    return {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": wish
			}
		},
		{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": "Bday Image"
			},
			"image_url": "https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5ehu8kafdo3g0313ul03.jpeg",
			"alt_text": "Birthday Wishes"
		}
	]
    }

if __name__ == '__main__':
    
    data = get_employee_list()

    wishes = {
        'bday' : {
            'title' : 'Birthday Wishes',
            'emoji' : [':blossom:', ':boom:', ':cake:', ':candy:'],
            'message': [
                'Happy Birthday',
                'Many Many Happy Return of the Day',
                'Here’s to a fabulous birthday! May it be filled with love, laughter, and joy.'
                'Wishing you everything that brings joy in life. Happy Birthday.'
            ]
        }
    }
    
    
    
    '''
    Business Logic
    '''
    today = date.today()
    # Fetch month
    formatted_date = today.strftime("%m-%d")
    formatted_date = "07-13"
    employee_to_be_wished = list()
    
    for emp in data['employees']:
        try:
            empDob = datetime.strptime(emp['dateOfBirth'], "%Y-%m-%d").strftime("%m-%d")
            if(formatted_date == empDob):
                employee_to_be_wished.append(emp['fullName2'])
        except ValueError as e:
            pass
 
    print("Employees who are celebrating bday = " , len(employee_to_be_wished))
    for name in employee_to_be_wished:
        name = name.split(",")
        name = name [1] + " "+ name[0]
        wish_happy_birthday(slack_hook_url, customizer, name, wishes)
