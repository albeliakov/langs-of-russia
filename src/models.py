from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class Language(db.Model):
    __tablename__ = 'languages'
    id       = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(100), nullable=False, unique=True)

    # при удалении Language все записи из district_languages и language_tasks будут удалены
    district_languages = db.relationship(
        'DistrictLanguage',
        backref='language_ref',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    tasks = db.relationship(
        'LanguageTask',
        backref='language_ref',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class Districts(db.Model):
    __tablename__ = 'districts'
    district = db.Column(db.String(50), primary_key=True)
    name_ru  = db.Column(db.String(100), nullable=False)

    district_languages = db.relationship(
        'DistrictLanguage',
        backref='district_ref',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class DistrictLanguage(db.Model):
    __tablename__ = 'district_languages'
    id       = db.Column(db.Integer, primary_key=True)
    district = db.Column(
        db.String(50),
        db.ForeignKey('districts.district', ondelete='CASCADE'),
        nullable=False
    )
    language = db.Column(
        db.Integer,
        db.ForeignKey('languages.id', ondelete='CASCADE'),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint('district', 'language', name='uix_district_language'),
    )


class LanguageTask(db.Model):
    __tablename__ = 'language_tasks'
    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    language    = db.Column(
        db.Integer,
        db.ForeignKey('languages.id', ondelete='CASCADE'),
        nullable=False
    )
