import sublime
import os


def plugin_loaded():
    """Initiate language specific settings after all plugins are loaded."""
    init_default_settings("s840d_arc")
    init_default_settings("s840d_gcode")
    init_default_settings("s840d_hmi")


def init_default_settings(syntax):
    """Initiate essential language specific settings.

    There are some setting, which are essensial to make G-Code files
    work correctly on a CNC later. If no language specific settings
    file exists, create one with those settings.
    """
    file_name = syntax + ".sublime-settings"
    file_path = os.path.join(sublime.packages_path(), "User", file_name)
    if not os.path.exists(file_path):

        settings = sublime.load_settings(file_name)

        # UTF8 encoding not supported
        settings.set("default_encoding", "ASCII")
        settings.set("fallback_encoding", "Western (Windows 1252)")

        # avoid tab stops end ensure newline at eof
        settings.set("ensure_newline_at_eof_on_save", True)
        settings.set("translate_tabs_to_spaces", True)
        settings.set("use_tab_stops", True)

        # Define the format of binary numbers for the Hex-Bin-System plugin
        # Binaries look like 'B101110'
        settings.set("convert_src_bin", "'B([01]+)'")
        settings.set("convert_dst_bin", "'B{0:b}'")

        # Define the format of hexadecimal numbers for Hex-Bin-System plugin
        # Hexadecimals look like 'H1AF23'
        settings.set("convert_src_hex", "'H([0-9A-F]+)'")
        settings.set("convert_dst_hex", "'H{0:X}'")

        # Define the format of exponential numbers for Hex-Bin-System plugin
        # The pattern must match the base as group 1 and exponent as group 2.
        # Exponential numbers look like 3.14EX-4
        settings.set("convert_src_exp", "\\b([1-9]\\.\\d+)EX([-+]?\\d+)\\b")
        settings.set("convert_dst_exp", "EX")

        sublime.save_settings(file_name)
