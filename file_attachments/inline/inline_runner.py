import base64
import pathlib

from lxml import etree
from zeep import Client
from zeep.plugins import HistoryPlugin

BASE_PATH = pathlib.Path(__file__).resolve().parents[0]
WSDL = BASE_PATH.joinpath('inline.wsdl')
ATTACHMENT = BASE_PATH.joinpath('shinanogold.png')


def run():
    # バイナリ形式でファイルを読み込み
    with ATTACHMENT.open(mode='rb') as f:
        attachment_data = f.read()

    # ファイルをBase64エンコード
    encoded_data = base64.b64encode(attachment_data)

    history_plugin = HistoryPlugin()
    client = Client(str(WSDL), plugins=[history_plugin])

    # ZeepクライアントにBase64エンコードしたデータを渡す
    # この場合、上記で定義した `image` elementに渡している
    response = client.service.requestMessage(image=encoded_data)

    print('--- request body ---')
    print(etree.tostring(history_plugin.last_sent['envelope'], pretty_print=True, encoding='unicode'))

    print('--- response ---')
    print(response)


if __name__ == '__main__':
    run()
