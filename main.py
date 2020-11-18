"""
Ulauncher extension for opening recent projects on Jetbrains IDEs.
"""
import os

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.event import KeywordQueryEvent
from jetbrains.project_parser import RecentProjectsParser


class JetbrainsLauncherExtension(Extension):
    """ Main Extension Class  """
    def __init__(self):
        """ Initializes the extension """
        super(JetbrainsLauncherExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def find_in_preferences(self, preference_part, keyword):
        """ Return the value of the preference for the specific IDE """
        preference = None
        for ide in [
                'pstorm', 'webstorm', 'pycharm', 'idea', 'goland', 'clion',
                'rider', 'rubymine', 'studio'
        ]:
            if keyword == self.preferences.get('%s_keyword' % ide):
                preference = self.preferences.get(ide + preference_part)
        return preference

    def get_recent_projects_file_path(self, keyword):
        """ Returns the file path where the recent projects are stored """
        path = self.find_in_preferences('_projects_file', keyword)
        if path:
            return os.path.expanduser(path)
        raise AttributeError("Cant find IDE Path")

    def get_icon(self, keyword):
        """ Returns the application icon based on the keyword """
        icon_path = None
        for ide in [
                'pstorm', 'webstorm', 'pycharm', 'idea', 'goland', 'clion',
                'rider', 'rubymine', 'studio'
        ]:
            if keyword == self.preferences.get('%s_keyword' % ide):
                icon_path = os.path.join('images', "%s.png" % ide)
        return icon_path

    def get_launcher_file(self, keyword):
        """ Returns the launcher file from preferences"""
        script = self.find_in_preferences('_launch_script', keyword)
        return os.path.expanduser(script)


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """

    # pylint: disable=unused-argument,no-self-use
    def on_event(self, event, extension):
        """ Handles the event """
        items = []
        keyword = event.get_keyword()
        query = event.get_argument() or ""
        file_path = extension.get_recent_projects_file_path(keyword)

        projects = RecentProjectsParser.parse(file_path, query)

        if not projects:
            return RenderResultListAction([
                ExtensionResultItem(icon=extension.get_icon(keyword),
                                    name='No projects found',
                                    on_enter=HideWindowAction())
            ])
        for project in projects:
            items.append(
                ExtensionResultItem(
                    icon=project['icon'] if project['icon'] is not None else
                    extension.get_icon(keyword),
                    name=project['name'],
                    description=project['path'],
                    on_enter=RunScriptAction(
                        '%s "%s" &' % (extension.get_launcher_file(keyword),
                                       project['path']), []),
                    on_alt_enter=CopyToClipboardAction(project['path'])))
        return RenderResultListAction(items)


if __name__ == '__main__':
    JetbrainsLauncherExtension().run()
