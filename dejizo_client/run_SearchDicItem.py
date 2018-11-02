import pathlib

from zeep import Client

WSDL = pathlib.Path.cwd().joinpath('SoapServiceV11.xml')


def get_guid_list_from_api():
    client = Client(str(WSDL))

    response = client.service.GetDicList(AuthTicket='')
    return [response[0]['DicID'], response[1]['DicID']]


def call_api_with_get_type():
    def create_query(word):
        ns0_merge_option = client.get_type('ns0:MergeOption')
        ns0_match_option = client.get_type('ns0:MatchOption')

        query = client.get_type('ns0:Query')(
            Words=xsd_string(word),
            ScopeID=xsd_string('HEADWORD'),
            MatchOption=ns0_match_option('EXACT'),
            MergeOption=ns0_merge_option('OR')
        )
        return query

    client = Client(str(WSDL))
    xsd_string = client.get_type('xsd:string')
    xsd_unsigned_int = client.get_type('xsd:unsignedInt')
    ns1_guid = client.get_type('ns1:guid')

    guid_list = get_guid_list_from_api()
    guids = client.get_type('ns0:ArrayOfGuid')([
        ns1_guid(guid_list[0]),
        ns1_guid(guid_list[1]),
    ])
    queries = client.get_type('ns0:ArrayOfQuery')([
        create_query('apple'),
        create_query('america'),
    ])

    response = client.service.SearchDicItem(
        AuthTicket=xsd_string(''),
        DicIDList=guids,
        QueryList=queries,
        SortOrderID=xsd_string(''),
        ItemStartIndex=xsd_unsigned_int('0'),
        ItemCount=xsd_unsigned_int('2'),
        CompleteItemCount=xsd_unsigned_int('2'),
    )

    for r in response['ItemList']['DicItem']:
        print(r['Title']['_value_1'].text)
        print(dir(r['Title']['_value_1']))
        print('=' * 5)


def call_api_without_get_type():
    def create_query(word):
        return {
            'Words': word,
            'ScopeID': 'HEADWORD',
            'MatchOption': 'EXACT',
            'MergeOption': 'OR',
        }

    client = Client(str(WSDL))
    guids = {'guid': get_guid_list_from_api()}
    queries = {
        'Query': [
            create_query('apple'),
            create_query('america'),
        ]
    }

    response = client.service.SearchDicItem(
        AuthTicket='',
        DicIDList=guids,
        QueryList=queries,
        SortOrderID='',
        ItemStartIndex=0,
        ItemCount=2,
        CompleteItemCount=2,
    )

    for r in response['ItemList']['DicItem']:
        print(r['Title']['_value_1'].text)
        print(dir(r['Title']['_value_1']))
        print('=' * 5)


if __name__ == '__main__':
    # client.get_type() を使うパターン
    call_api_with_get_type()

    # client.get_type() を使わないパターン
    call_api_without_get_type()
