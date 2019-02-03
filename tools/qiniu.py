from qiniu import Auth, put_file
from wechat.settings import qiniu_access_key, qiniu_secret_key
import random
import time

random_str = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'


class CloudPic:
    def __init__(self):
        self._time = time.strftime('%Y%m%d')
        self._bucket_name = 'pfish'

    def get_key(self, file_name=None):
        if file_name:
            pic_name = file_name.spilt('.')[1]
            random_s = random.sample(random_str, 12)
        else:
            e = 'file name is None!'
            raise Exception(e)
        return 'weixin/{}/{}.{}'.format(self._time, random_s, pic_name)

    def upload_to_qiniu(self, file_name):
        q = Auth(access_key=qiniu_access_key, secret_key=qiniu_secret_key)
        key = self.get_key(file_name)
        token = q.upload_token(self._bucket_name, key, 3600)
        localfile = '../templates/test.png'
        ret, info = put_file(token, key, localfile)


