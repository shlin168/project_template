from __future__ import print_function
from __future__ import unicode_literals

import shelve


class Persistence(object):

    path = "var/snapshot/snapshot"

    @classmethod
    def save(cls, key, value):
        file = None
        try:
            file = shelve.open(cls.path, flag='c', protocol=2, writeback=False)
            file[str(key)] = value
        finally:
            if file is not None:
                file.close()

    @classmethod
    def load(cls, key):
        file = None
        try:
            file = shelve.open(cls.path)
            return file[str(key)]
        except KeyError:
            return None
        finally:
            if file is not None:
                file.close()

        return None
