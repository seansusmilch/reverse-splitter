from pocketbase import PocketBase
import os

client = PocketBase(os.environ.get('PB_URL'))
server_user = client.collection('users').auth_with_password(os.environ.get('PB_USER'), os.environ.get('PB_PASS'))

def get_pb():
    if not server_user.is_valid:
        client.collection('users').auth_with_password(os.environ.get('PB_USER'), os.environ.get('PB_PASS'))
    return client


if __name__ == '__main__':
    print(vars(get_pb().collection('newsletters').get_full_list()[0]))