from django.shortcuts import render

from django.utils import timezone

from django.db.models import Sum

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet

from rest_framework import authentication,permissions

from api.serializers import UserSerializer

from api.serializers import IncomeSerializer,ExpenseSerializer

from api.permissions import OwnerOnly

from budget.models import Income,Expense


class UserCreationView(APIView):
    
    def post(self,request,*args, **kwargs):
        
        serializer_instance=UserSerializer(data=request.data)
        
        if serializer_instance.is_valid():
            
            serializer_instance.save()
            
            return Response(data=serializer_instance.data)
        
        else:
            
            return Response(data=serializer_instance.errors)


class IncomeViewSetView(ModelViewSet):

    serializer_class=IncomeSerializer
        
    queryset=Income.objects.all()
        
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]
    
    def list(self,request,*args, **kwargs):
        
        qs=Income.objects.filter(user_object=request.user)
        
        serializer_instance=IncomeSerializer(qs,many=True)
        
        return Response(data=serializer_instance.data)
    
    def perform_create(self, serializer):
        
        return serializer.save(user_object=self.request.user)
    
class IncomeSummaryView(APIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        
        current_month=timezone.now().month
        
        current_year=timezone.now().year
        
        all_incomes=Income.objects.filter(user_object=request.user, created_date__month=current_month,created_date__year=current_year)
        
        income_total=all_incomes.values("amount").aggregate(total=Sum("amount"))
        
        category_summary=all_incomes.values("category").annotate(total=Sum("amount"))
        
        data={
            "income_total":income_total,
            
            "category_summary":category_summary

        }

        return Response(data=data)


class ExpenseViewSetView(ModelViewSet):

    serializer_class=ExpenseSerializer

    queryset=Expense.objects.all()
        
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[OwnerOnly]

    def list(self,request,*args, **kwargs):
        
        qs=Expense.objects.filter(user_object=request.user)
        
        serializer_instance=ExpenseSerializer(qs,many=True)
        
        return Response(data=serializer_instance.data)
    
    def perform_create(self, serializer):
        
        return serializer.save(user_object=self.request.user)
    
class ExpenseSummaryView(APIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args, **kwargs):

        current_year=timezone.now().year

        current_month=timezone.now().month

        all_expense=Expense.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        expense_total=all_expense.values("amount").aggregate(total=Sum("amount"))

        category_summary=all_expense.values("category").annotate(total=Sum("amount"))

        priority_summary=all_expense.values("priority").annotate(total=Sum("amount"))


        data={
            "expense_total":expense_total,
            "category_summary":category_summary,
            "priority_summary":priority_summary

        }

        return Response(data=data)