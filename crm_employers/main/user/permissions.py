from rest_framework.permissions import BasePermission

class GraphGroupPermission(BasePermission):
    def has_permission(self, request, view):
        #checking if the user specific is inside the permission
        #later it will be gathered from the sqlite database
        return request.user.groups.filter(name="full_graph_permission")
    

class InsightsGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="full_insight_permission")
    

class CanCreateEployers(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="can_create_employers")
    

class CanCreateDepartments(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="can_create_departments")
    

class CanUpdateGetEmployers(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="can_update_get_employers")
    