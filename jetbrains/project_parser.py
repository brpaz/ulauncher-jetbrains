"""
Parses the Jetbrains based IDEs recent projects list
"""

import glob
import os
import xml.etree.ElementTree as ET


class RecentProjectsParser():
    """ Processes the "Recent projects" file from Jetbrains IDEs """
    @staticmethod
    def parse(file_path, query):
        """
        Parses the recent projects file passed as argument and returns a list of projects
        @param str file_path The path to the file which holds the recent open projects by the IDE
        @param str query Optional search query to filter the results
        """
        if not os.path.isfile(file_path):
            return []

        root = ET.parse(file_path).getroot()

        # pylint: disable=line-too-long
        recent_projects = root.findall(
            './/component[@name="RecentProjectsManager"][1]/option[@name="recentPaths"]/list/option'
        ) + root.findall(
            './/component[@name="RecentDirectoryProjectsManager"][1]/option[@name="recentPaths"]/list/option'
        )

        attr = "value"
        if (recent_projects.__len__() == 0):
            recent_projects = root.findall(
                './/component[@name="RecentProjectsManager"][1]/option[@name="additionalInfo"]/map/entry'
            )
            attr = "key"

        result = []
        for project in recent_projects:
            project_path = project.attrib[attr].replace(
                '$USER_HOME$', os.path.expanduser('~'))
            project_name = os.path.basename(project_path)
            icons = glob.glob(os.path.join(project_path, '.idea', 'icon.*'))

            if query and query.lower() not in project_name.lower():
                continue

            result.append({
                'name': project_name,
                'path': project_path,
                'icon': icons[0] if len(icons) > 0 else None
            })

        return result[:8]