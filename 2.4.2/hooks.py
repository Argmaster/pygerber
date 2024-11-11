import logging
from typing import Iterable
import mkdocs.plugins
from mkdocs.structure.nav import Navigation
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Section
from mkdocs.structure import StructureItem

log = logging.getLogger("mkdocs")


@mkdocs.plugins.event_priority(-100)
def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
    NavWalker(nav.items).walk()


class NavWalker:
    def __init__(self, nav: Iterable[StructureItem]):
        self.nav = nav

    def walk(self):
        self._walk(self.nav)

    def _walk(self, nav: Iterable[StructureItem]):
        for item in nav:
            if isinstance(item, Page):
                self.on_page(item)
            if isinstance(item, Section):
                self.on_section(item)

    def on_page(self, page: Page):
        pass

    def on_section(self, section: Section):
        if section.title.casefold() == "reference".casefold():
            return

        self._walk(section.children)
        section.title = section.title.lstrip("1234567890").strip().capitalize()
