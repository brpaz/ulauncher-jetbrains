"""
Parses the Jetbrains based IDEs recent projects list
"""

import os
import xml.etree.ElementTree as ET


class RecentProjectsParser:
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

        tree = ET.parse(file_path)
        root = tree.getroot()

        # pylint: disable=line-too-long
        recent_projects = root.findall('.//component[@name="RecentProjectsManager"][1]/option[@name="recentPaths"]/list/option') + root.findall(
            './/component[@name="RecentDirectoryProjectsManager"][1]/option[@name="recentPaths"]/list/option')

        result = []
        for project in recent_projects:
            project_path = project.attrib["value"].replace(
                '$USER_HOME$', os.path.expanduser('~'))
            project_name = os.path.basename(project_path)

            if query and query.lower() not in project_name.lower():
                continue

            result.append({
                'name': project_name,
                'path': project_path
            })

        return result[:8]
