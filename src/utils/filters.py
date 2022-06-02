class DescriptionFilter:
    @property
    def short_description(self):
        raise NotImplementedError


class ImageFilter:
    @property
    def show_display(self):
        raise NotImplementedError

    @property
    def show_field(self):
        raise NotImplementedError