from django import forms
from .models import Message, Visitor, Applicant


class StyledModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StyledModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.itervalues():
            field.widget.attrs['placeholder'] = field.label.capitalize()
            field.widget.attrs['required'] = ''


class MessageForm(StyledModelForm):

    name = forms.CharField(required=True, label='name')
    email = forms.EmailField(required=True, label='email')
    phone = forms.CharField(required=True, label='phone')

    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'subject', 'content']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Message'

    def save(self):
        instance = super(MessageForm, self).save()

        post_data = self.clean()
        v, _ = Visitor.objects.update_or_create(
            email=post_data['email'],
            defaults={'name': post_data['name']})

        instance.visitor = v
        instance.save()

        return instance


class ApplicantForm(StyledModelForm):

    class Meta:
        model = Applicant
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'address_1', 'address_2', 'city', 'state', 'country', 'zip_code',
                  'experiences', 'added_file_url']

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields['address_1'].widget.attrs['placeholder'] = 'Street Address'
        self.fields['address_2'].widget.attrs['placeholder'] = 'Address Line 2'
        self.fields['state'].widget.attrs['placeholder'] = 'State / Province / Region'
        self.fields['zip_code'].widget.attrs['placeholder'] = 'Postal / Zip Code'
        self.fields['country'].widget.attrs['data-validation'] = 'country'
        self.fields['added_file_url'].widget.attrs['style'] = 'display: none'
        del self.fields['address_2'].widget.attrs['required']
        del self.fields['experiences'].widget.attrs['required']
        del self.fields['added_file_url'].widget.attrs['required']
