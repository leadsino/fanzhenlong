#### 1.  Web应用扫描器简介

##### 1.1 什么是Web漏洞扫描器

​	Web应用扫描器是一种对目标站点持续发送http（s）请求，通过对服务器响应进行分析，从而发现被扫描站点存在的安全风险以及漏洞的工具。

​	一个综合的业务系统存在着大量的Web页面和资源，以简单的登陆界面为例，当用户输入用户名和密码提交时，业务系统需要对其参数进行验证，在系统开发安全意识不足时，这个验证过程就可能存在一定的安全风险。当业务系统的逻辑越复杂，内容越丰富，存在安全风险的几率就越高。若攻击者通过Web应用扫描器进行扫描，业务系统的安全问题会很快暴露，并被攻击者所利用 ，从而对业务系统不同程度的侵害。

##### 	1.2 Web应用扫描器的工作原理

​	Web应用扫描器扫描站点一般分为三个阶段。

​	第一阶段：站点爬行

​	扫描器通过爬虫爬取目标站点的所有链接以及页面中的所有资源，以获取整个站点的层次结构。这一过程可以分为两步：（1）网络访问。（2）收集链接（url）。

​	在扫描器进行对特定站点进行网络访问时，可以伪装自身的请求信息，cookie信息，在得到站点响应后，可以从html或者html注释等静态资源以及通过Webkit从渲染后的DOM树，JS等动态资源中收集静态或动态的链接。

​	第二阶段：探测点获取

​	探测点由扫描器自定义的规则库所设置，常用的探测点包括get请求中的url参数，cookie值，请求头部，响应体等。探测点将用于下一步的漏洞探测。

​	第三阶段：漏洞检测

​	扫描器通过对探测点注入攻击代码来检测是否存在着相应的安全漏洞。在攻击中可能会发现新的url，此时再重复扫描过程，直至扫描结束。常见的攻击类型包括：SQL注入攻击，XSS跨站脚本攻击，CSRF跨站请求伪造，弱口令检测，文件上传攻击，网络脚本攻击等。

