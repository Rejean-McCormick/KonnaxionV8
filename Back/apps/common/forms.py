from django import forms

class BaseForm(forms.ModelForm):
    """
    Base form to be extended by all ModelForms. Adds a common CSS class to each field.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # Apply a common CSS class to every field widget
            visible.field.widget.attrs.setdefault('class', 'form-control')
