from flask_admin.contrib import sqla
from secure_views import SecureModelView


class HazardSummaryView(SecureModelView):

    can_create = True
    can_edit = True
    can_delete = False

    column_list = ('id', 'hazard_category', 'bad_distance', 'summary',
                   'source')
    column_searchable_list = ['hazard_category', 'bad_distance', 'summary',
                              'source']
    column_filters = column_list
    form_columns = column_list
