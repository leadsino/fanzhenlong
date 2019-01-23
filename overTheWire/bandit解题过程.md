题目地址：http://overthewire.org/wargames/

#### level0-level1

已知HOST：bandit.labs.overthewire.org  PORT：2220  账号：bandit0 密码bandit0

通过提示查看home下的readme文件，获取bandit1的密码

![1547707654828](assets/1547707654828.png)

#### level1-level2

登录bandit1，发现目录下的-文件，直接cat并不能查看

![1547707768634](assets/1547707768634.png)

查看cat --help发现，直接cat会变为标准输入

![1547707822090](assets/1547707822090.png)

通过当前目录来加上当前目录来绕过cat ./-

![1547707897783](assets/1547707897783.png)

#### level2-level3

登录bandit2

查看存在spaces in this filename文件

通过cat 输入部分然后tab补全，会发现空格前面存在转义符号\

![1547708291626](assets/1547708291626.png)

#### level3-leve4

登录bandit3

根据提示，文件放置在inhere文件夹内，cd进入文件夹，ls没有发现存在文件，通过ls -a查看发现有隐藏文件.hidden，cat获得密码

![1547708586255](assets/1547708586255.png)

#### level4-level5

登录bandit4

查看inhere目录有多个文件

通过

```
file ./*
```

查看文件所有文件类型，找到-file07为密码

#### level5-level6

登录bandit5

查看发现有大量目录及文件，根据提示，文件大小为1033bytes

通过

```
find ./ -size 1033c
```

![1547710497430](assets/1547710497430.png)

拓展

![1547710880581](assets/1547710880581.png)

#### level6-level7

登录bandit6

通过

```
find / -user bandit7 -group bandit6 -size 33c
```

#### level7-level8

登录bandit7

查找指定内容的行

```
cat data.txt |grep 'millionth'
```

#### level8-level9

对内容进行排序

```
cat data.txt |sort
sort data.txt | uniq -u
```

#### level9-level10

文件是二进制文件，strings打印内容中可打印的字符

```
strings data.txt | grep '='
```

#### level10-level11

直接base64解密

```
cat ./data.txt | base64 -d
```

#### level11-level12

凯撒加密，字母偏移量

5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu

#### level12-level13

首先文件是16进制的，使用xxd -r将文件转换为二进制，通过file确定文件为gzip，可以通过更改文件后缀，或者直接使用zcat重定向解压得到内部文件，然后中间有tar与bzip的解压，最终获得ascii的密码文件

> xxd -r 转换二进制
>
> file确定解压后的文件类型

#### level13-level14

通过密钥登录

```
ssh -i sshkey.private bandit14@localhost
```

登录成功此时用户为bandit14

```
cat /etc/bandit_pass/bandit14
```

4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e

#### level14-level15

利用nc工具和本地端口建立tcp连接

```
nc localhost 30000
```

输入bandit14的密码后，返回密码

BfMYroe26WYalil77FoDi9qh59eK5xNr

level15-level16

通过openssl s_client

```
openssl s_client -connect localhost:30001 -quiet
```

-quiet：用以关闭session和证书的信息，同时打开-ign_eof这个选项。前者可简化显示的界面，后者则保证在输入完成后不是立即断开连接，否则无法看到回显的下一个等级的密码。

cluFn7wTiGryunymYOu4RcffSxQluehd

#### level16-level17

通过nmap扫描本地端口

```
nmap -p31000-32000 localhost
```

再通过openssl监听端，其中一个获得密钥

-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----

#### level17-level18

通过grep比较找出不同的行

```
grep -vFf password.old password.new
或者 diff password.old password.new
```

注：new文件放后面，不用弄反

kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd

#### level18-level19

登录发现直接登出，返回byebye

尝试直接ssh带命令登录

```
ssh -p 2220 bandit18@bandit.labs.overthewire.org cat ./readme
或者
scp bandit18@bandit.labs.overthewire.org:.~/readme ./readme
```

IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x

#### level19-level20

通过直接执行该文件，提示用法，能够用另一个用户权限执行某个命令

![1547781705401](assets/1547781705401.png)

然后再查看文件权限，所属者bandit20具有s权限，组bandit19具有执行权限，即文件执行具有20的权限，那我们就可以根据提示去查看20的密码文件

![1547781808949](assets/1547781808949.png)

```
./bandit20-do cat /etc/bandit_pass/bandit20
```

GbKksEFF4yrVs6il55v6gwY5aVje5f0j

#### level20-level21