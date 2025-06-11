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
   git clone <your-repo-url>
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

## Security Features

- **File Validation**: MIME type checking and image verification
- **Secure Storage**: UUID-based naming prevents conflicts
- **Auto-Cleanup**: All files deleted after 1 hour
- **Size Limits**: 16MB maximum file size
- **Privacy**: No permanent storage, no user data collection

## How to Use

1. **Upload**: Drag and drop an image or click to browse
2. **Select Format**: Choose your desired output format
3. **Convert**: Click convert and wait for processing  
4. **Download**: Download your converted image immediately

## Browser Support

- Chrome (recommended)
- Firefox
- Safari  
- Edge
- Mobile browsers

## Troubleshooting

### Common Issues

**File too large error**:
- Maximum file size is 16MB
- Try compressing your image first

**Conversion failed**:
- Ensure the file is a valid image
- Try a different source format

**Upload not working**:
- Check your internet connection
- Ensure JavaScript is enabled

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