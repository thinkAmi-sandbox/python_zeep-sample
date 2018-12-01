# WSDLでのnamespaceとbindingの設定を抜粋
# <wsdl:definitions
#       xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
#       xmlns:soap11="http://schemas.xmlsoap.org/wsdl/soap/"
#       xmlns:http="http://schemas.xmlsoap.org/wsdl/http/"
#       xmlns:mime="http://schemas.xmlsoap.org/wsdl/mime/"
#       xmlns:xsd="http://www.w3.org/2001/XMLSchema"
#       xmlns:ns0="http://example.com/HelloWorld"
#       targetNamespace="http://example.com/HelloWorld">
# <wsdl:port name="HelloServicePort" binding="ns0:HelloBindingSoap11">
#   <soap11:address location="http://localhost:8088/mockHelloBindingSoap11"/>


import pathlib

from zeep import Client

WSDL = pathlib.Path(__file__).parents[0].joinpath('Hello.wsdl')

client = Client(str(WSDL))

# ServiceProxyを作成
service = client.create_service(
    '{http://example.com/HelloWorld}HelloBindingSoap11',
    'http://localhost:9100/hello'
)

# 通常
# response = client.service.requestMessage(userName='taro')
# だが、ServiceProxyを使う場合は以下のように書く
response = service.requestMessage(userName='taro')


print(type(response))
# => <class 'str'>

print(response)
# => Hello, taro
