from ._anvil_designer import startupTemplate

README = (
    "See this project's [README](https://github.com/anvilistas/media-manager) "
    "for usage instructions."
)


class startup(startupTemplate):
    def __init__(self, **properties):
        self.rich_text_1.content = README
        self.init_components(**properties)
