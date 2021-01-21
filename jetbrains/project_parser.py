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

        recent_projects_paths_node = root.find('.//component[@name="RecentProjectsManager"][1]/option[@name="recentPaths"]')
        recent_directory_projects_paths_node = root.find('.//component[@name="RecentDirectoryProjectsManager"][1]/option[@name="recentPaths"]')

        if recent_projects_paths_node is None and recent_directory_projects_paths_node is None:
            recent_projects = root.findall(
                './/component[@name="RecentProjectsManager"][1]/option[@name="additionalInfo"]/map/entry'
            ) + root.findall(
                './/component[@name="RecentDirectoryProjectsManager"][1]/option[@name="additionalInfo"]/map/entry'
            )

            recent_project_paths = [ project.attrib["key"] for project in recent_projects ]
        else:
            recent_projects = root.findall(
                './/component[@name="RecentProjectsManager"][1]/option[@name="recentPaths"]/list/option'
            ) + root.findall(
                './/component[@name="RecentDirectoryProjectsManager"][1]/option[@name="recentPaths"]/list/option'
            )

            recent_project_paths = [ project.attrib["value"] for project in recent_projects ]

        result = []

        for recent_project_path in recent_project_paths:
            project_title = ''
            project_path = recent_project_path.replace(
                '$USER_HOME$', os.path.expanduser('~'))
            name_file = project_path + '/.idea/.name'

            if os.path.exists(name_file):
                with open(name_file, 'r') as file:
                    project_title = file.read().replace('\n', '')

            project_name = os.path.basename(project_path)
            icons = glob.glob(os.path.join(project_path, '.idea', 'icon.*'))

            if query and query.lower() not in project_name.lower(
            ) and query.lower() not in project_title.lower():
                continue

            result.append({
                'name': project_title or project_name,
                'path': project_path,
                'icon': icons[0] if len(icons) > 0 else None
            })

        return result[:8]
