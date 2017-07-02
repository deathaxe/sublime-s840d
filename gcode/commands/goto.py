# -*- encoding: utf-8 -*-
from ... import lib
from .. import codeintel
from . import base


class S840dGotoDefinitionCommand(base.TextCommand):
    """Custom goto definition command to be used within S840D G-Code.

    Sublime Text's goto_definition requires a symbol to be located in the index
    to find its location. Therefore it does not work with Sublime Text's local
    symbol definitions or the "hidden symbol definitions" this package uses to
    handle local argument/label/macro/variable declarations/definitions.

    This is the only way to make goto definition work for local variable
    definitions without polluting the global index right now.
    """

    def run(self, edit, point=None):
        """Goto local definition or run default "goto_definition" command."""
        view = self.view
        if point is None:
            selections = view.sel()
            if selections:
                point = selections[0].begin()
        if point:
            word = view.substr(view.word(point))
            region = codeintel.symbols.find_definition(view, point, word)
            if region:
                # local definition was found
                lib.view.goto_point(view, region.begin())
                return
        # run sublime text default command
        view.run_command("goto_definitinon")
