"""
Ulauncher extension for opening recent projects on Jetbrains IDEs.
"""

import logging
import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from jetbrains import RecentProjectsParser

LOGGING = logging.getLogger(__name__)


class JetbrainsLauncherExtension(Extension):
    """ Main Extension Class  """

    def __init__(self):
        """ Initializes the extension """
        super(JetbrainsLauncherExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def get_recent_projects_file_path(self, keyword: str):
        """ Returns the file path where the recent projects are stored """
        ides = ['pstorm', 'webstorm', 'pycharm', 'intellij']
        switcher = {self.preferences.get(f"{ide}_keyword"): self.preferences.get(f"{ide}_projects_file") for ide in ides}
        print(switcher)
        return os.path.expanduser(switcher.get(keyword, ""))

    @staticmethod
    def get_icon(keyword):
        """ Returns the application icon based on the keyword """
        icon_path = os.path.join('images', "%s.png" % keyword)

        return icon_path

    def get_launcher_file(self, keyword):
        """ Returns the launcher file from preferences"""
        return os.path.expanduser(
            self.preferences.get("%s_launch_script" % keyword))


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """

    @staticmethod
    def on_event(event, extension):
        """ Handles the event """
        items = []

        keyword = event.get_keyword()
        query = event.get_argument() or ""
        file_path = extension.get_recent_projects_file_path(keyword)

        projects = RecentProjectsParser.parse(file_path, query)

        if not projects:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon=extension.get_icon(keyword),
                    name='No projects found',
                    on_enter=HideWindowAction()
                )
            ])

        for project in projects:

            items.append(ExtensionResultItem(
                icon=extension.get_icon(keyword),
                name=project['name'],
                description=project['path'],
                on_enter=RunScriptAction('%s "%s" &' % (
                    extension.get_launcher_file(keyword), project['path']), []),
                on_alt_enter=CopyToClipboardAction(project['path'])
            ))

        return RenderResultListAction(items)


if __name__ == '__main__':
    JetbrainsLauncherExtension().run()
