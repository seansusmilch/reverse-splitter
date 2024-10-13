from pocketbase import PocketBase
import os
import reverse_splitter.bin.logger as logger
import cachetools.func

log = logger.setup_logger('DB')

@cachetools.func.ttl_cache(maxsize=1, ttl=1209600)
def auth_pb():
    log.info('Authenticating PocketBase')
    client = PocketBase(os.environ.get('PB_URL'))
    user = client.collection('users').auth_with_password(os.environ.get('PB_USER'), os.environ.get('PB_PASS'))
    return client, user.record

def get_pb():
    return auth_pb()[0]

def get_user():
    return auth_pb()[1]

if __name__ == '__main__':
    print(vars(get_user()))
    print(vars(get_user()))
    print(vars(get_user()))
    print(vars(get_user()))