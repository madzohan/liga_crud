from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from flask_security import current_user
from flask import redirect, abort, url_for, request
from flask_admin import Admin, helpers as admin_helpers
from flask_admin.menu import MenuLink

from app import app, security


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


class SecuredModelView(ModelView):
    def is_accessible(self):
        if not (current_user.is_active and current_user.is_authenticated):
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


admin_site = Admin(app, name='Liga documents', template_mode='bootstrap3')
admin_site.add_link(LogoutMenuLink(name='Logout', category='', endpoint='security.logout', ))


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin_site.base_template,
        admin_view=admin_site.index_view,
        h=admin_helpers,
        get_url=url_for
    )


# Redirect to admin
@app.route('/')
@login_required
def index():
    return redirect(url_for('admin.index'), code=302)
