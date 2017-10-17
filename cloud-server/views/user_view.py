from flask_admin.contrib import sqla
from secure_views import SecureModelView


class UserView(SecureModelView):

    can_create = False
    can_edit = False
    can_delete = False

    column_list = (
        'username',
        'email',
        'user_group',
        'active',
        'last_login',
        'gender',
        'birth_date',
    )

    column_searchable_list = ['username', 'email']

    column_filters = column_list
