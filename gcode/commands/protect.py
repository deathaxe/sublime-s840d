# -*- encoding: utf-8 -*-
import os
import re
import shutil
import subprocess
import tempfile

import sublime
import sublime_plugin

# check if protector exists in PATH
_HAVE_PROTECTOR = bool(shutil.which('protector.exe'))


class S840dProtectCommand(sublime_plugin.WindowCommand):
    """Shrink code code as small as possible and convert to cpf.

    Remove all comments and block numbers as well as all unrequired
    whitespaces to create as small as possible encrypted cycle.
    """
    PANEL_SETTINGS = {
        "auto_indent": False,
        "detect_indentation": False,
        "fold_buttons": False,
        "gutter": False,
        "is_widget": True,
        "mini_diff": False,
        "syntax": "s840d_gcode.sublime-syntax",
        "translate_tabs_to_spaces": False,
        "word_wrap": False,
    }

    def is_enabled(self):
        """Enable command for G-Code if protector.exe exists."""
        return _HAVE_PROTECTOR

    def run(self, paths=None):
        """API entry point to run 's840d_protect' command.

        Arguments:
            edit (Edit): The current edit token which groups this operation
        """
        if not paths:
            paths = [self.window.extract_variables()['file']]
            if not paths:
                return

        try:
            # Temporary file to use for protector
            temp_name = tempfile.mktemp(suffix='.spf')
            # Create temporary output panel and use it to run the minify command.
            panel = self.window.create_output_panel('s840d_protector', unlisted=True)
            for key, value in self.PANEL_SETTINGS.items():
                panel.settings().set(key, value)
            # Protect all files
            for file_name in paths:
                if os.path.isfile(file_name):
                    self._protect(panel, file_name, temp_name)
        finally:
            self.window.destroy_output_panel('s840d_protector')
            try:
                os.unlink(temp_name)
            except:
                pass

    def _protect(self, panel, file_name, temp_name):
        source = ''
        try:
            print("Encrypting", file_name)
            with open(file_name, encoding='utf-8') as file:
                source = file.read()
            # strip ARC headers
            source = re.sub(r'^\s*(?:%_N_|;\$PATH=).*$', '', source, flags=re.MULTILINE)
            panel.run_command("insert", {"characters": source})
            panel.run_command("s840d_minify")
            source = panel.substr(sublime.Region(0, panel.size()))
            with open(temp_name, 'w', encoding='utf-8') as file:
                file.write(source)
            self._protector(temp_name)
            # move protected file next to source file
            shutil.move(os.path.splitext(temp_name)[0] + '.CPF',
                        os.path.splitext(file_name)[0] + '.CPF')
        except Exception as error:
            print('  -> Error!  ({})'.format(error))

    @staticmethod
    def _protector(filename):
        try:
            # protect temporary file
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            out = subprocess.check_output(
                args=['protector.exe', filename],
                stderr=subprocess.STDOUT,
                startupinfo=startupinfo)
            if out:
                print(out.decode().replace('\r', ''))
        except subprocess.CalledProcessError as error:
            print('S840D: protector failed with error', error.returncode)
        except FileNotFoundError:
            print('S840D: Can\'t encrypt cycle, protector.exe was not found!')
