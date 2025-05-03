from flask import Flask, render_template, request
from sqlalchemy import event
from sqlalchemy.engine import Engine

from models import db, Language, Districts, LanguageTask
from routes import api
from admin import init_admin

# Включаем PRAGMA foreign_keys=ON для SQLite
@event.listens_for(Engine, "connect")
def _enable_sqlite_fks(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

app = Flask(__name__, template_folder='templates',
    static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret'

db.init_app(app)
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    # return app.send_static_file('index.html')
    return render_template('index.html')

@app.route('/tasks/<int:language_id>')
def tasks_page(language_id):
    # Получаем номер страницы из query-параметра ?page=1
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Проверяем, что язык существует
    language = Language.query.get_or_404(language_id)

    # Фильтруем задачи и пагинируем
    pagination = LanguageTask.query.filter_by(language=language_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    tasks = pagination.items

    return render_template(
        'tasks.html',
        language=language,
        tasks=tasks,
        pagination=pagination
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Заполняем таблицу округов
        if not Districts.query.first():
            predefined = [
                ('central', 'Центральный'),
                ('northwest', 'Северо-Западный'),
                ('southern', 'Южный'),
                ('northcaucasus', 'Северо-Кавказский'),
                ('volga', 'Приволжский'),
                ('ural', 'Уральский'),
                ('siberian', 'Сибирский'),
                ('far-east', 'Дальневосточный'),
            ]
            db.session.bulk_insert_mappings(
                Districts,
                [{'district': code, 'name_ru': name} for code, name in predefined]
            )
            db.session.commit()

    init_admin(app)
    app.run(debug=True, host='0.0.0.0', port=5000)
