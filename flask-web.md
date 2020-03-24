#### flask-demo（部署基于flask工程到函数计算）

通过该模板的示例代码，用户可以通过url去访问函数，实现flask web工程serverless
用户通过 $(account-id).$(region).fc.aliyuncs.com/2016-08-15/proxy/serviceName/functionName/ 访问函数
比如: account-id为12345，region为cn-shanghai, serviceName为fcService, functionName为test, 那么访问函数的url就是12345.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/fcService/test/

#### 输入参数

无(http 触发)

#### 输出参数

web html 页面