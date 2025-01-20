from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile

class UserInfoForm(forms.ModelForm):
	full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Vardas Pavardė'}), required=True)
	phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telefono numeris'}), required=True)
	shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Elektroninis Paštas'}), required=True)
	address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Gatvė, namo nr.'}), required=True)
	address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Butas'}), required=False)
	city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miestas'}), required=True)
	zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pašto kodas'}), required=False)
	country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Šalis'}), required=True)

	class Meta:
		model = Profile
		fields = ['phone', 'address1', 'address2', 'city', 'zipcode', 'country', 'shipping_email']
		exclude = ['user']

class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = ('<ul class="form-text text-muted small">'
												  '<li>Jūsų slaptažodis negali būti per daug panašus į kitą jūsų asmeninę informaciją.</li>'
												  '<li>Jūsų slaptažodis turi būti sudarytas iš bent 8 simbolių.</li>'
												  '<li>Jūsų slaptažodis negali būti dažnai naudojamas slaptažodis.</li>'
												  '<li>Jūsų slaptažodis negali būti sudarytas vien tik iš skaičių.</li></ul>')

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Patvirtinti slaptažodį'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Įveskite tą patį slaptažodį kaip ir anksčiau</small></span>'

class UpdateUserForm(UserChangeForm):
	# hide password
	password = None

	email = forms.EmailField(label="",
							 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Elektroninis paštas'}), required=False)
	first_name = forms.CharField(label="", max_length=100,
								 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vardas'}))
	last_name = forms.CharField(label="", max_length=100,
								widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pavardė'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', )

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Vartotojas'
		self.fields['username'].label = ''
		self.fields[
			'username'].help_text = '<span class="form-text text-muted"><small>Ne daugiau kaip 150 simbolių. Galimos tik raidės, skaičiai ir @/./+/-/_ simboliai.</small></span>'


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Elektroninis paštas'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Vardas'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pavardė'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Vartotojas'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Ne daugiau kaip 150 simbolių. Galimos tik raidės, skaičiai ir @/./+/-/_ simboliai.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Slaptažodis'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = ('<ul class="form-text text-muted small">'
											  '<li>Jūsų slaptažodis negali būti per daug panašus į kitą jūsų asmeninę informaciją.</li>'
											  '<li>Jūsų slaptažodis turi būti sudarytas iš bent 8 simbolių.</li>'
											  '<li>Jūsų slaptažodis negali būti dažnai naudojamas slaptažodis.</li>'
											  '<li>Jūsų slaptažodis negali būti sudarytas vien tik iš skaičių.</li></ul>')

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Patvirtinti Slaptažodį'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Įveskite tą patį slaptažodį kaip ir anksčiau.</small></span>'

class PaymentForm(forms.Form):
	card_name =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Vardas Pavardė'}), required=True)
	card_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Korteles Numeris'}), required=True)
	card_exp_date =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Galiojimo Data'}), required=True)
	card_cvv_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Kodas'}), required=True)



