import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    config_dir = Path(__file__).parent.parent / "config"
    # Load settings.yaml
    try:
        with open(config_dir / "settings.yaml", 'r') as f:
            settings = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_dir / 'settings.yaml'}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML format in settings.yaml: {e}")
    
    # Load cred.yaml
    try:
        with open(config_dir / "cred.yaml", 'r') as f:
            creds = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_dir / 'cred.yaml'}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML format in cred.yaml: {e}")
    
    # Process users (roles)
    users = creds.get("users", {})
    for role, user_data in users.items():
        if not isinstance(user_data, dict):
            raise ValueError(f"Invalid user data format for role: {role}")
            
        username_key = user_data.get("username_key")
        password_key = user_data.get("password_key")
        
        if not username_key or not password_key:
            raise ValueError(f"Missing credential keys for role: {role}")
        
        user_data["username"] = os.getenv(username_key)
        user_data["password"] = os.getenv(password_key)
        
        if not user_data["username"]:
            raise ValueError(f"Missing environment variable: {username_key}")
        if not user_data["password"]:
            raise ValueError(f"Missing environment variable: {password_key}")
    
    # Process employees (by name)
    employees = creds.get("employees", {})
    for name, emp_data in employees.items():
        if not isinstance(emp_data, dict):
            raise ValueError(f"Invalid employee data format for: {name}")
            
        username_key = emp_data.get("username_key")
        password_key = emp_data.get("password_key")
        
        if not username_key or not password_key:
            raise ValueError(f"Missing credential keys for employee: {name}")
        
        emp_data["username"] = os.getenv(username_key)
        emp_data["password"] = os.getenv(password_key)
        
        if not emp_data["username"]:
            raise ValueError(f"Missing environment variable: {username_key}")
        if not emp_data["password"]:
            raise ValueError(f"Missing environment variable: {password_key}")
    
    # Process secret
    secret = creds.get("secret", {})
    if secret:
        password_key = secret.get("password_key")
        if password_key:
            secret["password"] = os.getenv(password_key)
    
    return {"settings": settings, "credentials": {"users": users, "employees": employees, "secret": secret}}
