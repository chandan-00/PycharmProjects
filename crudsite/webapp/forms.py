from django import forms


class EmployeeList(forms.Form):
    name = forms.CharField(label="Name", max_length=300)


# class

