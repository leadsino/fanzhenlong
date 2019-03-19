SQLServer可以通过Ole Automation的存储过程调用外部服务，操作文件等相关操作。

内置的存储过程

![1547452608438](C:\Users\fandashen\AppData\Roaming\Typora\typora-user-images\1547452608438.png)

默认情况下Ole Automation procedures组件是禁止的。SQL Server阻止了对组件'Ole Automation Procedures'的过程'sys.sp_OACreate'的访问。系统管理员可以通过sp_configure启用“Ole Automation procedures”。

```
sp_configure 'show advanced options',1;
RECONFIGURE;
EXEC sp_configure 'Ole Automation procedures',1;
RECONFIGURE;
GO
EXEC sp_configure 'show advanced options',0;
RECONFIGURE;
GO
```

当启用OLE Automation Procedures时，对sp_OACreate的调用将会启动OLE共享执行环境。

#### 创建OLE对象

```
sp_OACreate { progid | clsid } , objecttoken OUTPUT [ , context ]
```

**progid**：要创建的OLE对象编程标识符，形式为，‘OLEComponent.Object’

OLEComponent是自动化服务器的组件名称，Object是OLE对象的名称，指定的OLE对象必须有效且必须支持IDispatch接口。

**clsid**：要创建的OLE对象的类标识符，形式为，‘{nnnnnnnn-nnnn-nnnn-nnnn-nnnnnnnnnnnn}’

**objecttoken**：返回的对象令牌，int型局部变量，用于调用其他OLE自动化存储过程

**context**：指定要运行的上下文

1=仅使用进程内（.dll）ole服务器

4=仅使用本地（.exe）ole服务器

5=同时使用进程和本地

默认为5。

当上下文值是1或5，该服务器可以访问SQLServer拥有的资源。进程内OLE服务器可能破坏SQLServer的内存或资源并导致不可预知的结果。

#### 调用OLE对象方法

```
sp_OAMethod objecttoken , methodname  
    [ , returnvalue OUTPUT ]   
    [ , [ @parametername = ] parameter [ OUTPUT ] [ ...n ] ]
```

**objecttoken**：对象令牌，int型局部变量

**methodname**：要调用的OLE对象的方法名

**returnvalue OUTPUT**：OLE对象的返回值。

如果返回的是OLE对象，returnvalue必须是int类型，此对象令牌可用于其他OLE自动化存储过程。

**parameter**：OLE对象的方法的参数。



#### 示例

```
DECLARE @ExpectedFolder VARCHAR(50)='C:\Users\Administrator\Desktop\'
DECLARE @ExpectedFilePrefix VARCHAR(10)='test'
DECLARE @ExpectedFullFileName VARCHAR(255)= 
               @ExpectedFolder + @ExpectedFilePrefix + '.txt'

DECLARE @returnCode INT
DECLARE @objectToken INT
DECLARE @CFToken INT
DECLARE @fileToken INT
DECLARE @txtToken INT
DECLARE @txt VARCHAR(255)

EXEC sp_OACreate 'Scripting.FileSystemObject',@objectToken OUTPUT 

exec sp_OAMethod @objectToken,'CreateTextFile',
                 @CFToken OUTPUT,@ExpectedFullFileName,'True'
SELECT @CFToken

exec sp_OAMethod @objectToken,'FileExists',
                 @returnCode OUTPUT,@ExpectedFullFileName
SELECT @returnCode
```

参考文档：http://blog.sina.com.cn/s/blog_5d5562600101emnd.html

https://docs.microsoft.com/zh-cn/previous-versions/sql/sql-server-2012/ms189763(v%3dsql.110)