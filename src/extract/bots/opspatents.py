import numpy as np
import epo_ops
import xmltodict
import logging

from utils.bot import Bot


class BotInstance(Bot):
    collection = 'bots.epo.patents'
    key = '@doc-number'

    def process_item(self, db=None):
        collections = [
            ('data.organizations', 'nombre')
        ]

        organizations = set()
        for k, v in collections:
            organizations = organizations.union(db[k].distinct(v))

        __key__ = 'OQZtQ6amCYzhovfqvXxI9DgOEDPymHzT'
        __secret__ = 'MJuF1bivcTGMiK1m'

        client = epo_ops.Client(
            key=__key__,
            secret=__secret__
        )

        for organization in sorted(organizations):
            end = 1
            total = np.Inf
            while end <= total:
                try:
                    response = client.published_data_search(
                        cql='ia all "{}"'.format(organization),
                        range_begin=end,
                        range_end=end + 24,
                        constituents=[
                            'biblio'
                        ]
                    )
                    data = xmltodict.parse(response.text)['ops:world-patent-data']['ops:biblio-search']
                    for x in data['ops:search-result']['exchange-documents']:
                        yield x['exchange-document']
                    total = int(data['@total-result-count'])
                    end = int(data['ops:range']['@end']) + 1
                except Exception as e:
                    # TODO: Define exception
                    logging.debug(e)
                    break
