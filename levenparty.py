import os
import random
import re

from restless.it import IttyResource
import itty
from pylev import levenshtein


__author__ = 'Daniel Lindsley'
__license__ = 'BSD'
__version__ = (1, 0, 0)


DEBUG = os.environ.get('DEBUG', False)
MAX_PARTIES = 500
LETTERS = [letter for letter in 'abcdefghijklmnopqrstuvwxyz']
LAST_FIFTY = []


class LevenPartyResource(IttyResource):
    debug = DEBUG

    def serialize_list(self, data):
        return self.raw_serialize(data)

    @classmethod
    def setup_urls(cls, rule_prefix):
        list_url = "%s" % itty.add_slash(rule_prefix)
        detail_url = "%s" % itty.add_slash(rule_prefix + "/(?P<word_1>\w+)/(?P<word_2>\w+)")

        list_re = re.compile("^%s$" % list_url)
        detail_re = re.compile("^%s$" % detail_url)

        for method in ('GET', 'POST', 'PUT', 'DELETE'):
            itty.REQUEST_MAPPINGS[method].append((list_re, list_url, cls.as_list()))
            itty.REQUEST_MAPPINGS[method].append((detail_re, detail_url, cls.as_detail()))

    def list(self):
        return {
            'hello': 'Welcome to LevenParty, a pseudo-port of Translation Party.',
            'help': "Send a GET request in the format /<word_1>/<word_2>/ (i.e. /hello/friend/).",
            'last_fifty_parties': LAST_FIFTY,
            'source_code': 'https://github.com/toastdriven/levenparty',
        }

    def detail(self, word_1, word_2):
        party = {
            'word_1': word_1,
            'word_2': word_2,
            'times_partied': 0,
            'steps': []
        }

        for count in range(MAX_PARTIES):
            party['times_partied'] += 1
            w1_len = len(word_1)
            w2_len = len(word_2)
            lev = levenshtein(word_1, word_2)
            data = {
                'word_1': word_1,
                'word_2': word_2,
                'lev': lev,
                'message': 'Matched'
            }

            if lev <= 0:
                # We're outta here!
                break
            elif w1_len == w2_len:
                # Pick a random letter & a random location.
                offset = random.randint(0, w2_len - 1)
                char = random.choice(LETTERS)
                attempt = word_2[:offset] + char + word_2[offset + 1:]

                if levenshtein(word_1, attempt) > lev:
                    data['message'] = 'Tried {0}, no luck'.format(attempt)
                else:
                    word_2 = attempt
                    data['message'] = 'Same lev distance'
            elif w1_len > w2_len:
                # Lengthen by one.
                word_2 = word_2 + random.choice(LETTERS)
                data['message'] = 'Lengthened word_2'
            else:
                # Shorten by one.
                word_2 = word_2[:-1]
                data['message'] = 'Shortened word_2'

            data['word_2'] = word_2
            party['steps'].append(data)

        # Store it.
        LAST_FIFTY.append(party)

        # If we have more than 50, kill off the oldest ones.
        while len(LAST_FIFTY) > 50:
            LAST_FIFTY.pop(0)

        return party


LevenPartyResource.setup_urls('')


if __name__ == '__main__':
    if DEBUG:
        itty.run_itty()
