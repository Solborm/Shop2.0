from django import forms
from django.utils import timezone
from django.contrib.auth.models import User



class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email'
		]


	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'
		self.fields['password'].help_text = 'Придумайте пароль'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['email'].label = 'Ваша почта'
		self.fields['email'].help_text = 'Пожалуйста указывайте реальный Адрес'
		self.fields['password_check'].label	 = 'Повторите пароль'


	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Пользователь с таким логином уже зарегистрирован')
		if password != password_check:
			raise forms.ValidationError('Пароли не совпадают')




class OrderForm(forms.Form):
	
	name = forms.CharField()
	last_name =  forms.CharField(required=False)
	phone = forms.CharField()
	buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Самовывоз"), ("delivery", "Доставка")]))
	date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
	address = forms.CharField(required=False)
	comments = forms.CharField(widget=forms.Textarea, required=False)


	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['phone'].label = 'Контактный телефон'
		self.fields['phone'].help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с вами можно связаться'
		self.fields['buying_type'].label = 'Способ получения'
		self.fields['address'].label = 'Адресс доставки'
		self.fields['address'].help_text = '*обязательно указывайте город'
		self.fields['comments'].label = 'Комментарии к заказу'
		self.fields['date'].label = 'Дата доставки'
		self.fields['date'].help_text = 'Доставка производится на следующий день после оформления заказа. Менеджер с вами свяжется'


