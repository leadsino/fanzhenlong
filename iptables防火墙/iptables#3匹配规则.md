### 基本匹配条件

**-s**：匹配报文的源地址，可以同时指定多个源地址，每个IP之间用逗号隔开，也可以指定为网段

```
iptables -I INPUT -s 192.168.1.1,192.168.1.2 -j DROP
iptables -I INPUT -s 192.168.1.0/24 -j ACCEPT
iptables -I INPUT ! -s 192.168.1.0/24 -j ACCEPT
```

##### 可以使用！取非

**-d**：匹配报文的目标地址，和-s一样，可以同时指定多个目标地址，每个IP之间用逗号隔开，也可以指定为网段

```
iptables -I INPUT -d 192.168.1.1,192.168.1.2 -j DROP
iptables -I INPUt -d 192.168.1.0/24 -j ACCEPT
```

**-p**：匹配报文的协议类型，可以匹配tcp、udp、udplite、icmp、esp、ah、sctp等（centos7还支持icmpv6、mh）

```
iptables -I INPUT -p tcp -s 192.168.1.1 -j ACCEPT
iptables -I INPUT ！ -p udp -s 192.168.1.2 -j DROP
```

**-i**：用于匹配报文从哪个网卡流入，由于匹配报文流入的网卡，所以在OUTPUT链与POSTROUTING链中不能使用

```objective-c
iptables -I INPUT -i eth0 -j DROP
```

**-o**：用于匹配报文从哪个网卡流出，由于匹配报文流出的网卡，所以在INPUT链与PREROUTING链中不能使用

```
iptables -I OUTPUT -p icmp -o eth1 -j DROP
```

### 拓展匹配条件

#### tcp拓展模块

**-p tcp -m tcp --sport**：用于匹配tcp协议报文的源端口，使用冒号指定连续的端口范围

**-p tcp -m tcp --dport**：用于匹配tcp协议报文的目标端口，使用冒号指定连续的端口范围

```
iptables -t filter -I OUTPUT -d 192.168.1.2 -p tcp -m tcp --sport 23 -j REJECT
iptables -t filter -I OUTPUT -d 192.168.1.2 -p tcp --sport 23 -j REJECT
iptables -t filter -I OUTPUT -d 192.168.1.2 -p tcp --dport 20:30 -j REJECT
iptables -t filter -I OUTPUT -d 192.168.1.2 -p tcp --dport :30 -j REJECT
iptables -t filter -I OUTPUT -d 192.168.1.2 -p tcp --dport 20: -j REJECT
iptables -t filter -I OUTPUT -d 192.168.1.2 -p tcp ! --sport 22 -j REJECT
```

##### 可以省略-m，此时使用的拓展模块与选择的协议一致



#### multiport拓展模块

**-p tcp -m multiport --sport**：用于匹配离散的多个源端口号，端口号之间用“逗号”隔开

**-p tcp -m multiport --dport**：用于匹配离散的多个目标端口号，端口号之间用“逗号”隔开

```
iptables -t filter -I OUTPUT -d 192.168.1.2 -p tcp -m multiport --sport 22,23 -j REJECT 
iptables -t filter -I IUTPUT -d 192.168.1.2 -p tcp -m multiport --dport 20,23 -j REJECT 
```



#### iprange拓展模块

**-m iprange --src-range**：用于匹配一段连续的源IP地址范围

**-m iprange --dst-range**：用于匹配一段连续的目标IP地址范围

```
iptables -I INPUT -m iprange --src-range 192.168.1.1-192.168.1.5 -j DROP
iptables -I INPUT -m iprange --dst-range 192.168.1.1-192.168.1.5 -j DROP
```



#### string拓展模块

匹配报文中是否包含指定的字符串

```
iptables -I INPUT -m string --algo 算法 --string 指定字符串 -j REJECT
```

**--algo**：指定匹配算法，可选算法有bm和kmp，**必选项**

**--string**：指定匹配的字符串



#### time拓展模块

根据时间段匹配报文

```
iptables -I OUTPUT -m time --timestart 09:00:00 --timestop 12:00:00 -j REJECT
```

**--timestart**：指定匹配的起始时间

**--timestop**：指定起始的结束时间

```
iptables -I OUTPUT -m time --weekdays 6,7 --monthdays 22,23 -j REJECT
```

**--weekdays**：指定匹配每个星期的哪一天，除了用数字表示，还可以用缩写，例如，Mon，Tue，Wed，Thu，Fri，Sat，Sun

**--monthdays**：指定匹配每个月的哪一天

```
iptables -I OUTPUT -m time --datestart 2017-12-20 --datestop 2017-12-25 -j REJECT
```

**--datestart**：指定日期的开始时间

**--datestop**：指定日期的结束时间

--monthdays与--weekdays可以使用 ! 取反，其他选项不可以



#### connlimit拓展模块

限制每个IP地址同时连接到server端的链接数量

```
iptables -I INPUT -p tcp --dport 22 -m connlimit --connlimit-above 2 -j REJECT
```

**--connlimit-above**：限制链接的数量

```
iptables -I INPUT -m connlimit -connlimit-above 2 --connlimit-mask 24 -j REJECT
```

**--connlimit-mask**：子网掩码位数，表示一个IP段。



#### limit拓展模块

对单位时间内流入包的数量进行限制

```
iptables -I INPUT -p icmp -m limit --limit 10/minute -j ACCEPT
iptables -A INPUT -p icmp -j REJECT
```

第一条规则每个六秒钟接收一个包，其他包通过第二条规则拒绝

**--limit**：限制单位时间流入包的数量，单位/second，/minute，/hour，/day

```
iptables -I INPUT -p icmp -m limit --limit-burst 3 --limit 10/minute -j ACCEPT
```

**--limit-burst**：空闲时指定放行包的数量，

注：令牌桶算法，--limit-burst相当于令牌桶里有的令牌数量，--limit相当于多少时间生成一个令牌。数据包通过时消耗一个令牌。一开始消耗桶中原有的令牌，消耗完之后就靠单位时间生成的令牌通过。











