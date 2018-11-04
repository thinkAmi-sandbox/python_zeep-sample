import pathlib

from zeep import Client

WSDL = pathlib.Path.cwd().joinpath('RequestResponse.wsdl')


client = Client(str(WSDL))
response = client.service.requestMessage(userName='taro')

print(type(response))
print(response)
