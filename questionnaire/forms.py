from django import forms
from .models import Response, Option

class TextBoxResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(TextBoxResponseForm, self).__init__(*args, **kwargs)
        self.fields['response'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write the response'})

    class Meta:
        model = Response
        fields = ['response']

class SingleChoiceResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(SingleChoiceResponseForm, self).__init__(*args, **kwargs)
        if question:
            self.options = Option.objects.filter(question=question)

    class Meta:
        model = Response
        fields = ['response']
        

class MultipleChoiceResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(MultipleChoiceResponseForm, self).__init__(*args, **kwargs)
        self.fields['response'].widget = forms.CheckboxSelectMultiple()
        self.fields['response'].choices = [(option.id, option.text) for option in Option.objects.filter(question=question)]

    class Meta:
        model = Response
        fields = ['response']

class LocationResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(LocationResponseForm, self).__init__(*args, **kwargs)
        self.fields['response'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'})

    class Meta:
        model = Response
        fields = ['response']
