import sublime_plugin, sublime
import os

class ToolTipCommand(sublime_plugin.EventListener):

  cur_word = None
  tip_html = None

  def on_selection_modified(self, view):
    self.run(view, 'selection_modified')

  def run(self, view, where):
    # return if no s840d source code
    scope = view.scope_name(view.sel()[0].b)
    print(scope)
