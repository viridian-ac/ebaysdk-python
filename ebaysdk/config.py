# -*- coding: utf-8 -*-

import os
import inspect
import sys

from ebaysdk import log
# from ebaysdk.exception import ConnectionConfigError
from ebaysdk.utils import parse_yaml

sys.path.append('/Applications/XAMPP/xamppfiles/htdocs/')
from paiuva.sdk import VAClassHelper as vach
from paiuva.sdk import VAGetSet as vags
from paiuva.sdk import VAEbayError as ee


class Config(object):

    def __init__(self, domain, connection_kwargs=dict(), config_file='ebay.yaml'):
        vach.Help.curr_callers()

        self.config_file = config_file
        self.domain = domain
        self.values = dict()
        self.config_file_used = []
        self.connection_kwargs: dict = connection_kwargs
        self._populate_yaml_defaults()
        # print(self.config_file_used)

    def _populate_yaml_defaults(self):
        "Returns a dictionary of YAML defaults."
        vach.Help.curr_callers()
        # check for absolute path
        if self.config_file and os.path.exists(self.config_file):
            self.config_file_used = self.config_file

            dataobj = parse_yaml(self.config_file)

            for key, val in dataobj.get(self.domain, {}).items():
                self.set(key, val)

            return self

        # check other directories
        dirs: list = ['.','..', os.path.expanduser('~'), '/etc']
        for mydir in dirs:
            # print(mydir)
            myfile = "%s/%s" % (mydir, self.config_file)
            # print(myfile)

            if os.path.exists(myfile):
                print(myfile)
                self.config_file_used = myfile

                dataobj = parse_yaml(myfile)

                for k, val in dataobj.get(self.domain, {}).items():
                    self.set(k, val)

                return self

        if self.config_file:
            raise ee.ConnectionConfigError(
                'config file %s not found. Set config_file=None for use without YAML config.' % self.config_file)

    def file(self):
        return self.config_file_used


    def get(self, cKey, defaultValue=None):
        # log.debug('get: %s=%s' % (cKey, self.values.get(cKey, defaultValue)))
        return self.values.get(cKey, defaultValue)


    def set(self, cKey, defaultValue, force=False):
        vags.GetSet.set(cKey, self.values, self.connection_kwargs, defaultValue, force, False)
        """
        if force:
            # log.debug('set (force): %s=%s' % (cKey, defaultValue))
            self.values.update({cKey: defaultValue})

        elif cKey in self.connection_kwargs and self.connection_kwargs[cKey] is not None:
            # log.debug('set: %s=%s' % (cKey, self.connection_kwargs[cKey]))
            self.values.update({cKey: self.connection_kwargs[cKey]})

        # otherwise, use yaml default and then fall back to
        # the default set in the __init__()
        else:
            if cKey not in self.values:
                # log.debug('set: %s=%s' % (cKey, defaultValue))
                self.values.update({cKey: defaultValue})
            else:
                pass
        """


if __name__ == "__main__":
    ...

    c = Config(domain='api.ebay.com')

    c.set('fname', 'dr.jo')
    print(c.get('fname'))


    k=c.get('missingkey', 'dexfaultvalue')
    print(k)  # 'dexfaultvalue'

    print(c.values)
