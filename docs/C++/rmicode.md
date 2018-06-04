## gameworld与dataaccess的会话
gameworld对dataaccess说(session)：dataaccess，麻烦帮我从X表取出XX数据(远程方法),我在这等你(阻塞)。

dataacess马上从X表将XX数据取出，并在数据包(TLV)里放了一个成功标记，然后将数据打包到数据包里。

dataaccess递gameworld一个数据包(response)：搞定了，取出结果我放在数据包(TLV)里，你可以看一下。

gameworld拆开返回的数据包，看到了dataaccess标记着取出成功，就拿着数据走人了。

## 调用流程
ug04_cn的国家(Camp)初始化
gameworld
```
1.gameworld进程启动
2.执行CampManager::OnServerStart()
3.OnServerStart()调用CampManager::Load()
4.Load()内创建RMIInitCampBackObjectImpl实例和RMIGlobalClient实例
5.RMIGlobalClient实例绑定会话、远程调用方法和设置是否阻塞等
6.RMIGlobalClient实例调用成员方法InitCampAsyn
6.成员方法InitCampAsyn中m_session执行Call方法发送会话
7.等待接收dataaccess响应
8.拆开响应的TLV包，查看结果，成功获取数据执行CampManager::Instance().LoadRet()对国家对象进行初始化
```
dataaccess
```
1.dataaccess进程接收到请求
2.找到并执行对应的方法RMIGlobalObject::__InitCamp
3.创建一个临时CampParam对象并以引用方式传入InitCamp函数去数据库获取数据，返回获取数据结果
4.将返回结果结果压入TLVSerializer *out_param中，并判断返回结果是否正常，如果正常将临时CamParam对象序列化(TLV)进out_param
5.序列化完成后给gameworld发回一个响应，相应内容是序列化的结果
```