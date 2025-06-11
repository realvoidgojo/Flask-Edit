import os
import json
import uuid
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image

# Format config loader
def load_format_config():
    config_file = 'flask_format_config.json'
    
    default_config = {
        'SUPPORTED_FORMATS': ['PNG', 'JPEG', 'GIF', 'BMP', 'WEBP', 'TIFF'],
        'SUPPORTED_CONVERSIONS': {
            'PNG': ['JPEG', 'GIF', 'BMP', 'WEBP', 'TIFF'],
            'JPEG': ['PNG', 'GIF', 'BMP', 'WEBP', 'TIFF'],
            'GIF': ['PNG', 'JPEG', 'BMP', 'WEBP', 'TIFF'],
            'BMP': ['PNG', 'JPEG', 'GIF', 'WEBP', 'TIFF'],
            'WEBP': ['PNG', 'JPEG', 'GIF', 'BMP', 'TIFF'],
            'TIFF': ['PNG', 'JPEG', 'GIF', 'BMP', 'WEBP']
        },
        'EXTENSION_MAP': {
            'PNG': 'png', 'JPEG': 'jpg', 'GIF': 'gif',
            'BMP': 'bmp', 'WEBP': 'webp', 'TIFF': 'tiff'
        }
    }
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return default_config
    except Exception:
        return default_config

# App config
FORMAT_CONFIG = load_format_config()
SUPPORTED_FORMATS = FORMAT_CONFIG['SUPPORTED_FORMATS']
SUPPORTED_CONVERSIONS = FORMAT_CONFIG['SUPPORTED_CONVERSIONS']
EXTENSION_MAP = FORMAT_CONFIG['EXTENSION_MAP']

# Extensions setup
ALLOWED_EXTENSIONS = set()
for format_name in SUPPORTED_FORMATS:
    extension = EXTENSION_MAP[format_name]
    ALLOWED_EXTENSIONS.add(extension)
    if format_name == 'JPEG':
        ALLOWED_EXTENSIONS.add('jpeg')
    elif format_name == 'TIFF':
        ALLOWED_EXTENSIONS.add('tif')

# Flask setup
app = Flask(__name__)
app.config.update(
    UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', 'uploads'),
    TEMP_FOLDER=os.environ.get('TEMP_FOLDER', 'temp_conversions'),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
    SECRET_KEY=os.environ.get('SECRET_KEY', str(uuid.uuid4()))
)

