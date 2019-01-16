如果将scan for startup procs设置为1，则SQL Server启动时将扫描服务器上定义的所有自动运行的存储区过程，并运行这些过程。

##### 自动执行的存储过程使用与固定服务器角色 **sysadmin** 成员相同的权限进行操作

检查配置值

```
SELECT name, 
	CAST(value as int) as value_configured, 
	CAST(value_in_use as int) as value_in_use 
FROM sys.configurations 
WHERE name = 'scan for startup procs';
```

此选项通过sp_configure进行设置

```
EXECUTE sp_configure 'show advanced options', 1; 
RECONFIGURE; 
EXECUTE sp_configure 'scan for startup procs', 0; 
RECONFIGURE; 
GO 
EXECUTE sp_configure 'show advanced options', 0; 
RECONFIGURE;
```

重启数据库引擎将应用配置

我们可以通过sp_procoption存储过程将指定存储过程设置为自动执行

```
sp_procoption [ @ProcName = ] 'procedure' 
        , [ @OptionName = ] 'option' 
        , [ @OptionValue = ] 'value'
示例：sp_procoption 'procA','startup',true
```

**[ @ProcName = ] 'procedure'**

设置选项的存储过程的名称。数据类型nvarchar（776），无默认值

**[ @OptionName = ] 'option'**

设置选项的名称。唯一值startup

**[ @OptionValue = ] 'value'**

开启（true/on）还是关闭（false/off），数据类型varchar（12），无默认值