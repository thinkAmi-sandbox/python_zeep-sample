import base64
import mimetypes
import uuid
import pathlib
from typing import Iterable

from zeep.transports import Transport
from zeep.wsdl.utils import etree_to_string


class SwATransport(Transport):
    """ SOAP with Attachment (SwA、非swaRef)用のTransport

    添付ファイルは、binary/Base64エンコードのどちらも可 (引数is_base64izeで切り替え)
    なお、Type Hints は、自作部分のみ記載(Zeepのものは不明/差し替わる可能性があるため)
    """
    NEW_LINE_FOR_SWA_BODY = b'\r\n'

    def __init__(self, file: pathlib.Path, attachment_content_id: str, is_base64ize: bool = False,
                 cache=None, timeout=300, operation_timeout=None, session=None) -> None:
        self.file = file
        self.attachment_content_id = attachment_content_id
        self.is_base64ize = is_base64ize

        # boundaryとSOAP部分のContentIDは任意の値で良いため、内部で生成する
        self.boundary = f'boundary_{self._generate_id_without_hyphen()}'
        self.soap_message_content_id = f'start_{self._generate_id_without_hyphen()}'

        super().__init__(cache=cache, timeout=timeout, operation_timeout=operation_timeout,
                         session=session)

    def post_xml(self, address, envelope, headers):
        """ オーバーライドして、SwAデータをPOSTできるようにする """

        message = self._create_message(envelope)
        self._add_swa_header(headers, message)

        # SwAの添付ファイル部分はSOAP envelopeの外側にあり、HistoryPluginでは表示されないため、
        # 送信時のmessageを見るためにprint()しておく
        print(message)

        # etree_to_string()はすでに実行済のため、元々のpost_xml()にあった、self.post()だけ実装する
        return self.post(address, message, headers)

    def _create_message(self, envelope) -> bytes:
        """ SwA用のリクエストボディを作成する

        requests.post() で送信するため、bytes型で返すこと
        """

        # SOAP部分の作成
        soap_part = self._create_soap_part(envelope)
        # 添付ファイル部分の作成
        attachment_part = self._create_attachment_part()

        return self.NEW_LINE_FOR_SWA_BODY.join([
            soap_part,
            attachment_part,
            self._format_bytes(b'--%a--', (self.boundary,)),
        ])

    def _create_soap_part(self, envelope) -> bytes:
        """ レスポンスボディのうち、SOAP部分を作成する """
        mime_message_header = self.NEW_LINE_FOR_SWA_BODY.join([
            self._format_bytes(b'--%a', (self.boundary,)),
            b'Content-Type: text/xml; charset=utf-8',
            b'Content-Transfer-Encoding: 8bit',
            self._format_bytes(b'Content-ID: %a', (self.soap_message_content_id,)),
            b'',
        ])

        # etree_to_string()にて、envelopeをbytes型の送信データへ変換する
        return self.NEW_LINE_FOR_SWA_BODY.join([
            mime_message_header,
            etree_to_string(envelope),
        ])

    def _create_attachment_part(self) -> bytes:
        """ レスオンスボディのうち、添付ファイル部分を作成する """
        if not self.file:
            return b''

        transfer_encoding = 'base64' if self.is_base64ize else 'binary'

        # ファイル名からMIMEタイプを推測するが、戻り値はタプルであることに注意
        # Content-Type向けのは1つ目の要素
        # https://docs.python.jp/3/library/mimetypes.html#mimetypes.guess_type
        content_type, _ = mimetypes.guess_type(str(self.file))

        mime_part_header = self.NEW_LINE_FOR_SWA_BODY.join([
            self._format_bytes(b'--%a', (self.boundary,)),
            self._format_bytes(b'Content-Transfer-Encoding: %a', (transfer_encoding,)),
            self._format_bytes(b'Content-Type: %a; name="%a"', (content_type, self.file.name)),
            self._format_bytes(b'Content-ID: <%a>', (self.attachment_content_id,)),
            self._format_bytes(b'Content-Disposition: attachment; name="%a"; filename="%a"',
                               (self.file.name, self.file.name)),
            b'',
        ])

        # 添付ファイルはバイナリ(bytes型)であることに注意
        with self.file.open(mode='rb') as f:
            attachment_data = f.read()

        if transfer_encoding == 'base64':
            attachment_data = base64.b64encode(attachment_data)

        return self.NEW_LINE_FOR_SWA_BODY.join([
            mime_part_header,
            attachment_data,
        ])

    def _add_swa_header(self, headers: dict, message: bytes):
        """ SwA用のヘッダを追加する """

        headers["Content-Type"] = "; ".join([
            "multipart/related",
            'boundary="{}"'.format(self.boundary),
            'type="text/xml"',
            'start="{}"'.format(self.soap_message_content_id),
            "charset=utf-8"
        ])
        headers["Content-Length"] = str(len(message))

    def _generate_id_without_hyphen(self) -> str:
        """ uuid4()でIDを生成する

        uuid4()だとハイフンも含まれるため、削除しておく
        """
        return str(uuid.uuid4()).replace("-", "")

    def _format_bytes(self, target: bytes, values: Iterable[str]) -> bytes:
        """ bytes型にstr型を埋め込む

        埋め込むと、シングルクォート(')まで含まれてしまうため、削除しておく
        """
        return (target % values).replace(b"'", b"")
