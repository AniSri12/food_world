from django import forms

class LoginForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	password = forms.CharField()


class RegisterForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.CharField()
	password = forms.CharField()
	phone_number = forms.CharField()


class CreateSnackForm(forms.Form):
	name = forms.CharField()
	price = forms.CharField()
	country = forms.CharField()
	description = forms.CharField()
	nutricional_info = forms.DecimalField(max_digits=6, decimal_places=2)


