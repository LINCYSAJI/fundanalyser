from django import forms 

from budget.models import Expense,Income

from django.contrib.auth.models import User

class ExpenseForm(forms.ModelForm):
    
    class Meta:
        
        model=Expense
        
        exclude=("id","created_date","user_object")
        
        
        widgets={
            
            "title":forms.TextInput(attrs={"class":"form-control"}),
            
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
            
            "category":forms.Select(attrs={"class":"form-control form-select"}),
            
            # "owner":forms.TextInput(attrs={"class":"form-control"}),
            
            "priority":forms.Select(attrs={"class":"form-control form-select"})
            
        }


class IncomeForm(forms.ModelForm):
    
    class Meta:
        
        model=Income
        
        exclude=("id","created_date","user_object")
        
        widgets={
            
            "title":forms.TextInput(attrs={"class":"form-control"}),
            
            "amount":forms.TextInput(attrs={"class":"form-control"}),
            
            "category":forms.Select(attrs={"class":"form-control form-select"}),
            
            # "owner":forms.TextInput(attrs={"class":"form-control"}),
        }
        
        
        
class RegistrationForm(forms.ModelForm):
    
    class Meta:
        
        model=User
        
        fields=["username","email","password"]
        
        widgets={
            
            "username":forms.TextInput(attrs={"class":"form-control"}),
            
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            
            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }
        
        
class LoginForm(forms.Form):#there is no create and update in login form so we use normal form
    
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    
class SummaryForm(forms.Form):
    
    start_date=forms.DateTimeField(widget=forms.DateInput(attrs={"class":"form-control mb-4","type":"date"}))

    end_date=forms.DateTimeField(widget=forms.DateInput(attrs={"class":"form-control mb-4","type":"date"}))
