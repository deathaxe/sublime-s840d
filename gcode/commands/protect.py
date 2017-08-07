# -*- encoding: utf-8 -*-
import os
import re
import shutil
import subprocess
import tempfile

import sublime

from . import base
from . import minify

# check if protector exists in PATH
_HAVE_PROTECTOR = bool(shutil.which('protector'))


class S840dProtectCommand(base.TextCommand):
    """Shrink code code as small as possible and convert to cpf.

    Remove all comments and block numbers as well as all unrequired
    whitespaces to create as small as possible encrypted cycle.
    """

    def is_enabled(self):
        """Enable command for G-Code if protector.exe exists."""
        return _HAVE_PROTECTOR and super().is_enabled()

    def run(self, edit):
        """API entry point to run 's840d_protect' command.

        Arguments:
            edit (Edit): The current edit token which groups this operation
        """
        sublime.set_timeout_async(self._run_async)

    def _run_async(self):

        # check if view is saved to disk
        file_name = self.view.file_name()
        if not file_name or not os.path.isfile(file_name):
            return sublime.error_message(
                "Please save the cycle to disk first.")
        # save view to disk to sync timestamp
        self.view.run_command("save")
        # minimize and encode content
        region = sublime.Region(0, self.view.size())
        source = self.view.substr(region)
        source = minify.minify_code(source)
        # strip ARC headers and comments except VERSION
        source = re.sub(r'\s*(?:%_N_|;\s*(?!VERSION|DATE)).*$', '',
                        source, flags=re.MULTILINE)
        source = source.replace('\n\n', '\n')
        source = source.encode()
        # save to temporary file and run protector
        try:
            file, temp_name = tempfile.mkstemp(suffix='.spf')
            os.write(file, source)
            os.close(file)
            self._protector(temp_name)
            # move protected file next to source file
            shutil.move(os.path.splitext(temp_name)[0] + '.cpf',
                        os.path.splitext(file_name)[0] + '.cpf')
        except:
            print('S840D: Program not encrypted!')
        finally:
            try:
                os.unlink(temp_name)
            except:
                pass

    @staticmethod
    def _protector(filename):
        try:
            # protect temporary file
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            out = subprocess.check_output(
                args=['protector', filename],
                stderr=subprocess.STDOUT,
                startupinfo=startupinfo)
            if out:
                print(out.decode().replace('\r', ''))
        except subprocess.CalledProcessError as error:
            print('S840D: protector failed with error', error.returncode)
        except FileNotFoundError:
            print('S840D: Can\'t encrypt cycle, protector.exe was not found!')
