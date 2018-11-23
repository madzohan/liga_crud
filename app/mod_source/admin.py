from app import admin_site, Source, db
from app.admin import SecuredModelView

admin_site.add_view(SecuredModelView(Source, db.session))
