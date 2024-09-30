from pocketbase import PocketBase
import os

def auth_pb():
    client = PocketBase(os.environ.get('PB_URL'))
    user = client.collection('users').auth_with_password(os.environ.get('PB_USER'), os.environ.get('PB_PASS'))
    return client, user.record

def get_pb():
    return auth_pb()[0]

def get_user():
    return auth_pb()[1]

if __name__ == '__main__':
    print(vars(get_user()))