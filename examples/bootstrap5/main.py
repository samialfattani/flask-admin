import datetime
import enum
import os

from flask import Flask
from flask import redirect
from flask import request
from flask import url_for
from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.base import expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.fields import Select2Field
from flask_admin.menu import MenuDivider
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap5Theme
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields import DateTimeLocalField

from examples.bootstrap5.data import all_themes
from examples.bootstrap5.data import build_sample_db

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config["SECRET_KEY"] = "123456790"

# Create in-memory database
app.config["DATABASE_FILE"] = "sample_db.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + app.config["DATABASE_FILE"]
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


def get_locale():
    return "en"


# Initialize babel
babel = Babel(app, locale_selector=get_locale)


class Social(enum.Enum):
    UNKNOWN = "❌ UNKNOWN"
    Single = "🔗 Single"
    Married = "💍 Married"
    Complicated = "❓ Complicated"

    @classmethod
    def _missing_(cls, value):
        """Hook called when a value is not found in the enumeration."""
        return cls.UNKNOWN

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"<Social.{self.name}: {self.value}>"


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(64))
    active = db.Column(db.Boolean, default=True)
    dob = db.Column(db.Date)
    daily_reminder = db.Column(db.Time)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    social = db.Column(db.Enum(Social), default=Social.Single)

    organization_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    organization = db.relationship("Organization", back_populates="users")

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    shortname = db.Column(db.Unicode(16))

    users = db.relationship("User", back_populates="organization")

    def __unicode__(self):
        return f"{self.name} {self.shortname}"

    def __repr__(self):
        return self.shortname


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(64))
    content = db.Column(db.UnicodeText)

    def __unicode__(self):
        return self.name


# Customized admin interface
class CustomView(ModelView):
    pass


class UserAdmin(CustomView):
    column_searchable_list = ("name",)
    column_filters = (
        "name",
        "email",
        "organization",
        "dob",
        "daily_reminder",
        "social",
        "active",
        "created_at",
    )
    can_export = True
    export_types = ["csv", "xlsx"]

    column_editable_list = [
        "name",
        "email",
        "active",
        "dob",
        "daily_reminder",
        "social",
        "organization",
        "created_at",
    ]
    form_columns = [
        "name",
        "email",
        "active",
        "dob",
        "daily_reminder",
        "social",
        "organization_id",
        "created_at",
    ]

    form_overrides = {"organization_id": Select2Field, "created_at": DateTimeLocalField}

    form_args = {
        "organization_id": {
            "choices": [(1, "x")],
            "coerce": int,
            "label": "Organization",
            "description": "select an organization for this user",
        }
    }

    can_view_details = True
    details_modal = True
    create_modal = True
    edit_modal = True
    can_set_page_size = True
    page_size = 3
    page_size_options = (3, 10, 20, 50, 100)

    def _organization_id_choices(self):
        return [(o.id, f"{o.name} ({o.shortname})") for o in Organization.query.all()]

    def make_form(self, create_or_edit_form, obj=None):
        form = create_or_edit_form(obj)
        form.organization_id.choices = self._organization_id_choices()
        return form

    def create_form(self, obj=None):
        return self.make_form(super().create_form, obj)

    def edit_form(self, obj=None):
        return self.make_form(super().edit_form, obj)


class OrganizationAdmin(CustomView):
    column_searchable_list = ("name", "shortname")
    column_filters = ("name", "shortname")
    create_modal = True

    inline_models = [
        User,
    ]

    can_view_details = True


class MyAdminIndexView(AdminIndexView):
    def set_theme(self):
        reqTheme = request.args.get("theme")
        cookTheme = request.cookies.get("theme")

        t = reqTheme or cookTheme or "cosmo"

        if self.admin and self.admin.theme:
            if hasattr(self.admin.theme, "swatch"):
                self.admin.theme.swatch = t

    @expose("/change-theme")
    def change_theme(self):
        self.set_theme()

        next = request.referrer

        return redirect(next or url_for("admin.index"))


class FileAdminModal(FileAdmin):
    rename_modal = True
    edit_modal = True
    mkdir_modal = True
    upload_modal = True


# Flask views
@app.route("/")
def index_page():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# Create admin with custom base template
admin = Admin(
    app,
    "Bootstrap5",
    theme=Bootstrap5Theme(swatch="default", fluid=True),
    index_view=MyAdminIndexView(
        menu_icon_type="fas",
        menu_icon_value="fa-home",
        menu_class_name="text-warning",
    ),
    category_icon_classes={
        "Menu": "fa fa-cog text-danger",
    },
)

# Add views
admin.add_view(
    UserAdmin(
        User,
        db.session,
        category="Menu",
        menu_icon_type="fas",
        menu_icon_value="fa-users",
        menu_class_name="text-warning",
    )
)
admin.add_view(OrganizationAdmin(Organization, db.session, category="Menu"))

admin.add_sub_category(name="Submenu", parent_name="Menu")
admin.add_view(CustomView(Page, db.session, category="Submenu"))
admin.add_view(FileAdmin("files/", name="Local Files", category="Menu"))
admin.add_view(
    FileAdminModal("files/", name="Local Files with Modals", category="Menu")
)

admin.add_link(
    MenuLink(
        name="link1",
        url="http://www.example.com/",
        class_name="text-warning bg-danger",
        icon_type="fas",
        icon_value="fa-external-link-alt",
    )
)

admin.add_link(
    MenuLink(
        name="link1",
        url="/",
        category="Links",
        icon_type="fa",
        icon_value="fa-users",
    )
)
admin.add_link(
    MenuLink(
        name="link2", url="/", category="Links", icon_type="fas", icon_value="fa-users"
    )
)
admin.add_menu_item(MenuDivider(), target_category="Links")
admin.add_link(
    MenuLink(
        name="link3",
        url="/",
        category="Links",
        icon_type="image",
        icon_value="man.png",
    )
)
admin.add_link(
    MenuLink(
        name="link4",
        url="/",
        category="Links",
        icon_type="image-url",
        icon_value="https://cdn-icons-png.freepik.com/256/1296/1296698.png?semt=ais_white_label",
    )
)


for t in all_themes:
    admin.add_link(
        MenuLink(
            name=f"{t.title()}",
            url=f"/admin/change-theme?theme={t}",
            category="Themes",
        )
    )


if __name__ == "__main__":
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config["DATABASE_FILE"])
    if not os.path.exists(database_path):
        with app.app_context():
            build_sample_db(db, User, Page, Organization, Social)

    # Start app
    app.run(debug=True)
