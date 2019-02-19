from __future__ import print_function
from __future__ import unicode_literals


class DictUtils(object):

    @classmethod
    def merge_dicts(cls, *dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """

        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result
