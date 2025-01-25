# Draw Error
class InvalidAlignParameter(Exception):
    def __init__(self, align:str):
        super().__init__(f'The align parameter {align} is not a valid align parameter.')

# Widgets Errors
class CreateWidgetTypeError(Exception):
    def __init__(self, widget_type:str):
        super().__init__(f'The widget type {widget_type} is not a valid widget type or cant can be found.')
        
class WidgetPassedError(Exception):
    def __init__(self, widget, quant:int):
        super().__init__(f'The widget {widget._type} passed out the widget limit! this is dangerous!\n\t- {quant} widgets in total')