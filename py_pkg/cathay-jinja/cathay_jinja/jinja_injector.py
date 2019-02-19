from __future__ import print_function
from __future__ import unicode_literals

import logging
from jinja2 import Environment, BaseLoader, FileSystemLoader
from cathay_jinja.custom_filters import CUSTOM_FILTERS
from cathay_jinja.dict_utils import DictUtils

logger = logging.getLogger(__name__)


class JinjaInjector(object):

    @classmethod
    def set_filters(cls, jinja_env, filters=None):
        """
        :arg jinja_env: Environment of jinja instance
        """
        jinja_env.filters = DictUtils.merge_dicts(jinja_env.filters, filters)

        return jinja_env

    @classmethod
    def setup_jinja(cls, **kwargs):
        """
        Create Jinja core component instance
        """

        jinja_env = Environment(**kwargs)

        return cls.set_filters(jinja_env, filters=CUSTOM_FILTERS)

    @classmethod
    def string_render_args(cls, content, jinja_env=None, **kwargs):
        """
        Assign arguments render template string

        >>> JinjaInjector.string_render_args(content="A=> {{A}}",A='10')
        u'A=> 10'

        """

        if jinja_env is None or isinstance(jinja_env, Environment):
            logger.info("Generate new Environment of Jinja")
            jinja_env = cls.setup_jinja(loader=BaseLoader())

        return jinja_env.from_string(content).render(**kwargs)

    @classmethod
    def file_render_args(cls, path, jinja_env=None, **kwargs):
        """
        Assign arguments render template file
        calls example:
            JinjaInjector.file_render_args(path="/apps/conf/dev/job.conf",yyyymm=201803)
        """

        return cls.setup_jinja(loader=FileSystemLoader('/')).get_template(path).render(**kwargs)
