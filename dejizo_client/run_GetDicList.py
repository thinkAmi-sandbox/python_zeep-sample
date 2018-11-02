import pathlib

from zeep import Client

WSDL = pathlib.Path.cwd().joinpath('SoapServiceV11.xml')


def call_api_with_get_type():
    client = Client(str(WSDL))
    xsd_string = client.get_type('xsd:string')

    response = client.service.GetDicList(AuthTicket=xsd_string(''))
    print(response)


def call_api_without_get_type():
    client = Client(str(WSDL))

    response = client.service.GetDicList(AuthTicket='')
    print(response)


if __name__ == '__main__':
    # client.get_type() を使うパターン
    call_api_with_get_type()

    # client.get_type() を使わないパターン
    call_api_without_get_type()
