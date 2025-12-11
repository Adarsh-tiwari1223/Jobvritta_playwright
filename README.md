# Jobvritta Playwright Test Automation Framework

A robust test automation framework built with Playwright and Python for testing the Jobvritta application.

## 🚀 Features

- **Page Object Model (POM)** - Clean, maintainable page objects
- **Multi-Role Authentication** - Support for admin, HR, employees, recruiters
- **Secure Credential Management** - Environment-based configuration
- **Comprehensive Base Page** - Universal element interactions, dropdowns, date pickers
- **Smart Logging** - Detailed test execution logs
- **HTML Reports** - Beautiful test reports with screenshots

## 📁 Project Structure

```
Jobvritta_playwright/
├── config/
│   ├── settings.yaml      # Environment URLs & browser settings
│   └── cred.yaml         # Credential mappings (no secrets)
├── pages/
│   ├── base_page.py      # Common page interactions
│   └── loginpage.py      # Login page object
├── tests/
│   ├── conftest.py       # Pytest fixtures & configuration
│   └── test_login.py     # Login test cases
├── utils/
│   ├── logger_setup.py   # Logging configuration
│   ├── yaml_loader.py    # Configuration loader
│   └── test_data_generator.py # Test data generation
├── reports/              # Test reports & logs
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
Update `.env` file with actual credentials:
```env
# Admin Credentials
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_admin_password

# Employee Credentials
RAJIV_USERNAME=rajiv@jobvritta.com
RAJIV_PASSWORD=Rajiv@123
# Add more employees as needed
```

### 3. Update Settings
Modify `config/settings.yaml`:
```yaml
base_url: "https://your-environment.jobvritta.com"
browser:
  headless: false
  viewport:
    width: 1366
    height: 768
```

## 🧪 Running Tests

### All Tests
```bash
python -m pytest tests/ -v
```

### Specific Test Types
```bash
# Smoke tests only
python -m pytest tests/ -m smoke -v

# Regression tests only
python -m pytest tests/ -m regression -v

# With HTML report
python -m pytest tests/ --html=reports/report.html -v
```

### Specific Test File
```bash
python -m pytest tests/test_login.py -v
```

## 👥 Multi-User Support

### Role-Based Testing
```python
# Admin login
admin = credentials['users']['admin']
login_page.login(admin['username'], admin['password'])

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
- `base_url`: Application URL
- `browser.headless`: Run in headless mode
- `browser.viewport`: Browser window size

### Credential Management
- **Secure**: Passwords stored in `.env` (git-ignored)
- **Flexible**: Easy to add new users/roles
- **Scalable**: Unlimited employee support

## 📊 Reporting

### HTML Reports
```bash
python -m pytest tests/ --html=reports/report.html --self-contained-html
```

### Logs
- Console output with timestamps
- File logging in `reports/test.log`
- Screenshot capture on failures

## 🎯 Best Practices

### Page Objects
```python
class LoginPage(BasePage):
    # Locators as class constants
    USERNAME_INPUT = "input[name='email']"
    
    def login(self, username, password):
        self.fill(self.find(self.USERNAME_INPUT), username)
```

### Test Structure
```python
@pytest.mark.smoke
def test_login(page, credentials, logger):
    login_page = LoginPage(page)
    admin = credentials['users']['admin']
    login_page.login(admin['username'], admin['password'])
    logger.info("Login successful")
```

## 🤝 Team Collaboration

### Git Workflow
1. Never commit `.env` file
2. Update `cred.yaml` for new user mappings
3. Use descriptive commit messages
4. Review page object changes

### Code Standards
- Use BasePage methods for consistency
- Add meaningful assertions
- Include proper logging
- Follow POM principles

## 🐛 Troubleshooting

### Common Issues
1. **Module not found**: Activate virtual environment
2. **Timeout errors**: Check selectors and wait conditions
3. **Login failures**: Verify credentials in `.env`
4. **Import errors**: Ensure proper project structure

### Debug Mode
```python
# Highlight elements for debugging
login_page.highlight(login_page.find(login_page.USERNAME_INPUT))

# Take screenshots
login_page.take_screenshot("debug_login")
```

## 📝 Contributing

1. Create feature branch
2. Add tests for new functionality
3. Update documentation
4. Submit pull request

## 📞 Support

For issues or questions, contact the QA team or create an issue in the repository.