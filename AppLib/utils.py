'''
    工具类函数库

'''
import base64
import logging
import datetime,time
from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from sqlalchemy import create_engine

class DataConversion:
    ''' 提供数据转换的类 '''
    def __init__(self) : ...

    def Base64Code(self,value, types='encode', tostring=True):
        ''' Base64转换。

            将字符串转换为 Base64编码，或将 Base64 字节转换为字符串。
        
        '''
        re = None
        if types == 'encode': 
            ss = bytes(value, 'utf-8')
            encodestr = base64.b64encode(ss)
            re = str(encodestr, 'utf-8')
        if types == 'decode': 
            re = base64.b64decode(value)
            re = str(re,'utf-8')
        return re

    def ForeachKV(self,j:dict): 
        ''' 遍历 Json 对象的所有键值。 

            将所有键值转换为一个数组序列
        
            Args:
                j:  {"k":v,"k2":{"k2k":vv}}

            Returns: 
                [k,v,k2k,vv]
        '''
        re = []
        for i in j:
            if type(j[i]) == str or type(j[i]) == int:
                re.append(i)
                re.append(j[i])
            if type(j[i]) == dict:
                re.append(i)
                for ii in self.ForeachKV(j[i]):
                    re.append(ii)
            if type(j[i]) == list:
                re.append(i)
                re.append(str(j[i]))
        return re

    def UnixTimeToStr(self, t=time.time(), strftime="%Y-%m-%d %T"):
        ''' 时间戳转换为字符串日期格式 
        
            Args:
                t:          时间戳
                strftime:   转换占位符

            Return:
                日期字符串  'yyyy-mm-dd hh:mm:ss'
        '''
        return datetime.datetime.utcfromtimestamp(t).strftime(strftime)
    
    pass



class Security: 
    ''' 处理安全相关的工具库 '''
 
    class AEScoder():
        ''' 字符加密 '''
        def __init__(self, key) -> None:
            ''' 密钥 '''
            self.key = key
            pass
        
        def encrypt(self, message , password):
            ''' 加密 '''
            plain_text = message
            # generate a random salt
            salt = get_random_bytes(AES.block_size)
            # use the Scrypt KDF to get a private key from the password
            private_key = hashlib.scrypt(
                password.encode(),
                salt=salt,
                n=2 ** 14,
                r=8,
                p=1,
                dklen=32,
                )
            # create cipher config
            cipher_config = AES.new(private_key, AES.MODE_GCM)
            # return a dictionary with the encrypted text
            (cipher_text, tag) = \
                cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
            encryptedDict = {
                'cipher_text': b64encode(cipher_text).decode('utf-8'),
                'salt': b64encode(salt).decode('utf-8'),
                'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
                'tag': b64encode(tag).decode('utf-8'),
                }
            encryptedString = encryptedDict['cipher_text'] + '*' \
                + encryptedDict['salt'] + '*' + encryptedDict['nonce'] + '*' \
                + encryptedDict['tag']
            return encryptedString
        

        def decrypt(self, enc_dict, password):
            ''' 解密 '''
            enc_dict = enc_dict.split('*')
            try:
                enc_dict = {
                    'cipher_text': enc_dict[0],
                    'salt': enc_dict[1],
                    'nonce': enc_dict[2],
                    'tag': enc_dict[3],
                    }
                # decode the dictionary entries from base64
                salt = b64decode(enc_dict['salt'])
                cipher_text = b64decode(enc_dict['cipher_text'])
                nonce = b64decode(enc_dict['nonce'])
                tag = b64decode(enc_dict['tag'])
                # generate the private key from the password and salt
                private_key = hashlib.scrypt(
                    password.encode(),
                    salt=salt,
                    n=2 ** 14,
                    r=8,
                    p=1,
                    dklen=32,
                    )
                # create the cipher config
                cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
                # decrypt the cipher text
                decrypted = cipher.decrypt_and_verify(cipher_text, tag)
            except:
                return False

            return decrypted.decode('UTF-8')


class DB: 
    ''' 数据库相关的工具库 '''
    def SqlalchemyQueryResultToDict(self, row):
        ''' 转换 Sqlalchemy 查询结果为 Dict 类型 '''
        redata = []
        for i in row:
            t = i.__dict__.copy()
            t.pop('_sa_instance_state')
            redata.append(t)
        return redata

    def CheckMysql(self,url): 
        '''
        检查数据库可用性。 
        '''  
        try:
             
            engine = create_engine(url)
            conn = engine.connect()
            logging.info('Check Mysql Connect: Success')
            for i in conn.execute('show global status;').fetchall(): 
                if i[0] in [
                    'Memory_used', 'Open_files', 'Open_tables', 
                    'Qcache_total_blocks', 'Uptime', 
                    'Threads_running', 'Innodb_page_size']:
                    logging.info('Mysql Status: ' + str(i))
            conn.close()
        except Exception as e: 
            logging.error('检查数据库连接时发生错误: ' + str(e))
    
    
    
    pass













