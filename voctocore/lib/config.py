import os.path
import logging
from configparser import DuplicateSectionError
from lib.args import Args
from vocto.config import VocConfigParser

__all__ = ['Config']

Config = None


class VoctocoreConfigParser(VocConfigParser):

    def add_section_if_missing(self, section):
        try:
            self.add_section(section)
        except DuplicateSectionError:
            pass


def load():
    global Config
    files = [
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     '../default-config.ini'),
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     '../config.ini'),
        '/etc/voctomix/voctocore.ini',
        '/etc/voctomix.ini',  # deprecated
        '/etc/voctocore.ini',
        os.path.expanduser('~/.voctomix.ini'),  # deprecated
        os.path.expanduser('~/.voctocore.ini'),
    ]

    if Args.ini_file is not None:
        files.append(Args.ini_file)

    Config = VoctocoreConfigParser()
    readfiles = Config.read(files)

    log = logging.getLogger('ConfigParser')
    log.debug('considered config-files: \n%s',
              "\n".join([
                  "\t\t" + os.path.normpath(file)
                  for file in files
              ]))
    log.debug('successfully parsed config-files: \n%s',
              "\n".join([
                  "\t\t" + os.path.normpath(file)
                  for file in readfiles
              ]))

    if Args.ini_file is not None and Args.ini_file not in readfiles:
        raise RuntimeError('explicitly requested config-file "{}" '
                           'could not be read'.format(Args.ini_file))
