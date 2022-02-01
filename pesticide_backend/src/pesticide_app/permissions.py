from rest_framework import permissions
from pesticide_app.models import *
import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_CONFIG_FILE = open(os.path.join(
    BASE_DIR,
    'config/base.yml'
))
BASE_CONFIGURATION = yaml.load(BASE_CONFIG_FILE, Loader=yaml.FullLoader)

class CommentorPermissions(permissions.BasePermission):
    """
    Allow access to comment creator, safe and post access to other members.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        return obj.commentor == request.user


class IssueCreatorPermissions(permissions.BasePermission):
    """
    Allow delete access to issue reporter, safe and post access to other members.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        elif request.method in permissions.SAFE_METHODS or request.method == 'DELETE':
            return obj.reporter == request.user
        else:
            return False


class ProjectCreatorMembersPermissions(permissions.BasePermission):
    """
    Allow access to project creator and members, safe and post access to other members.
    """

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user in obj.members.all()


class ImageProjectCreatorMembersPermissions(permissions.BasePermission):
    """
    Allow access to project (of whose the icon is being changed) creator and members, safe and post access to other members.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        return obj.project.creator == request.user or request.user in obj.project.members.all()


class AdminOrReadOnlyPermisions(permissions.BasePermission):
    """
    Allow access to admins, safe access to other members.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_master

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_master


class AdminOnlyPermisions(permissions.BasePermission):
    """
    Allow access to admins only.
    """

    def has_permission(self, request, view):
        return request.user.is_master

    def has_object_permission(self, request, view, obj):
        return request.user.is_master


class AdminOrSafeMethodsPostPermissions(permissions.BasePermission):
    """
    Allow access to admins, safe and post access to other members.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        return request.user.is_master


class ReadOnlyPermissions(permissions.BasePermission):
    """
    Allow read access.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


class UserSelfPermissions(permissions.BasePermission):
    """
    Allow users to change their own email subscriptions. 
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.user


class IssueProjectCreatorOrMembers(permissions.BasePermission):
    """
    Allow issue edit access to issue's project members. 
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'PATCH':
            return request.user in obj.project.members.all() or obj.project.creator == request.user

        return False

class ProjectMemberOrAdmin(permissions.BasePermission):
    """
    Allow webhook edit/add/delete access to only the members of the project and admins.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS :
            return True
        if request.user in obj.project.members.all() or request.user.is_master:
            return True
        return obj.creator

class IsFlaskRequest(permissions.BasePermission):
    """
    Verify Flask user with token authentication.
    """
    def has_permission(self, request, view):
        if request.method == 'GET' :
            return request.headers['Token'] == BASE_CONFIGURATION["flaskToken"]["token"]
        return False