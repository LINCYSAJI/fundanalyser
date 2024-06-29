from django.shortcuts import render,redirect

from django.views.generic import View

from budget.forms import ExpenseForm,IncomeForm,RegistrationForm,LoginForm,SummaryForm

from budget.models import Expense,Income

from django.contrib import messages

from  django.utils import timezone

from django.db.models import Sum

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator

from budget.decorators import Signin_required

import datetime

# Create your views here.

# function decorator==>method decorator


@method_decorator(Signin_required,name="dispatch")
class ExpenseCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        if not request.user.is_authenticated:
            
            messages.error(request,"invalid session please login")
            
            return redirect("signin")
        
        form_instance=ExpenseForm()
        
        # qs=Expense.objects.all() # to fetch all expenses
        
        qs=Expense.objects.filter(user_object=request.user) #to fetch all expenses of login user
        
        return render(request,"expense_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):
        
        form_instance=ExpenseForm(request.POST) #create
        
        if form_instance.is_valid():
            
            # add user_object to form instance
            
            form_instance.instance.user_object=request.user
        
            form_instance.save()
            
            
            messages.success(request,"Expense added successfully")
        
            return redirect("expense-add")
        
        else:
            
            messages.error(request,"failed to add expense")
            
            return render(request,"expense_add.html",{"form":form_instance})

@method_decorator(Signin_required,name="dispatch")
class ExpenseUpdateView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        expense_object=Expense.objects.get(id=id)
        
        form_instance=ExpenseForm(instance=expense_object)
        
        return render(request,"expense_edit.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        expense_object=Expense.objects.get(id=id)
        
        form_instance=ExpenseForm(instance=expense_object,data=request.POST)#update/ if form_instance contain instance then it perform update function
        
        if form_instance.is_valid():
            
            form_instance.save()

            messages.success(request,"expense changed")

            return redirect("expense-add")
        else:
            messages.error(request,"failed to update")

            return render(request,"expense_edit.html",{"form":form_instance})
    
@method_decorator(Signin_required,name="dispatch")
class ExpenseDetailView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        qs=Expense.objects.get(id=id)
        
        return render(request,"expense_detail.html",{"data":qs})
    
@method_decorator(Signin_required,name="dispatch")
class ExpenseDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Expense.objects.get(id=id).delete()
        
        messages.success(request,"successfully deleted")
        
        return redirect("expense-add")
    
@method_decorator(Signin_required,name="dispatch")
class ExpenseSummaryView(View):
    
    def get(self,request,*args, **kwargs):
        
        current_month=timezone.now().month
        
        current_year=timezone.now().year
        
        expense_list=Expense.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)
        
        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))
        
        print(expense_total)
        
        category_summary=expense_list.values("category").annotate(total=Sum("amount"))
        
        print("cat summary",category_summary)
        
        priority_summary=expense_list.values("priority").annotate(total=Sum("amount"))
        
        print("priority summary",priority_summary)
        
        data={
              "expense_total":expense_total,
              
              "category_summary":category_summary,
              
              "priority_summary":priority_summary,
              
              }

        return render(request,"expense_summary.html",data)

# ===============income views=====================
@method_decorator(Signin_required,name="dispatch")
class IncomeCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=IncomeForm()

        # qs=Income.objects.all()
        qs=Income.objects.filter(user_object=request.user) #to fetch all income of login user


        return render(request,"income_add.html",{"form":form_instance,"data":qs})

    def post(self,request,*args, **kwargs):

        form_instance=IncomeForm(request.POST)

        if form_instance.is_valid():
            
            # add user_object to form instance
            
            form_instance.instance.user_object=request.user

            form_instance.save()

            messages.success(request,"income added successfully")

            return redirect("income-add")
        else:
            
            messages.error(request,"failed to add income")

            return render(request,"income_add.html",{"form":form_instance})
