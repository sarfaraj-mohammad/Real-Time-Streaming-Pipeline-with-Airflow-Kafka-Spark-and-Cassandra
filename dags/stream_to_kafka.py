import requests
import json
import time

from kafka import KafkaProducer


def generate_random_user(url = 'https://randomuser.me/api/?results=1'):
    response = requests.get(url)
    user_details = response.json()
    user = user_details['results'][0]
    # print(*user.items(), sep='\n')

    return user


def filter_user_details(user):
    data = {}

    data['full_name'] = f"{user['name']['title']}. {user['name']['first']} {user['name']['last']}"
    data['gender'] = user['gender']
    data['street_address'] = f"{user['location']['street']['number'], user['location']['street']['name']}"
    data['city'] = user['location']['city']
    data['state'] = user['location']['state']
    data['country'] = user['location']['country']
    data['postcode'] = user['location']['postcode']
    data['email'] = user['email']
    data['username'] = user['login']['username']
    data['password'] = user['login']['password']
    data['dob'] = user['dob']['date']
    data['age'] = user['dob']['age']
    data['cell'] = user['cell']

    return data


def start_streaming():
    producer = KafkaProducer(bootstrap_servers=['kafka1:19092', 'kafka2:19093', 'kafka3:19094'])

    end_time = time.time() + 20

    while time.time() < end_time:
        results = generate_random_user()
        data = filter_user_details(results)
        producer.send('random_users', json.dumps(data).encode('utf-8'))
        
        time.sleep(10)
    


if __name__ == '__main__':
    start_streaming()