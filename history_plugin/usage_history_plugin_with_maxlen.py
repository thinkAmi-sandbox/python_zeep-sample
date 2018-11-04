import pathlib

from lxml import etree
from zeep import Client
from zeep.plugins import HistoryPlugin

WSDL = pathlib.Path.cwd().joinpath('RequestResponse.wsdl')


history_plugin = HistoryPlugin(maxlen=3)
client = Client(str(WSDL), plugins=[history_plugin])
client.service.requestMessage(userName='taro')
client.service.requestMessage(userName='jiro')
client.service.requestMessage(userName='saburo')

print(history_plugin._buffer)
# =>
# deque([
#   {'received': {
#       'envelope': <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x10ae37a08>,
#       'http_headers': {
#           'Content-Type': 'text/xml; charset=utf-8', 'Content-Encoding': 'gzip',
#           'Content-Length': '198', 'Server': 'Jetty(6.1.26)'}},
#    'sent': {
#       'envelope': <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x10adf28c8>,
#       'http_headers': {
#           'SOAPAction': '"http://example.com/HelloWorld/requestMessage"',
#           'Content-Type': 'text/xml; charset=utf-8'}}},
#   {'received': {
#       'envelope': <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x10ae43648>,
#       'http_headers': {
#           'Content-Type': 'text/xml; charset=utf-8', 'Content-Encoding': 'gzip',
#           'Content-Length': '199', 'Server': 'Jetty(6.1.26)'}},
#    'sent': {
#       'envelope': <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x10ae28e88>,
#       'http_headers': {
#           'SOAPAction': '"http://example.com/HelloWorld/requestMessage"',
#           'Content-Type': 'text/xml; charset=utf-8'}}},
#   {'received': {
#       'envelope': <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x10ae43dc8>,
#       'http_headers': {
#           'Content-Type': 'text/xml; charset=utf-8', 'Content-Encoding': 'gzip',
#           'Content-Length': '199', 'Server': 'Jetty(6.1.26)'}},
#    'sent': {
#       'envelope': <Element {http://schemas.xmlsoap.org/soap/envelope/}Envelope at 0x10ae43088>,
#       'http_headers': {
#           'SOAPAction': '"http://example.com/HelloWorld/requestMessage"',
#           'Content-Type': 'text/xml; charset=utf-8'}}}],
#   maxlen=3)


buf = history_plugin._buffer[2]
print(type(buf))
# => <class 'dict'>

print(etree.tostring(buf['sent']['envelope'], pretty_print=True, encoding='unicode'))
# =>
# <soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
# <soap-env:Body>
# <ns0:RequestInterface xmlns:ns0="http://example.com/HelloWorld">
# <ns0:userName>saburo</ns0:userName>
# </ns0:RequestInterface>
# </soap-env:Body>
# </soap-env:Envelope>
