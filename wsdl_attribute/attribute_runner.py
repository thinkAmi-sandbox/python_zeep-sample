import pathlib

import requests_mock
from lxml import etree
from zeep import Client
from zeep.exceptions import XMLSyntaxError
from zeep.plugins import HistoryPlugin

BASE_PATH = pathlib.Path(__file__).resolve().parents[0]


def set_root_attribute():
    history_plugin = HistoryPlugin()
    child_wsdl = BASE_PATH.joinpath('root_attribute.wsdl')
    client = Client(str(child_wsdl), plugins=[history_plugin])

    # Zeepと同様、requests_mockを使って、POSTをMockする
    # https://github.com/mvantellingen/python-zeep/blob/3.2.0/tests/integration/test_http_post.py#L15
    with requests_mock.mock() as m:
        m.post('http://localhost:9500/attributeBindingSoap11', text='<root>mocked!</root>')

        # requestMessage()の結果がWSDLの内容と異なるため、常にXMLSyntaxErrorが出る
        # 今回は送信したSOAPエンベロープの値を見たいので、例外は無視する
        try:
            response = client.service.requestMessage(href='ham_spam')
        except XMLSyntaxError:
            pass

        print(etree.tostring(history_plugin.last_sent['envelope'],
                             pretty_print=True, encoding='unicode'))


def set_child_attribute():
    history_plugin = HistoryPlugin()
    child_wsdl = BASE_PATH.joinpath('child_attribute.wsdl')
    client = Client(str(child_wsdl), plugins=[history_plugin])

    with requests_mock.mock() as m:
        m.post('http://localhost:9501/attributeBindingSoap11', text='<root>mocked!</root>')

        # requestMessage()の結果がWSDLの内容と異なるため、常にXMLSyntaxErrorが出る
        # 今回は送信したSOAPエンベロープの値を見たいので、例外は無視する
        try:
            response = client.service.requestMessage(image={'href': 'foo_bar'})
        except XMLSyntaxError:
            pass

        print(etree.tostring(history_plugin.last_sent['envelope'],
                             pretty_print=True, encoding='unicode'))


if __name__ == '__main__':
    print('-' * 40)
    print('親要素のattributeを設定')
    print('-' * 40)
    set_root_attribute()

    print('-' * 40)
    print('子要素のattributeを設定')
    print('-' * 40)
    set_child_attribute()