@method_decorator(Signin_required,name="dispatch")
class IncomeUpdateView(View):

    def get(self,request,*args, **kwargs):

        id=kwargs.get("pk")

        income_object=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=income_object)

        return render(request,"income_edit.html",{"form":form_instance})

    def post(self,request,*args, **kwargs):

        id=kwargs.get("pk")

        income_object=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=income_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()
            
            messages.success(request,"income has been updated successfully")

            return redirect("income-add")

        else:
            
            messages.error(request,"failed to update income")

            return render(request,"income_edit.html",{"form":form_instance})
        
@method_decorator(Signin_required,name="dispatch")
class IncomeDetailView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        qs=Income.objects.get(id=id)
        
        return render(request,"income_detail.html",{"data":qs})
    
@method_decorator(Signin_required,name="dispatch")
class IncomeDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Income.objects.get(id=id).delete()
        
        messages.success(request,"successfully deleted")
        
        return redirect("income-add")
    

#RegistrationView

class SighnUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):
        
        form_instance=RegistrationForm(request.POST)
        
        if form_instance.is_valid():
            
            # form_instance.save() passwrd is not encripted
            
            data=form_instance.cleaned_data
            
            User.objects.create_user(**data) #password will encripted
            
            print("user object created")
            
            return redirect("signin")
            
        else:
            
            print("failed")
            
            return render(request,"register.html",{"form":form_instance})


#loginView
#==username,password
#step1: extract username,password from form
#step2: authenticate()
#step3: session

class SignInView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=LoginForm()
        
        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=LoginForm(request.POST)
        
        if form_instance.is_valid():
            
            data=form_instance.cleaned_data
            
            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("dashboard")

        messages.error(request,"invalid credential")

        return render(request,"login.html",{"form":form_instance})
        
@method_decorator(Signin_required,name="dispatch")
class SignOutView(View):
    
    def get(self,request,*args, **kwargs):
        
        logout(request)

        return redirect("signin")

class DashBoardView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        income_list=Income.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        print("expense list", expense_list)

        print("income list", income_list)

        expense_total=expense_list.values('amount').aggregate(total=Sum("amount"))

        income_total=income_list.values('amount').aggregate(total=Sum('amount'))

        print("expense total", expense_total)

        print("income total", income_total)
        
        monthly_expenses={}
        
        monthly_incomes={}
        
        for month in range(1,13):
            
            start_date=datetime.date(current_year,month,1)
            
            if month==12:
                
                end_date=datetime.date(current_year+1,1,1)
            else:
                
                end_date=datetime.date(current_year,month+1,1)
            
            monthly_expense_total=Expense.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum('amount'))['total']
            
            monthly_income_total=Income.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum('amount'))['total']
            
            monthly_expenses[start_date.strftime('%B')]=monthly_expense_total if monthly_expense_total else 0
            
            monthly_incomes[start_date.strftime('%B')]=monthly_income_total if monthly_income_total else 0 #convert startdate to maonth and if monthly income none then set to 0
            
        print("monthly expense",monthly_expenses)
        
        print("monthly income",monthly_incomes)
        
        form_instance=SummaryForm()

        return render(request,"dashboard.html",{
            "expense":expense_total,
            "income":income_total,
            "form":form_instance,
            "monthly_expense":monthly_expenses,
            "monthly_incomes":monthly_incomes
            }
                      )

    def post(self,request,*args, **kwargs):

        form_instance=SummaryForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            start_date=data.get("start_date")

            end_date=data.get("end_date")

            expense_list=Expense.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)

            income_list=Income.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)

            print("expense list", expense_list)

            print("income list", income_list)

            expense_total=expense_list.values('amount').aggregate(total=Sum("amount"))

            income_total=income_list.values('amount').aggregate(total=Sum('amount'))

            print("expense total", expense_total)

            print("income total", income_total)

            form_instance=SummaryForm()

            return render(request,"dashboard.html",{"expense":expense_total,"income":income_total,"form":form_instance})




