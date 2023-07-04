import sublime
import sublime_plugin


class FoldUseCommand(sublime_plugin.TextCommand):
    def run(self, edit, args=None):
        if isNotPhpFile(self.view):
            return

        self.view.fold(self.get_imports_use_region())

        if (config('fold_traits_use')):
            self.view.fold(self.get_traits_use_region())

    def get_imports_use_region(self):
        regions = self.view.find_all("^use .*;$", 0)

        if len(regions) == 0:
            return []

        return shift_region(regions_to_region(regions), len("use "))

    def get_traits_use_region(self):
        regions = self.view.find_all("^(\t|\s{4})use .*;$", 0)

        if len(regions) == 0:
            return []

        return shift_region(regions_to_region(regions), len('    use '))


class FoldUseEventListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        if isNotPhpFile(view):
            return

        view.run_command("fold_use")

    def on_load(self, view):
        if isNotPhpFile(view):
            return

        view.run_command("fold_use")


def isNotPhpFile(view):
    return "PHP" != view.syntax().name


def shift_region(region, times):
    return sublime.Region(region.a + times, region.b)


def regions_to_region(regions):
    if len(regions) == 0:
        return False

    return regions[0].cover(regions[-1])


def config(key):
    return sublime.load_settings("FoldUse.sublime-settings").get(key)
