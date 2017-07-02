# -*- encoding: utf-8 -*-


def goto_point(view, point):
    if view.window():
        view.window().focus_view(view)
    view.sel().clear()
    if not view.visible_region().contains(point):
        view.show_at_center(point)
    view.sel().add(point)
