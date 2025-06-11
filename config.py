import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    TEMP_FOLDER = os.environ.get('TEMP_FOLDER', 'temp_conversions')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class ProductionConfig(Config):
    DEBUG = False
    UPLOAD_FOLDER = '/tmp/uploads'
    TEMP_FOLDER = '/tmp/temp_conversions'

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 