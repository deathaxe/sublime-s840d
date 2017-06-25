# -*- encoding: utf-8 -*-
import locale

import sublime
import sublime_plugin

from .. import doc
from .. import lib

SELECTOR = 'source.s840d_hmi & support.variable.nck'


class S840DHmiEvents(sublime_plugin.EventListener):

    def on_hover(self, view, point, hover_zone):
        """Handle the hover event and show tooltip if needed."""
        if hover_zone != sublime.HOVER_TEXT:
            return
        if not view.match_selector(point, SELECTOR):
            return
        word = view.substr(view.word(point))
        # load current OS display language (e.g.: de_DE)
        lang = locale.getdefaultlocale()[0][:2].lower()
        content = doc.database.tooltip(view, word, lang)
        if not content:
            return
        window_width = min(1000, int(view.viewport_extent()[0]) - 64)
        view.show_popup(
            content=lib.html.POPUP_TEMPLATE.format(content),
            location=point,
            max_width=window_width,
            flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY)