![1](https://github.com/leadsino/dqk/blob/master/3.7/images/1.png?raw=true)

##### 1.3 扫描器的常见特征

​	扫描器对站点进行扫描与正常用户访问有何区别?

​	本文主要总结了以下几点：

​	（1）扫描器自带指纹

​	市场上存在一系列开源或者商用的Web应用扫描器。商用产品如Acunetix Web Vulnerability Scanner，AppScan，绿盟极光等，开源产品如Nikto，Paros proxy，X-scan等，每种扫描器的特点或许不同，但其主要扫描原理是相同的，并且开源产品往往不如商用版功能全面。目前汉武实验室暂时针对市面上最常用的AVWS，AppScan，绿盟极光进行相应的研究。

​	Awvs（Acunetix Web Vulnerability Scanner ）对目标站点进行扫描时，往往在http(s)请求中会带有其特征的指纹。

​	Awvs在请求url、header、body中往往会带有自身的特征信息。

```http
（1）Url:
acunetix-wvs-test-for-some-inexistent-file
by_wvs
acunetix_wvs_security_test
acunetix
acunetix_wvs
acunetix_test
（2）Headers:
Accept:acunetix/wvs
Accept-Language: acunetix_wvs_security_test
Acunetix-Aspect:
Acunetix-Aspect-Password:
Acunetix-Aspect-Queries:
Client-IP: acunetix_wvs_security_test
Cookie: acunetix
Cookie: acunetixCookie
Cookie: acunetix_wvs_security_test
Host: acunetix_wvs_security_test
HTTP_AUTH_PASSWD: acunetix
Location: acunetix_wvs_security_test
Origin: $(@print(md5(acunetix_wvs_security_test)))
Referer: acunetix_wvs_security_test
User-Agent: acunetix_wvs_security_test
Via: acunetix_wvs_security_test
X-Forwarded-Host: acunetix_wvs_security_test
X-Forwarded-For: acunetix_wvs_security_test
（3）Body
acunetix
acunetix_wvs_security_test
```

​	Appscan也会在扫描发送http(s)请求时，在其中会带有其特征的指纹。

```http
（1）Url
Appscan
（2）Headers
Accept: Appscan
Content-Type: Appscan
Content-Type: AppScanHeader
User-Agent:Appscan
（3）body
Appscan
```

​	绿盟极光同样会在扫描发送http(s)请求时，在其中会带有其特征的指纹。

```http
（1）Url
nsfocus
（2） Headers
User-Agent: Rsas
```

​	（2）时间特征

​	对扫描器而言都具有一个相同的时间特征。当扫描器通过对目标站点不断发出http请求来进行扫描时，单位时间内同一个IP地址对目标站点发出请求是大大区别于正常用户访问的。

​	（3）行为特征

​	扫描器在扫描过程中会有站点爬行，探测点获取和漏洞检测三个步骤。

​	每个步骤都会有扫描器区别于正常用户访问的特征。

​	扫描器在进行站点爬行时，会对网页html（包括注释）中存在的所有链接加以访问，而一些暗链或是注释中的链接等是普通用户无法触发的。

​	扫描器在进行探测点获取时，会构造出各种特殊的网页请求，对站点存在的资源进行访问，如对某个动态资源（http://www.xxx.com/js/xx.js)，这也是区别于普通用户访问之处。另外扫描器构造的站点不一定是真实存在的，所以目标站点会返回的大量的404响应。

​	扫描器在进行漏洞检测时，会对各个探测点注入攻击代码，此时发生的http(s)请求的url中会带有恶意代码。如当扫描器进行SQL注入攻击时，请求url往往会包括一些非法参数——id为负数，"$,-,!"等；当扫描器进行XSS攻击时，请求url通常会包含一些JS代码；当扫描器进行CSRF攻击时，往往请求url中会包含恶意的referer字段。

​	

#### 2. 扫描器防御措施

##### 2.1 隐藏的链接标签

​	对应web扫描器来说，一些扫描器的爬虫会把页面里面的所有链接都会去做一个探测。并且有些更强大的扫描器还能够渲染css与js，爬出更多的链接进行探测，甚至能够将注释中的内容也扫描出来。但对于那些基于字典的扫描器，就不一定又有效了。

​	为什么要使用隐藏的标签链接呢？隐藏的标签链接是只正常的使用者不会察觉到，也不会去触发。比如：

```
<a href="http://www.baidu.com"></a>
```

​	这种标签人是点击不到的（链接标签没有text，不会显示在页面）。



​	通过我们的WAF做一个实验，它能通过更改代理的业务系统返回流的HTML内容。

![2](https://raw.githubusercontent.com/leadsino/fanzhenlong/master/images/1552030121536.png)

​	其中内容替换就是将返回流内的某个字符串替换成新的字符串，来达到我们所需要的目的。这样一来我们就可以将我们的隐藏链接标签加入到业务系统的页面里。

![1552032408902](https://raw.githubusercontent.com/leadsino/fanzhenlong/master/images/1552032408902.png)

​	在返回流的body前插入一个隐藏的链接标签。

​	通过WAF代理后查看页面，我们可以看到我们插入的链接标签在html内容中了。正常用户使用是看不到这个链接，且不通过WAF访问也看不到这个链接标签。

![1552033714720](https://raw.githubusercontent.com/leadsino/fanzhenlong/master/images/1552033714720.png)

​	这时候，我们通过AWVS扫描器去扫描这个这个业务系统。AWVS会抓取页面里的所有链接，再递归抓取的链接页面中链接。

![1552034079620](https://raw.githubusercontent.com/leadsino/fanzhenlong/master/images/1552034079620.png)

​	扫描器肯定就是会去对这个链接进行访问，这时候WAF一旦接收到这个插入的链接的请求，就对发起请求的用户进行限制，比如IP禁止，或是限制访问一些目录。所以针对这一类的扫描器，这种设置隐藏链接标签陷阱的措施还是挺有效的。

​	不单单可以直接插入隐藏的a标签，有些扫描器还能够扫描到注释内容，可以把链接放在注释中，同样能够被访问。

​	但是正常情况下也一直往用户访问的页面中插入代码也是让人很反感的，所以就可以在前面做一些限制条件，比如说用户访问频率达到一定的阈值，再给这个用户单独插入一个隐藏标签。这样既不影响正常业务，也能很好的抵御扫描器。

##### 2.2 单IP某段时间触发规则次数

​	一般来说，扫描器都是会在短时间内向服务器大量发送请求。根据某个IP某时间段内触发WAF拦截规则的次数大于设定的某个阀值，比如在5秒内，扫描器的IP触发WAF拦截规则20次，就认定为非法访问，就可以对该IP进行封禁。

​	但是大多数情况下，可能业务系统是不同用户同一个IP访问过来的，这时候就不能针对某一个IP进行设定规则。需要根据IP地址和Cookie一起来确定用户身份，防止误阻拦。另外还可以加入user agent，referer等设定更多维度的规则。

##### 2.3 Cookie植入与验证码

​	cookie注入与验证码与上面的隐藏链接植入其实大同小异。

​	cookie植入原理：当攻击者在固定的时间内触发规则到一定的阈值，给请求发起者的植入一个cookie，需要攻击者下次请求要带着这个cookie，如果没有带上，则可能就是扫描器。

​	而验证码验证也与cookie差不多，只是把cookie换成的验证码。常见的有想发帖网站，当连续发帖时，之后的发帖会带上验证码来限制你的发帖速度，而扫描器则可能就停在了验证验证码这一步。这种方法也被用于CC攻击。

##### 2.4 返回http状态404比例

​	有一类是探测敏感目录和文件的扫描器，这类的扫描器都是基于字典文件，通过对字典文件内的url进行请求获得返回信息来进行判断目录或者文件是否存在。比如nikto，skipfish这类扫描器，都是基于字典库来猜解文件及目录。

​	说道进行猜解，想必当这类扫描器去扫描我们的业务系统的时候，就会在一段时间内快速发送请求，而且会出现大量的404状态的服务器返回。这时候WAF可以收集针对这个IP在这段时间内返回404状态的数目，到达一段的阈值对其进行封禁。

​	用nikto去扫描测试业务系统，会发现它在基于它的字典再进行扫描。

![1552036658692](https://raw.githubusercontent.com/leadsino/fanzhenlong/master/images/1552036658692.png)

​	并且得到的服务器返回基本上都是404。

![1552036709927](https://raw.githubusercontent.com/leadsino/fanzhenlong/master/images/1552036709927.png)



##### 2.5 限制某些特殊目录的访问

​	既然扫描器会来访问我的敏感文件及目录，那我为何不设置规则去保护我的敏感文件及目录。可以去设置的敏感目录文件的规则，对访问的url进行匹配，在一段时间内，一旦业务系统的敏感目录在一段时间内频繁的被访问，访问的频率达到一个设定的阈值，就可以对这个来源IP进行封禁。

##### 2.6 扫描器特征库

​	WAF最基本的防扫描器的行为，就是基于扫描器的指纹进行阻断了。不同的扫描器都有自己的一些特征，比如发出的请求会加一些特定的head 字段，测试漏洞的请求参数的值会带上自己扫描器的名称等。上面的第一节也介绍过了。这样就根据扫描器各自的指纹构建WAF的特征库，一旦匹配到对应扫描器的指纹，就可以封禁目标IP，去阻断扫描器的扫描工作。

​	但是，单单靠扫描器指纹构建特征库，是很容易被绕过。毕竟规则是死的，人是活的。攻击者会通过各自方法隐藏自己扫描器的指纹，以达到绕过WAF的特征库。所以说不是所有的扫描器请求会带上扫描器特征，根据扫描器指纹特征只能够抵挡之一部分扫描器的扫描。



#### 3. 陷阱反入侵

##### 3.1 反入侵准备

​	将一个测试用的业务系统（DVWA）的地址反向代理到汉领下一代应用防火墙的IP+PORT上，并利用汉领下一代应用防火墙的内容替换功能，向业务系统的某个页面加入一个无内容的a标签，如

```html
<a href="http://10.10.xxx.xx:xx/xxx.php"></a>
```

​	此链接是一个蜜罐页面，诱使攻击者停留。

##### 3.2 反入侵原理

![2](https://github.com/leadsino/dqk/blob/master/3.7/images/2.png?raw=true)

##### 3.3 反入侵实践

​	反入侵方使用WAF往指定业务系统界面植入<a>标签链接；链接是一个具有sql注入漏洞的网页，其中包含了一个精心构造的js，当扫描器对此链接发出http(s)请求时，会触发此JS，同时扫描器会被此具有漏洞的网页“吸引”，从而保持入侵方与反入侵方的连接；此时反入侵方可以使用BeEF框架中的一些工具就可以获取入侵方的一些网络信息，甚至是控制入侵方的浏览器进行更深层次的入侵。

​	（1）反入侵方使用汉领新一代Web应用防火墙往指定网页上添加<a>标签。

![3](https://github.com/leadsino/dqk/blob/master/3.7/images/3.png?raw=true)

​	（2）此时测试用业务系统（DVWA）网页源代码中，多出一个a标签。

![4](https://github.com/leadsino/dqk/blob/master/3.7/images/4.png?raw=true)

​	（3）入侵方用AWVS对此业务系统进行扫描。

![5](https://github.com/leadsino/dqk/blob/master/3.7/images/5.png?raw=true)

​	（4）通过BeEF服务器"hook"扫描器。

![6](https://github.com/leadsino/dqk/blob/master/3.7/images/6.png?raw=true)

​	此时反入侵方成功获取到入侵方的一些信息。



#### 参考资料

1. WEB漏洞扫描原理 https://cloud.tencent.com/developer/news/175423

2. 常见扫描器或者自动化工具的特征（指纹）https://www.freebuf.com/column/156291.html

3. 十大漏洞扫描程序 https://blog.csdn.net/jackpk/article/details/38226487
4. 深入探讨Web拦截技术 https://www.waitalone.cn/web-scanner-interception-technology-depth.html

