##### #1 确认SQLServer服务器与远程端网络上是通的。

##### #2 SQLServer数据库服务器开启允许远程链接

本地账户登录，右键数据库，选择属性选项

![1547447533383](C:\Users\fandashen\AppData\Roaming\Typora\typora-user-images\1547447533383.png)

选择"连接"，勾选“允许远程连接到此服务器”：

![1547449130529](C:\Users\fandashen\AppData\Roaming\Typora\typora-user-images\1547449130529.png)

##### #3 对SQL服务器进行配置（MSSQLServer）

![1547449411293](C:\Users\fandashen\AppData\Roaming\Typora\typora-user-images\1547449411293.png)

确保SQLServer服务已经启动

![1547449714044](C:\Users\fandashen\AppData\Roaming\Typora\typora-user-images\1547449714044.png)

启用TCP/IP协议，端口都设置为1433

![1547449588906](C:\Users\fandashen\AppData\Roaming\Typora\typora-user-images\1547449588906.png)

##### #4 对服务器进行防火墙配置，添加对于1433的入站规则