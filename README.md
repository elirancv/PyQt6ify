# PyQt6ify Pro

A modern, modular PyQt6-based desktop application framework with built-in configuration management, error handling, and database support.

## 🌟 Features

- 🎨 Modern and responsive user interface
  - Customizable themes with live preview
  - Light/Dark mode support
  - Runtime theme switching with persistence
  - Status bar feedback for operations
- ⚙️ Modular architecture for easy extension
- 📝 Comprehensive configuration management
- 🔒 Built-in error handling and logging
  - Detailed operation logging
  - Error tracking and reporting
  - Status feedback for user actions
- 💾 SQLite database integration
- 🛠️ Modern menu system
  - Icon-based menu items
  - Keyboard shortcuts
  - Status tips
- 📊 Status bar for user feedback
- 🎯 Resource management for icons and assets

## 📁 Project Structure

```
PyQt6ify-Pro/
├── config/                 # Configuration module
│   ├── app_config.py      # Configuration management
│   └── config.ini         # Application settings
├── database/              # Database storage
│   └── my_pyqt_app.db    # SQLite database file
├── modules/               # Core modules
│   ├── about.py          # About dialog
│   ├── database.py       # Database operations
│   ├── error_handling.py # Error management
│   ├── menu.py          # Menu system
│   ├── theme/           # Theme management
│   │   ├── theme_dialog.py    # Theme settings dialog
│   │   └── theme_manager.py   # Theme engine
│   ├── status_bar.py    # Status bar
│   └── toolbar.py       # Toolbar functionality
├── resources/            # Application resources
│   └── icons/           # Application icons
├── logs/                 # Application logs
├── docs/                 # Documentation
├── tests/               # Test suite
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── LICENSE.md          # License information
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git (for cloning the repository)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/elirancv/PyQt6ify-Pro.git
cd PyQt6ify-Pro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## ⚙️ Configuration

The application uses a two-tier configuration system:

### 1. Runtime Configuration (app_config.py)
- Application metadata
- Module enablement
- Resource paths
- Default settings

### 2. User Configuration (config.ini)
```ini
[APP]
start_maximized = True
screen_width = 1024
screen_height = 768
```

## 💾 Database

The application uses SQLite for data storage:
- Automatic database initialization
- Connection management
- Built-in error handling
- Located in `database/my_pyqt_app.db`

## 🔍 Features in Detail

### Error Handling
```python
from modules.error_handling import show_error_dialog

try:
    # Your code here
except Exception as e:
    show_error_dialog("Error Title", str(e))
```

### Logging
```python
from loguru import logger

logger.info("Information message")
logger.error("Error message")
```

### Configuration Usage
```python
from config.app_config import Config

config = Config()
window_title = config.get_about_info('name')
is_maximized = config.get_app_setting('start_maximized')
```

## 🛠️ Development

### Adding New Features

1. Create a new module in the `modules` directory:
```python
# modules/my_feature.py
class MyFeature:
    def __init__(self):
        self.name = "My New Feature"
```

2. Enable the module in `config/app_config.py`:
```python
self.modules = {
    'my_feature': True,
    # other modules...
}
```

3. Import and use in `main.py`:
```python
from modules import my_feature
```

### Best Practices

1. **Error Handling**
   - Use the built-in error handling system
   - Provide user-friendly error messages
   - Log all errors appropriately

2. **Configuration**
   - Store user settings in config.ini
   - Keep defaults in app_config.py
   - Validate all configuration values

3. **Database**
   - Use context managers for connections
   - Handle connection errors gracefully
   - Keep database operations atomic

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Version History

### v1.0.0 b002 (2024-12-09)
- 🎨 Enhanced Theme System
  - Added status bar feedback for theme changes
  - Improved theme switching stability
  - Added detailed logging to theme operations
  - Centralized logging to app.log
- 🛠️ Menu System Improvements
  - Added icons to all menu items
  - Reorganized menu order (File, Edit, View, Help)
  - Added status tips for menu actions
- 📁 Project Structure
  - Consolidated icon resources under resources/icons
  - Improved theme module organization
  - Updated documentation

### v1.0.0 b001 (2024-09-04)
- 🚀 Initial beta release
- 🎨 Basic theme support (Light/Dark)
- 📝 Configuration management
- 🔒 Error handling and logging
- 💾 SQLite database integration
- 🛠️ Basic menu and toolbar system

## 📄 License

This project is licensed under the terms of the LICENSE.md file.

## 🙏 Acknowledgments

- PyQt6 team for the excellent GUI framework
- Contributors and users of the project

## 📫 Contact

Eliran - [@elirancv](https://github.com/elirancv)

Project Link: [https://github.com/elirancv/PyQt6ify-Pro](https://github.com/elirancv/PyQt6ify-Pro)
