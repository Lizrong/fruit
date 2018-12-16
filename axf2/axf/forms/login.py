from django import forms

class LoginForm(forms.Form):
    logname = forms.CharField(max_length=12, required=True,error_messages={"required":'用户账号不能为空', 'invalid':'格式错误'})
    logpwd   = forms.CharField(max_length=16, widget=forms.PasswordInput)




