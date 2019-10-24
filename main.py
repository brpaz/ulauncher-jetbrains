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

    @staticmethod
    def get_recent_projects_file_path(keyword: str, projects_file_switcher):
        """ Returns the file path where the recent projects are stored """
        logging.info(f"keyword {keyword}")
        return os.path.expanduser(projects_file_switcher.get(keyword, ""))

    @staticmethod
    def get_icon(image_file):
        """ Returns the application icon based on the keyword """
        icon_path = os.path.join('images', image_file)

        return icon_path

    @staticmethod
    def get_launcher_file(keyword, launch_script_switcher):
        """ Returns the launcher file from preferences"""
        return os.path.expanduser(launch_script_switcher.get(keyword))


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """

    def on_event(self, event, extension):
        preferences = extension.preferences
        ides = ['pstorm', 'webstorm', 'pycharm', 'intellij']
        projects_file_switcher = {
            preferences.get(f"{ide}_keyword"): preferences.get(f"{ide}_projects_file") for ide in ides}
        launch_script_switcher = {
            preferences.get(f"{ide}_keyword"): preferences.get(f"{ide}_launch_script") for ide in ides}
        icon_switcher = {preferences.get(f"{ide}_keyword"): f"{ide}.png" for ide in ides}

        logging.info(f"launch script: {launch_script_switcher}")
        logging.info(f"projects files: {projects_file_switcher}")

        """ Handles the event """
        items = []
        logging.info(f"preferences {extension.preferences}")
        keyword = event.get_keyword()
        logging.info(f"keyword: {keyword}")
        query = event.get_argument() or ""
        file_path = extension.get_recent_projects_file_path(keyword, projects_file_switcher)

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
                icon=extension.get_icon(icon_switcher[keyword]),
                name=project['name'],
                description=project['path'],
                on_enter=RunScriptAction('%s "%s" &' % (
                    extension.get_launcher_file(keyword, launch_script_switcher), project['path']), []),
                on_alt_enter=CopyToClipboardAction(project['path'])
            ))

        return RenderResultListAction(items)


if __name__ == '__main__':
    JetbrainsLauncherExtension().run()