# Cleanup tracker
file_cleanup_tracker = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_format(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    extension_to_format = {}
    
    for format_name, ext in EXTENSION_MAP.items():
        extension_to_format[ext] = format_name
    
    extension_to_format.update({'jpeg': 'JPEG', 'jpg': 'JPEG', 'tif': 'TIFF', 'tiff': 'TIFF'})
    return extension_to_format.get(extension, 'UNKNOWN')

def validate_image_file(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def convert_image(input_path, output_path, target_format):
    try:
        with Image.open(input_path) as img:
            # Handle transparency
            if target_format in ['JPEG', 'BMP'] and img.mode in ['RGBA', 'LA']:
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            
            # Color mode fix
            if target_format != 'PNG' and img.mode not in ['RGB', 'L']:
                img = img.convert('RGB')
            
            # Save options
            save_kwargs = {}
            if target_format == 'JPEG':
                save_kwargs = {'quality': 95, 'optimize': True}
            elif target_format == 'PNG':
                save_kwargs = {'optimize': True}
            elif target_format == 'WEBP':
                save_kwargs = {'quality': 95, 'method': 6}
            elif target_format == 'TIFF':
                save_kwargs = {'compression': 'tiff_lzw'}
            
            img.save(output_path, format=target_format, **save_kwargs)
            return True
    except Exception:
        return False

def schedule_file_cleanup(file_path, delay_hours=1):
    cleanup_time = datetime.now() + timedelta(hours=delay_hours)
    file_cleanup_tracker[file_path] = cleanup_time
    
    def cleanup_file():
        time.sleep(delay_hours * 3600)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            if file_path in file_cleanup_tracker:
                del file_cleanup_tracker[file_path]
        except Exception:
            pass
    
    cleanup_thread = threading.Thread(target=cleanup_file, daemon=True)
    cleanup_thread.start()

@app.route("/")
def home():
    return render_template("index.html", supported_formats=SUPPORTED_FORMATS)

@app.route("/api/convert", methods=["POST"])
def api_convert():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        target_format = request.form.get('target_format', '').upper()
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            supported_ext = ', '.join(sorted(ALLOWED_EXTENSIONS))
            return jsonify({'error': f'File type not supported. Supported: {supported_ext}'}), 400
        
        if target_format not in SUPPORTED_FORMATS:
            return jsonify({'error': f'Target format not supported'}), 400
        
        # Secure paths
        original_filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        input_filename = f"{unique_id}_{original_filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        
        source_format = get_image_format(original_filename)
        
        # Validate conversion
        if source_format not in SUPPORTED_FORMATS:
            return jsonify({'error': f'Source format {source_format} not supported'}), 400
        
        if target_format not in SUPPORTED_CONVERSIONS.get(source_format, []):
            return jsonify({'error': f'Conversion from {source_format} to {target_format} not supported'}), 400
        
        if source_format == target_format:
            return jsonify({'error': 'Source and target formats cannot be the same'}), 400
        
        # Save & validate
        file.save(input_path)
        
        if not validate_image_file(input_path):
            os.remove(input_path)
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Convert process
        base_name = os.path.splitext(original_filename)[0]
        output_extension = EXTENSION_MAP[target_format]
        output_filename = f"{unique_id}_{base_name}.{output_extension}"
        output_path = os.path.join(app.config['TEMP_FOLDER'], output_filename)
        
        if convert_image(input_path, output_path, target_format):
            schedule_file_cleanup(input_path, 1)
            schedule_file_cleanup(output_path, 1)
            
            return jsonify({
                'success': True,
                'download_url': f'/download/{output_filename}',
                'filename': f"{base_name}.{output_extension}",
                'source_format': source_format,
                'target_format': target_format
            })
        else:
            os.remove(input_path)
            return jsonify({'error': 'Image conversion failed'}), 500
            
    except Exception:
        return jsonify({'error': 'Internal server error'}), 500

@app.route("/download/<filename>")
def download_file(filename):
    try:
        file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename.split('_', 1)[1])
        else:
            return jsonify({'error': 'File not found or expired'}), 404
    except Exception:
        return jsonify({'error': 'Error serving file'}), 500

@app.route("/api/formats/<source_format>")
def get_available_formats(source_format):
    source_format = source_format.upper()
    
    if source_format not in SUPPORTED_FORMATS:
        return jsonify({'error': f'Source format {source_format} not supported'}), 400
    
    available_formats = SUPPORTED_CONVERSIONS.get(source_format, [])
    return jsonify({
        'formats': available_formats,
        'source_format': source_format,
        'total_supported': len(SUPPORTED_FORMATS)
    })

@app.route("/api/formats")
def get_all_supported_formats():
    return jsonify({
        'supported_formats': SUPPORTED_FORMATS,
        'supported_conversions': SUPPORTED_CONVERSIONS,
        'extension_map': EXTENSION_MAP
    })

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Max size: 16MB'}), 413

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

if __name__ == '__main__':
    if os.path.exists('flask_format_config.json'):
        print("Loaded format configuration from flask_format_config.json")
    
    print("FlaskEdit Image Converter is starting up...")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}/")
    print(f"Temp folder: {app.config['TEMP_FOLDER']}/")
    print("Auto-cleanup enabled: Files deleted after 1 hour")
    print(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
    print(f"Application will be available at: http://127.0.0.1:5000")

    
    app.run(host='0.0.0.0', port=5000, debug=True)