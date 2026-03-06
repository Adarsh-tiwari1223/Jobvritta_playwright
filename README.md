# Jobvritta Playwright Test Automation Framework

A robust test automation framework built with Playwright and Python for testing the Jobvritta application.

## 🚀 Features

- **Page Object Model (POM)** - Clean, maintainable page objects with locators inside classes
- **Multi-Role Authentication** - Support for admin, HR, employees, recruiters with secret auth
- **Secure Credential Management** - Environment-based configuration with .env protection
- **Comprehensive Base Page** - Universal element interactions, dropdowns, date pickers, toast messages
- **Smart Error Detection** - Automatic validation error capture
- **Detailed Logging & Screenshots** - Complete test execution tracking
- **HTML Reports** - Beautiful test reports with organized screenshots

## 📁 Project Structure

```
Jobvritta_playwright/
├── config/
│   ├── settings.yaml      # Environment URLs & browser settings
│   └── cred.yaml         # Credential mappings (no secrets)
├── pages/
│   ├── base_page.py      # Universal page interactions & utilities
│   └── loginpage.py      # Login & secret auth page object
├── tests/
│   ├── conftest.py       # Pytest fixtures & configuration
│   └── test_login.py     # Login test cases (valid/invalid)
├── utils/
│   ├── logger_setup.py   # Logging configuration
│   ├── yaml_loader.py    # Configuration loader
│   └── test_data_generator.py # Test data generation
├── reports/
│   ├── screenshots/      # Test screenshots
│   ├── test.log         # Test execution logs
│   └── report.html      # HTML test reports
├── .env                  # Secure credentials (not in git)
├── .gitignore           # Git ignore rules
├── pytest.ini          # Pytest configuration
└── requirements.txt     # Python dependencies
```

## 🛠️ Setup

### 1. Clone & Install
```bash
git clone <repository-url>
cd Jobvritta_playwright
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

### 2. Configure Credentials
Create a `.env` file in the root directory with your credentials:
```env
# Admin Credentials
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_admin_password

# Secret Authentication
SECRET_PASSWORD=your_secret_password

# HR Manager Credentials
HR_MANAGER_USERNAME=your_hr_username
HR_MANAGER_PASSWORD=your_hr_password

# Employee Credentials
NITIN_USERNAME=employee1@company.com
NITIN_PASSWORD=employee1_password

ANIL_USERNAME=employee2@company.com
ANIL_PASSWORD=employee2_password

# Add more employees as needed
```

**Important**: Never commit the `.env` file. It's already in `.gitignore`.

### 3. Update Settings
Modify `config/settings.yaml`:
```yaml
base_url: "https://your-app-url.com"
browser:
  headless: false
  viewport:
    width: 1366
    height: 768
```

## 🧪 Running Tests

### All Tests
```bash
python -m pytest tests/ -v -s
```

### Specific Test Types
```bash
# Smoke tests only
python -m pytest tests/ -m smoke -v -s

# Regression tests only
python -m pytest tests/ -m regression -v -s

# With HTML report
python -m pytest tests/ --html=reports/report.html --self-contained-html -v -s
```

### Specific Test File
```bash
python -m pytest tests/test_login.py -v -s
```

**Note**: Use `-s` flag to see console output and debug information.

## 👥 Multi-User Support

### Role-Based Testing
```python
# Admin login with secret authentication
admin = credentials['users']['admin']
login_page.login(admin['username'], admin['password'])
login_page.submit_secret(credentials['secret']['password'])

# Employee login by name
rajiv = credentials['employees']['rajiv']
login_page.login(rajiv['username'], rajiv['password'])
```

### Adding New Employees
1. Add to `.env`:
```env
NEW_EMPLOYEE_USERNAME=newuser@jobvritta.com
NEW_EMPLOYEE_PASSWORD=NewPass@123
```

2. Add to `config/cred.yaml`:
```yaml
employees:
  new_employee:
    username_key: "NEW_EMPLOYEE_USERNAME"
    password_key: "NEW_EMPLOYEE_PASSWORD"
```

## 🔧 Configuration

### Environment Settings
- `base_url`: Jobvritta application URL
- `browser.headless`: Run in headless mode
- `browser.viewport`: Browser window size

### Credential Management
- **Secure**: Passwords stored in `.env` (git-ignored)
- **Flexible**: Easy to add new users/roles
- **Scalable**: Unlimited employee support

## 📊 Reporting

### HTML Reports
```bash
python -m pytest tests/ --html=reports/report.html --self-contained-html -v
```

### Logs & Screenshots
- **Console output**: Real-time with `-s` flag
- **File logging**: `reports/test.log`
- **Screenshots**: `reports/screenshots/`
- **Debug images**: Automatic capture on test steps

### Report Structure
```
reports/
├── screenshots/
│   ├── debug_page.png
│   └── screenshot_*.png
├── test.log
└── report.html
```

## 🎯 Best Practices

### Page Objects
```python
class LoginPage(BasePage):
    # Locators based on actual Jobvritta application
    USERNAME_INPUT = "textbox[name='UserName']"
    PASSWORD_INPUT = "textbox[name='Password']"
    LOGIN_BUTTON = "button[name='LOGIN']"
    
    def login(self, username, password):
        self.page.get_by_role("textbox", name="UserName").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="LOGIN").click()
    
    def submit_secret(self, secret):
        self.page.get_by_role("textbox", name="Enter Secret Password").fill(secret)
        self.page.get_by_role("button", name="SAVE").click()
```

### Test Structure
```python
@pytest.mark.smoke
def test_login(page, credentials, logger):
    page.goto("/login")
    login_page = LoginPage(page)
    admin = credentials['users']['admin']
    login_page.login(admin['username'], admin['password'])
    logger.info("Login successful")
```

### Error Detection
```python
# Automatic validation error detection
error = login_page.login_error_msg()
if error:
    print(f"Validation errors: {error}")
```

## 🤝 Team Collaboration

### Git Workflow
1. Never commit `.env` file
2. Update `cred.yaml` for new user mappings
3. Use descriptive commit messages
4. Review page object changes

### Code Standards
- Use BasePage methods for consistency
- Add meaningful assertions with expect()
- Include proper logging with context
- Follow POM principles with locators in page classes

## 🐛 Troubleshooting

### Common Issues
1. **Module not found**: Activate virtual environment
2. **Timeout errors**: Check selectors match Jobvritta application
3. **Login failures**: Verify credentials in `.env`
4. **Import errors**: Ensure proper project structure

### Debug Mode
```python
# Highlight elements for debugging
login_page.highlight(login_page.find(login_page.USERNAME_INPUT))

# Take screenshots (saved to reports/screenshots/)
login_page.take_screenshot("debug_login")

# Error message detection
error = login_page.login_error_msg()
if error:
    print(f"Login error: {error}")
```

### Validation Errors
The framework automatically detects Jobvritta validation messages:
- `"username is required*"`
- `"password is required*"`

## 📝 Contributing

1. Create feature branch
2. Add tests for new functionality
3. Update documentation
4. Submit pull request

## 📞 Support

For issues or questions, contact the QA team or create an issue in the repository.