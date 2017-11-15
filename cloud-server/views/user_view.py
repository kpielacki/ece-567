from flask_admin.contrib import sqla
from secure_views import SecureModelView


class UserView(SecureModelView):

    can_create = True
    can_edit = True
    can_delete = True

    column_list = (
        'id',
        'email',
        'password',
        'user_group',
        'active',
        'birthday',
        'gender',
        'last_login',
    )

    column_searchable_list = ['id', 'email']
    column_filters = column_list
