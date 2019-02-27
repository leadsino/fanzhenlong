#coding: utf8
import sys
import string
import random
import base64
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from binascii import b2a_hex, a2b_hex
 
class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        #plain_text = cryptor.decrypt(text)
        return plain_text.rstrip('\0')
        #rstrip()去除末尾的补足符
 
if __name__ == '__main__':
    #读取文件
    f1=open('C:\Users\\fandashen\Desktop\\ransom\\attack\\1548138662943_en.NONO','rb')
    all = f1.read()
    t1=all[0:32]
    t2=all[32:204]
    t3=all[204:]
    f1.close()
    #解密对称密钥
    with open('C:\Users\\fandashen\Desktop\\ransom\\attack\master-private.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        Dkey = cipher.decrypt(base64.b64decode(t2),'ERROR')
    #解密文件
    key=prpcrypt(Dkey)
    detxt = key.decrypt(t1)
    #bx=bytes(osv,encoding='utf-8')
    with open('C:\Users\\fandashen\Desktop\\ransom\\attack\\1548138662943.png','wb') as f:
        f.write(detxt+t3)
    #删除加密文件
    if(os.path.exists('C:\Users\\fandashen\Desktop\\ransom\\attack\\1548138662943_en.NONO')):
        os.remove('C:\Users\\fandashen\Desktop\\ransom\\attack\\1548138662943_en.NONO')
    if(os.path.exists('C:\Users\\fandashen\Desktop\\ransom\\attack\\readme.txt')):
        os.remove('C:\Users\\fandashen\Desktop\\ransom\\attack\\readme.txt')
    if(os.path.exists('C:\Users\\fandashen\Desktop\\ransom\\attack\master-public.pem')):
        os.remove('C:\Users\\fandashen\Desktop\\ransom\\attack\master-public.pem')
    if(os.path.exists('C:\Users\\fandashen\Desktop\\ransom\\attack\master-private.pem')):
        os.remove('C:\Users\\fandashen\Desktop\\ransom\\attack\master-private.pem')
    