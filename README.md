# FlaskEdit - Secure Image Converter

A robust, secure single-page image conversion web application built with Flask.

## Features

- **Universal Format Support**: Convert between PNG, JPEG, GIF, BMP, WEBP, and TIFF
- **Smart Format Filtering**: Automatically excludes source format from conversion options
- **High-Quality Conversions**: Optimized settings for each format
- **Auto-Deletion**: All files automatically deleted after 1 hour for privacy
- **Responsive Design**: Works perfectly on mobile and desktop


1. **Clone the repository**:
   ```bash
   git clone https://github.com/realvoidgojo/Flask-Edit.git
   cd FlaskEdit
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally**:
   ```bash
   python main.py
   ```

4. **Access**: Open `http://localhost:5000`

## Development

### Local Setup
```bash
# Clone repository
git clone <repo-url>
cd FlaskEdit

# Install dependencies
pip install -r requirements.txt

# Set development environment
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

# Run application
python main.py
```

### Environment Variables (.env)
```bash
FLASK_ENV=production          # production or development
SECRET_KEY=your-secret-key    # Auto-generated in production
PORT=5000                     # Port number
UPLOAD_FOLDER=/tmp/uploads    # Upload directory
TEMP_FOLDER=/tmp/temp_conversions  # Temp directory
```

## Project Structure
```
FlaskEdit/
├── main.py                   # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment configuration
├── render.yaml              # Render deployment config
├── runtime.txt              # Python version specification
├── flask_format_config.json # Supported formats configuration
├── templates/
│   └── index.html           # Single page application
├── static/                  # Static files (empty)
├── uploads/                 # Temporary uploads (auto-cleaned)
└── temp_conversions/        # Temporary conversions (auto-cleaned)
```

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section above 