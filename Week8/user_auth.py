class User:
    def __init__(self, username, password, privilege="standard"):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.privilege = privilege
        self.login_attempts = 0
        self.account_status = 'active'
        self.activity_log = []

    def hash_password(self, password):
        return f"hashed_{password}"
    
    def log_activity(self, message):
        from datetime import datetime
        self.activity_log.append(f"{datetime.now(): {message}}")
    
    def lock_account(self):
        self.account_status = "locked"
        self.log_activity("Account locked due to failed login attempts")

    def authenticate(self, password):
        if self.account_status == "locked":
            self.log_activity("Login attempt on locked account")
            return False
        
        if self.hash_password(password) == self.password_hash:
            self.login_attempts = 0
            self.log_activity("Successful login")
            return True
        else:
            self.login_attempts += 1
            self.log_activity(f"Failed login attempt {self.login_attempts}")
            if self.login_attempts >= 3:
                self.lock_account()
            return False

    def reset_login_attempts(self, admin_password):
        if self.hash_password(admin_password) == "hashed_admin_password":
            self.account_status = "active"
            self.login_attempts = 0
            self.log_activity("Account unlocked by admin")
            return True
        return False
    
    def get_safe_info(self):
        return {
            "username": self.username,
            "privilege": self.privilege,
            "account_status": self.account_status
        }
    
    def get_username(self):
        return self.username
    
    def get_privilege_level(self):
        return self.privilege