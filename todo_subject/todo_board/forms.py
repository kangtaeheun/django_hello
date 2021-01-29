from django import forms
from .models import TodoList

# date input type을 date로 설정 --> 달력 뜨게함.
class DateInput(forms.DateInput):
    input_type = 'date'

class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ('title', 'content', 'end_date')
        widgets = {
            # end_date ==> dateInput 클래스 불러옴.
            'end_date' : DateInput()
        }
