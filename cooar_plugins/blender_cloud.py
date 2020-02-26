import requests
from jinja2 import Template
from mechanicalsoup import StatefulBrowser

from cooar.file import File
from cooar.plugin import CooarPlugin
from cooar.utilities import dl_utils, echo, types


class BlenderCloudPlugin(CooarPlugin):
    name = "blender_cloud"
    description = "A tutorial website for Blender, to determin what to download use 'course:<course-slug>', 'workshop:<workshop-slug>', 'film:<film-slug>' to download a course or workshop. To download files with this plugin, a blender clound subscription is required!"
    url = "https://cloud.blender.org/"
    author = "Christopher Schmitt <cooar@chris.yt>"
    supported_mediatypes = (types.MediaType.VIDEO,)
    supported_authtypes = (types.AuthType.COOKIES,)
    supported_qualities = {types.MediaType.VIDEO: ("1080p",)}
    template_strings = (
        "title",
        "duration",
        "author",
        "file_format",
        "project_name",
        "group_title",
    )
    default_template = "{{project_name}}/{{group_title}}/{{title}}.{{file_format}}"

    def prepare(self, **kwargs):
        self.browser = StatefulBrowser()
        self._mediatypes = kwargs.get("mediatypes")
        self._qualities = kwargs.get("qualities")
        self._templates = kwargs.get("templates")
        auth_package = kwargs.get("auth")
        if auth_package[0] == types.AuthType.COOKIES:
            jar = requests.cookies.RequestsCookieJar()
            session_values = auth_package[1]["session"]

            jar.set(
                "session",
                session_values["value"],
                domain=".cloud.blender.org",
                path="/",
            )

            self.browser.session.cookies = jar
            self.browser.open(
                "https://cloud.blender.org/settings/profile"
            ).status_code == 200
            profile_page = self.browser.get_current_page()
            try:
                assert profile_page.find(class_="py-1") is not None
            except AssertionError:
                echo.error_msg("Authentication was not successfull")
                exit(1)

            echo.debug_msg("Authentication successfull")

    def collect(self, part_id=None, **kwargs):
        PROJECT_TYPES = ("course", "workshop", "film")

        files = []
        if part_id is None:
            echo.error_msg("This plugin does not support downloading all files at once")
            exit(1)
        project_type, slug = part_id.split(":")
        if project_type in PROJECT_TYPES:
            url_tree = f"https://cloud.blender.org/p/{slug}/jstree"
        else:
            echo.error_msg("Invalid part_id")
            exit(1)
        self.browser.open(f"https://cloud.blender.org/p/{slug}")
        page = self.browser.get_current_page()
        self._project_name = (
            page.find(class_="nav-secondary")
            .find("a", class_="font-weight-bold")
            .string
        )
        resp = self.browser.open(url_tree)
        capter_tree = resp.json()

        for item in capter_tree["items"]:
            if item["type"] == "group":
                _, id_ = item["id"].split("n_")
                node_resp = self.browser.open(
                    f"https://cloud.blender.org/nodes/{id_}/jstree?children=1"
                )
                for child in node_resp.json()["children"]:
                    if (
                        child["type"] == "video"
                        and types.MediaType.VIDEO in self._mediatypes
                    ):
                        _, fid_ = child["id"].split("n_")
                        file = self._create_video_file(
                            f"https://cloud.blender.org/nodes/{fid_}"
                        )
                        files.append(file)
        return files

    def _create_video_file(self, url):
        self.browser.open(url + "/view")
        page = self.browser.get_current_page()

        title = page.find("h4").string.replace("", "")
        duration = page.find("li", title="Duration").string

        author = page.find(title="Author").get_text().strip()
        project_name = self._project_name
        group_title = self.browser.open(url + "/breadcrumbs").json()["breadcrumbs"][0][
            "name"
        ]

        links = page.find("li", class_="download").find_all("a")
        video_quality = self._qualities[types.MediaType.VIDEO]
        dl_urls = []
        for link in links:
            if (
                link.find(class_="size") is not None
                and link.find(class_="size").string == video_quality
            ):
                dl_urls.append(link)
        file_format = dl_urls[0].find(class_="format").string
        video_template = Template(self._templates[types.MediaType.VIDEO])
        file = File(
            url=dl_urls[0].get("href"),
            file_path_string=video_template.render(
                title=title,
                duration=duration,
                author=author,
                project_name=project_name,
                group_title=group_title,
                file_format=file_format,
            ),
        )
        echo.debug_msg(
            video_template.render(
                title=title,
                duration=duration,
                author=author,
                project_name=project_name,
                group_title=group_title,
                file_format=file_format,
            )
        )
        return file

    def download(self, file: File, **kwargs):
        dl_utils.download(self.browser.session, file)
