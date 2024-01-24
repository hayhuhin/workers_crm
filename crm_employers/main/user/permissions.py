from rest_framework.permissions import BasePermission




class SystemAdminPermission(BasePermission):
    """
    permission:
    general database permission for system admin
    """
    def has_permission(self, request, view):
        #checking if the user specific is inside the permission
        #later it will be gathered from the sqlite database
        return request.user.groups.filter(name="admin_permission")
    

class ITAdminPermission(BasePermission):
    """
    permission:
    general database permission for IT
    """
    def has_permission(self, request, view):
        #checking if the user specific is inside the permission
        #later it will be gathered from the sqlite database
        return request.user.groups.filter(name="IT_permission")
    

class FinanceFullPermission(BasePermission):
    """
    permission:
    1.full CRUD operations on finance database
    """
    def has_permission(self, request, view):
        #checking if the user specific is inside the permission
        #later it will be gathered from the sqlite database
        return request.user.groups.filter(name="finance_full_permission")
    

class FinanceViewPermission(BasePermission):
    """
    permission:
    1.can view the finance data only
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="finance_view_permission")
    

class FinanceUpdatePermission(BasePermission):
    """
    permission:
    1.can update incomes only
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="finance_update_permission")


class MediumPermission(BasePermission):
    """
    gives the permission to do this:
    1.can assign finance
    2.can update income
    3.can create employers
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="medium_permission")
    



