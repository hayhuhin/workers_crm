from rest_framework.permissions import BasePermission

class GraphGroupPermission(BasePermission):
    def has_permission(self, request, view):
        #checking if the user specific is inside the permission
        #later it will be gathered from the sqlite database
        return request.user.groups.filter(name="full_graph_permission")
    

class InsightsGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="full_insight_permission")
    
