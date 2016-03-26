import Pyjo.UserAgent

import codecs
import sys

from Pyjo.Util import die

if sys.stdout.isatty():
    sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach() if hasattr(sys.stdout, 'detach') else sys.stdout, 'xmlcharrefreplace')
else:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach() if hasattr(sys.stdout, 'detach') else sys.stdout)

try:
    url = sys.argv[1]
except IndexError:
    raise Exception('get.py url opts')

opts = dict(map(lambda a: a.split('='), sys.argv[2:]))

tx = Pyjo.UserAgent.new(**opts).get(url)
err = tx.error
if err:
    if err['code']:
        die("{code} response: {message}".format(**err))
    else:
        die("Connection error: {message}".format(**err))
print(tx.res.text)
