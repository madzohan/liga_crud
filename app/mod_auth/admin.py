from app import admin_site, Role, User, db
from app.admin import SecuredModelView

admin_site.add_view(SecuredModelView(Role, db.session))
admin_site.add_view(SecuredModelView(User, db.session))
