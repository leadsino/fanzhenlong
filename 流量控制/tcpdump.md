#### tcpdump是采用命令行方式对接口的数据包进行筛选抓取

##### 命令格式：

```
tcpdump [ -DenNqvX ] [ -c count ] [ -F file ] [ -i interface ] [ -r file ]
        [ -s snaplen ] [ -w file ] [ expression ]
```

##### 抓包选项：

-c：指定抓取的包数量。

-i interface：指定tcpdump监听的接口。未指定会从接口列表搜寻编号最小的已配置好的接口，不包括环回接口；可以使用any抓取所有接口。

-n：不做主机名解析。地址以数字方式显示。（实际测试端口也会数字显示）

-nn：除了有-n的作用，还把端口显示为数值。

-N：不打印host的域名部分。

-Q：指定抓取流入的包还是流出的包。给定“in”、“out”和“inout”，默认“inout”。

-s snaplen：设置tcpdump的数据包抓取长度。如果设置过小数据包会被截断。默认是65535字节。

##### 输出选项：

-e：输出的每行将包括数据链路层头部信息，源MAC和目标MAC

-q：快速打印输出。打印很少的协议相关信息。

-X：输出包的头部数据，以16进制和ASCII两种方式同时输出。

-XX：输出包的头部数据，以16进制和ASCII两种方式同时输出。更详细

-v：分析打印输出更详细。

-vv：比-v跟详细的输出。

-vvv：比-vv跟详细的输出。

##### 其他选项：

-D：列出可用于抓包的接口

-F：从文件中读取抓包的表达式。命令行中的其他表达式都失效。

-w：将抓取的数据输出到文件。

-r：从给定的数据包文件中读取数据。



#### tcpdump表达式

表达式用于筛选数据包。tcpdump的表达式由一个或多个"单元"组成，每个单元一般包含ID的修饰符和一个ID(数字或名称)。

```
tcpdump [options] [not] proto dir type
```

##### type：指定ID的类型

可以给定的值有host/net/port/portrange。

host指定一台主机

net指定一个网络地址

port指定一个端口号

portrange指定端口号范围

##### dir：指定ID的方向

可以给定的值有src/dst/src or dst/src and dst，默认为src or dst

src为源，dst为目标

##### proto：通过给定的协议限定匹配的数据包类型

常用的协议有tcp/udp/arp/ip/ether/icmp等，若为给定协议类型，则匹配所有可能的类型



**一个基本的表达式单元为“proto dir type ID” 即“协议 方向 类型 ID”**

除了这三种关键字之外，其他重要的关键字：gateway，broadcast，less，greater

取非运算not，！

与运算and，&&

或运算or，||



### 示例：

B想要截获主机210.27.48.1 和主机210.27.48.2 或210.27.48.3的通信

```
#tcpdump host 210.27.48.1 and / (210.27.48.2 or 210.27.48.3 /)
```

如果想要获取主机210.27.48.1接收或发出的telnet包

```
#tcpdump tcp port 23 and host 210.27.48.1
```

