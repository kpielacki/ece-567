from flask_admin.contrib import sqla
from flask import Flask, url_for, redirect, request, abort
from flask_admin.contrib import sqla
from flask_security import (Security, SQLAlchemyUserDatastore, UserMixin,
                            RoleMixin, current_user, login_required)


class SecureModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect('/login')


# class SecureBaseView(sqla.BaseView):
# 
#     def is_accessible(self):
#         if not current_user.is_active or not current_user.is_authenticated:
#             return False
# 
#         if current_user.has_role('superuser'):
#             return True
# 
#         return False
# 
#     def _handle_view(self, name, **kwargs):
#         print('HERE IN HANDLE VIEW')
#         if not self.is_accessible():
#             if current_user.is_authenticated:
#                 abort(403)
#             else:
#                 return redirect(url_for('security.login', next=request.url))
# 
# 
# class SecureIndexView(sql.AdminIndexView):
# 
#     @admin.expose('/')
#     def index(self):
#         return self.render('admin/index.html')
# 
#     def is_accessible(self):
#         if not current_user.is_active or not current_user.is_authenticated:
#             return False
# 
#         if current_user.has_role('superuser'):
#             return True
# 
#         return False
# 
#     def _handle_view(self, name, **kwargs):
#         print('HERE IN HANDLE VIEW')
#         if not self.is_accessible():
#             if current_user.is_authenticated:
#                 abort(403)
#             else:
#                 return redirect(url_for('security.login', next=request.url))
