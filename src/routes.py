from flask import Blueprint, request, jsonify, abort
from models import db, Language, Districts, LanguageTask, DistrictLanguage

api = Blueprint('api', __name__)

# -------------------
# LANGUAGES
# -------------------

@api.route('/languages', methods=['GET'])
def get_languages():
    languages = Language.query.all()
    return jsonify([{'id': lang.id, 'language': lang.language} for lang in languages])

@api.route('/languages', methods=['POST'])
def create_language():
    data = request.get_json()
    if not data or 'language' not in data:
        abort(400, 'Missing language name.')
    lang = Language(language=data['language'])
    db.session.add(lang)
    db.session.commit()
    return jsonify({'id': lang.id, 'language': lang.language}), 201

@api.route('/languages/<int:id>', methods=['DELETE'])
def delete_language(id):
    lang = Language.query.get_or_404(id)
    db.session.delete(lang)
    db.session.commit()
    return jsonify({'message': 'Language deleted'})


# -------------------
# DISTRICTS
# -------------------
@api.route('/districts', methods=['GET'])
def get_districts_info():
    districts = Districts.query.all()
    return jsonify([
        {
            'district': d.district,    # англ. код
            'name_ru': d.name_ru       # русское название
        }
        for d in districts
    ])


@api.route('/district-languages/<string:district_code>', methods=['GET'])
def get_languages_by_district(district_code):
    # Проверка существования округа
    district = Districts.query.get(district_code)
    if not district:
        return jsonify({'error': 'District not found'}), 404

    # Получаем все связи с языками
    links = DistrictLanguage.query.filter_by(district=district_code).all()
    result = [
        {
            'language_id': link.language,
            'language_name': link.language_ref.language
        }
        for link in links
    ]
    return jsonify({
        'district': district.district,
        'name_ru': district.name_ru,
        'languages': result
    })

@api.route('/district-languages', methods=['POST'])
def create_district_language_link():
    data = request.get_json()
    district_code = data.get('district')
    language_id = data.get('language')

    if not district_code or not language_id:
        return jsonify({'error': 'Missing district or language ID'}), 400

    # Проверка существования district и language
    district = Districts.query.get(district_code)
    language = Language.query.get(language_id)

    if not district:
        return jsonify({'error': f'District {district_code} not found'}), 404
    if not language:
        return jsonify({'error': f'Language with ID {language_id} not found'}), 404

    # Проверка на дубликаты
    existing = DistrictLanguage.query.filter_by(district=district_code, language=language_id).first()
    if existing:
        return jsonify({'message': 'Link already exists'}), 200

    # Создание новой связи
    link = DistrictLanguage(district=district_code, language=language_id)
    db.session.add(link)
    db.session.commit()

    return jsonify({
        'message': 'Link created',
        'district': district_code,
        'language_id': language_id
    }), 201



# -------------------
# LANGUAGE TASKS
# -------------------

@api.route('/language-tasks', methods=['GET'])
def get_tasks():
    tasks = LanguageTask.query.all()
    return jsonify([{'id': t.id, 'description': t.description, 'language_id': t.language} for t in tasks])

@api.route('/language-tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'description' not in data or 'language' not in data:
        abort(400, 'Missing description or language ID.')
    task = LanguageTask(description=data['description'], language=data['language'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'description': task.description, 'language_id': task.language}), 201
