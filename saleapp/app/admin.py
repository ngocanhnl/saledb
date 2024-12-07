from app.models import User, Category, Product, UserRole
from flask_admin import Admin, BaseView, expose
from app import app, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect



class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class ProductView(AdminView):
    column_list = ['id','name','price']
    column_searchable_list = ['name']
    column_filters = ['id','name','price']
    column_editable_list = ['name']
    can_export = True

class CategoryView(AdminView):
    column_list = ['name', 'products']

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class Statsview(BaseView):
    @expose('/')
    def index(self):

        return self.render('admin/stats.html')
    def is_accessible(self):
        return current_user.is_authenticated

admin = Admin(app=app, name='eCommerce Admin', template_mode='bootstrap4')
admin.add_view(CategoryView(Category,db.session))
admin.add_view(ProductView(Product,db.session))

admin.add_view(AdminView(User,db.session))
admin.add_view(Statsview(name="Thong ke"))
admin.add_view(LogoutView(name="Logout"))