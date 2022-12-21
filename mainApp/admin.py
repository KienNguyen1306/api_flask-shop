from __init__ import *
from modal import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='ADMIN', template_mode='bootstrap4')


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Caterogy, db.session))
admin.add_view(ModelView(Product, db.session))

