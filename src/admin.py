from flask_admin import Admin
from wtforms import Form, StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from models import db, Language, Districts, DistrictLanguage, LanguageTask


class ReadOnlyModelView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False


class LanguageForm(Form):
    language = StringField('Язык', validators=[DataRequired()])


class LanguageAdmin(ModelView):
    form = LanguageForm
    column_labels = {
        'language': 'Язык',
    }

class DistrictAdmin(ReadOnlyModelView):
    form_columns = ['district', 'name_ru']
    column_labels = {
        'district': 'Код округа',
        'name_ru':  'Название'
    }


class DistrictLanguageAdmin(ModelView):
    form_columns    = ['district', 'language']
    column_list     = ['district', 'language']
    column_labels   = {'district': 'Округ', 'language': 'Язык'}
    form_overrides  = {'district': SelectField, 'language': SelectField}

    # Выбираемые опции для выпадающих списков
    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.district.choices = [
            (d.district, d.name_ru)
            for d in Districts.query.order_by(Districts.name_ru)
        ]
        form.language.choices = [
            (str(l.id), l.language)
            for l in Language.query.order_by(Language.language)
        ]
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.district.choices = [
            (d.district, d.name_ru)
            for d in Districts.query.order_by(Districts.name_ru)
        ]
        form.language.choices = [
            (str(l.id), l.language)
            for l in Language.query.order_by(Language.language)
        ]
        return form

    # Форматтеры для отображения в таблице
    column_formatters = {
        'language': lambda view, context, model, name: model.language_ref.language,
        'district': lambda view, context, model, name: model.district_ref.name_ru,
    }

class LanguageTaskAdmin(ModelView):
    # Показываем только описание и язык
    form_columns = ['description', 'language']
    column_list  = ['description', 'language']
    column_labels = {
        'description': 'Описание задачи',
        'language':    'Язык'
    }

    # Заставляем flask-admin использовать SelectField для поля language
    form_overrides = {
        'language': SelectField,
        'description': TextAreaField,
    }

    form_widget_args = {
        'description': {
            'rows': 10,
            'style': 'width: 100%;'
        }
    }

    # Заполняем choices динамически из таблицы Language
    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.language.choices = [
            (str(l.id), l.language)
            for l in Language.query.order_by(Language.language)
        ]
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.language.choices = [
            (str(l.id), l.language)
            for l in Language.query.order_by(Language.language)
        ]
        return form
    
    column_formatters = {
        'language': lambda view, context, model, name: model.language_ref.language,
    }


def init_admin(app):
    admin = Admin(app, name='Админка', template_mode='bootstrap4', url='/admin')
    admin.add_view(LanguageAdmin(Language, db.session,            name='Языки'))
    admin.add_view(DistrictAdmin(Districts, db.session,          name='Округа'))
    admin.add_view(DistrictLanguageAdmin(DistrictLanguage, db.session, name='Языки округов'))
    admin.add_view(LanguageTaskAdmin(LanguageTask, db.session,          name='Задачи'))