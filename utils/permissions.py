from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS
from utils import choices

ADMIN=choices.RoleChoices.ADMIN
STAFF=choices.RoleChoices.ADMIN
CREATOR=choices.RoleChoices.CREATOR

# Helper Functions
def is_superior(user,target):
    if user.role == ADMIN:
        return target.role in [STAFF,CREATOR]
    if user.role ==STAFF:
        return target.role in [CREATOR]
def is_self(user,target):
    return user==target

class SuperUserByPassPermission(BasePermission):
    perm_map={
        'GET':'view',
        'POST':'add',
        'PUT':'edit',
        'PATCH':'edit',
        'DELETE':'delete',
    }
    action=None
    def get_code_name(self,view):
        model_class=view.queryset.model
        app_label=model_class._meta.app_label
        model_name=model_class._meta.model_name
        return f"{app_label}.can_{self.action}_{model_name}"
    
    def has_permission(self,request,view):
        if request.user.is_superuser:
            return True
        else:
            return self.custom_has_permission(request,view)
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return self.custom_has_object_permission(request,view,obj)
    
    def has_extra_permission(self,request, view):
        self.action=self.perm_map.get(request.method)
        codename=self.get_code_name(view)
        return request.user.has_perm(codename)
    
    def has_extra_object_permission(self,request,view,obj):
        self.action=self.perm_map.get(request.method)
        codename=self.get_code_name(view)
        return request.user.has_perm(codename) and obj.created_by.role in ['CR','ST']

class CanCreateUpdateUser(SuperUserByPassPermission):
    '''Only Admins and staffs can create a user
    users Other than staff and admin cannot do create_user
    only the superior user can edit the username and can
     reset userpassword in lower rank
    '''
    def custom_has_permission(self, request, view):
        role=getattr(request.user,'role', None)
        if role and role in [ADMIN, STAFF]:
            return True
    def custom_has_object_permission(self,request,view,obj):
        user=request.user
        target_user=obj
        return is_superior(user,target_user)

class CanChangePassword(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return request.user==obj

class VisitorRecordPermission(SuperUserByPassPermission):
    def custom_has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.has_perm("visitor_record.view_visitor")
        elif request.method =='POST':
            return request.user.has_perm("visitor_record.add_visitor")
    def custom_has_object_permission(self, request, view, obj):
        pass


class RoleBasedObjectPermission(SuperUserByPassPermission):
    def custom_has_permission(self, request, view):
            return True
    def custom_has_object_permission(self, request, view, obj):
        user=request.user
        try:
            if request.method in SAFE_METHODS:
                return True
            if user==obj.created_by.user:
                return True
            else:
                actor_role=request.user.role
                target_role=obj.created_by.role
                if actor_role=='AD':
                    return target_role in ['ST','CR']
                elif actor_role=='ST':
                    return target_role =='CR'
                else:
                    return False
        except AttributeError:
            return False
        else:
            return False

