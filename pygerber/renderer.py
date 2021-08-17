from abc import ABC, abstractmethod


class Renderer(ABC):

    @abstractmethod
    def select_aperture(self, spec):
        pass

    @abstractmethod
    def draw_line(self, spec):
        pass

    @abstractmethod
    def draw_arc(self, spec):
        pass