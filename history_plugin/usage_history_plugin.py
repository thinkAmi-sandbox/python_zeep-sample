import pathlib

from lxml import etree
from zeep import Client
from zeep.plugins import HistoryPlugin

WSDL = pathlib.Path.cwd().joinpath('RequestResponse.wsdl')


history_plugin = HistoryPlugin()
client = Client(str(WSDL), plugins=[history_plugin])
response = client.service.requestMessage(userName='taro')

print(history_plugin.last_sent)
# =>
# {'envelope': <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x10929d988>,
#  'http_headers': {
#    'SOAPAction': '"http://example.com/HelloWorld/requestMessage"',
#    'Content-Type': 'text/xml; charset=utf-8'}}

print(type(history_plugin.last_sent['envelope']))
# => <class 'lxml.etree._Element'>

print(history_plugin.last_sent['envelope'])
# => <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x102c54a48>

print(etree.tostring(history_plugin.last_sent['envelope'], pretty_print=True, encoding='unicode'))
# =>
# <soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap-env:Body>
#     <ns0:RequestInterface xmlns:ns0="http://example.com/HelloWorld">
#       <ns0:userName>taro</ns0:userName>
#     </ns0:RequestInterface>
#   </soap-env:Body>
# </soap-env:Envelope>

print('-' * 30)

print(response)
# => Hello, taro

print(history_plugin.last_received)
# =>
# {'envelope': <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x1092e1ac8>,
#  'http_headers': {
#    'Content-Type': 'text/xml; charset=utf-8',
#    'Content-Encoding': 'gzip',
#    'Content-Length': '198', 'Server': 'Jetty(6.1.26)'}}

print(type(history_plugin.last_received['envelope']))
# => <class 'lxml.etree._Element'>

print(history_plugin.last_received['envelope'])
# => <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x102c98b48>

print(etree.tostring(history_plugin.last_received['envelope'], pretty_print=True, encoding='unicode'))
# => (長いので改行あり)
# <soapenv:Envelope
#       xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
#       xmlns:hel="http://example.com/HelloWorld">
#    <soapenv:Header/>
#    <soapenv:Body>
#       <hel:ResponseInterface>
#
#          <hel:returnMessage>Hello, taro</hel:returnMessage>
#       </hel:ResponseInterface>
#    </soapenv:Body>
# </soapenv:Envelope>
