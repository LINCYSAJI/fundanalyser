from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("income",views.IncomeViewSetView,basename="income")

router.register("expense",views.ExpenseViewSetView,basename="expense")


urlpatterns = [
    
    path("register/",views.UserCreationView.as_view()),
    
    path("income/summary/",views.IncomeSummaryView.as_view()),
    
    path("expense/summary/",views.ExpenseSummaryView.as_view()),
    
    path("token/",ObtainAuthToken.as_view())
    
]+router.urls
