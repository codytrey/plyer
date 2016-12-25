from subprocess import Popen, PIPE
from plyer.facades import UniqueID
from plyer.utils import whereis_exe

from os import environ


class FreeBSDUniqueID(UniqueID):
    def _get_uid(self):
        old_lang = environ.get('LANG')
        environ['LANG'] = 'C'
        dmidecode_process = Popen(["dmidecode", "-quiet"], stdout=PIPE, stderr=PIPE)
        grep_process = Popen(["grep", "-m1", "serial:"],
                             stdin=dmidecode_process.stdout, stdout=PIPE)
        dmidecode_process.stdout.close()
        output = grep_process.communicate()[0]
        environ['LANG'] = old_lang

        if output:
            return output.split()[1]
        else:
            return None


def instance():
    import sys
    if whereis_exe('dmidecode'):
        return FreeBSDUniqueID()
    sys.stderr.write("dmidecode not found.")
    return UniqueID()
