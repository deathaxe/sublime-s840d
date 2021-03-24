from typing import Any, List
import sublime_plugin
import sublime


class Foo(sublime_plugin.ViewEventListener):
    def on_query_completions(self, prefix: str, locations: List[int]) -> Any:
        promise = sublime.CompletionList()
        sublime.set_timeout_async(
            lambda: sublime.set_timeout(
                lambda: promise.set_completions([], sublime.INHIBIT_WORD_COMPLETIONS)
            )
        )
        return promise
