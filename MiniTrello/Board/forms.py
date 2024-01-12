from django import forms
from . import models


class BoardForm(forms.ModelForm):
    class Meta:
        model = models.Board
        exclude = ("owner",)


class CardForm(forms.ModelForm):
    class Meta:
        model = models.Card
        fields = "__all__"


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        fields = "__all__"
        exclude = ("card_limit",)


class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = "__all__"
