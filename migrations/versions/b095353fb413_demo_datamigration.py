"""demo datamigration

Revision ID: b095353fb413
Revises: 68a2e68c1906
Create Date: 2018-11-23 16:11:54.830188

"""

# revision identifiers, used by Alembic.
from app import user_datastore, User, db

revision = 'b095353fb413'
down_revision = '68a2e68c1906'
branch_labels = None
depends_on = None


def upgrade():
    for role in ['admin', 'user']:
        user_datastore.create_role(name=role)
        user_datastore.create_user(name=role, email='{}@example.com'.format(role),
                                   password=role, roles=[role])
    db.session.commit()


def downgrade():
    users = db.session.query(User).filter(User.name.in_(('admin', 'user')))
    for user in users:
        for role in user.roles:
            db.session.delete(role)
        db.session.delete(user)
    db.session.commit()
