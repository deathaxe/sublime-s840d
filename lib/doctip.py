import sublime
import sublime_plugin


class S840dShowDocPopupCommand(sublime_plugin.ApplicationCommand):

    template = """
        <html>
        <style>
        h1 {{
            font-size: 1.1rem;
        }}
        </style>
        {}
        </html>
    """


    def run(self, href):
        try:
            path = "Packages/CNC Sinumerik 840D/hmi/doc/{}.html".format(href)
            print("Loading", path)
            html = self.template.format(sublime.load_resource(path))
        except FileNotFoundError:
            html = "<html>No documentation available.</html>"

        sublime.active_window().active_view().show_popup(
            content=html,
            flags=sublime.COOPERATE_WITH_AUTO_COMPLETE|sublime.HIDE_ON_MOUSE_MOVE_AWAY
        )
