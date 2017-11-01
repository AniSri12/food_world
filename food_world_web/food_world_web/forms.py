from django import forms

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget = forms.PasswordInput)



class RegisterForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget = forms.PasswordInput)
	phone_number = forms.CharField()


class CreateSnackForm(forms.Form):
	name = forms.CharField()
	nutricional_info = forms.CharField()
	country = forms.CharField()
	description = forms.CharField()
	price = forms.DecimalField(max_digits=6, decimal_places=2)


