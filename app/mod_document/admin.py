from app import admin_site, Document, db
from app.admin import SecuredModelView

admin_site.add_view(SecuredModelView(Document, db.session))
