import pathlib

from lxml import etree
from requests import Session
from swa_transport import SwATransport
from zeep import Client
from zeep.plugins import HistoryPlugin

BASE_PATH = pathlib.Path(__file__).resolve().parents[0]
WSDL = BASE_PATH.joinpath('swa.wsdl')
ATTACHMENT = BASE_PATH.joinpath('shinanogold.png')


def run(attachment_content_id, is_base64ize=False):
    session = Session()
    transport = SwATransport(ATTACHMENT, attachment_content_id=attachment_content_id,
                             is_base64ize=is_base64ize, session=session)

    history_plugin = HistoryPlugin()
    client = Client(str(WSDL), transport=transport, plugins=[history_plugin])
    response = client.service.requestMessage()

    print('--- history ---')
    print('-- header --')
    print(history_plugin.last_sent)
    print('-- SOAP envelope --')
    print(etree.tostring(history_plugin.last_sent['envelope'],
                         pretty_print=True, encoding='unicode'))
    print('--- response ---')
    print(response)


if __name__ == '__main__':
    print('-' * 40)
    print('添付ファイルはバイナリのまま送信')
    print('-' * 40)
    run(attachment_content_id='ham', is_base64ize=False)

    print('-' * 40)
    print('添付ファイルはBASE64化して送信')
    print('-' * 40)
    run(attachment_content_id='spam', is_base64ize=True)
