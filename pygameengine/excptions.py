# Widgets Errors
class CreateWidgetTypeError(Exception):
    def __init__(self, widget_type:str):
        super().__init__(f'The widget type {widget_type} is not a valid widget type or cant can be found.')