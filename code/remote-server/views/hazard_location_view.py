from flask_admin.contrib import sqla
from secure_views import SecureModelView


class HazardLocationView(SecureModelView):

    can_create = True
    can_edit = True
    can_delete = True

    column_list = ('id', 'hazard_category', 'place_name', 'latitude',
                   'longitude')
    column_searchable_list = ['place_name', 'hazard_category']
    column_filters = column_list
