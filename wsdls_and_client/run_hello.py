import pathlib

from zeep import Client

WSDL = pathlib.Path.cwd().joinpath('Hello.wsdl')


client = Client(str(WSDL))
response = client.service.requestMessage()

print(type(response))
print(response)
