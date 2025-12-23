from datetime import datetime, timedelta

class Device:
    def __init__(self, device_id, device_type, owner, firmware_version="1.0.0"):
        self.device_id = device_id
        self.device_type = device_type
        self.owner = owner
        self.firmware_version = firmware_version
        self.compliance_status = "unknown"
        self.last_security_scan = None
        self.is_active = True
        self.access_log = []

    def log_access(self, username, action):
        self.access_log.append(f"{datetime.now()}: {username} - {action}")
    
    def get_username(self):
        return self.username
    
    def authorise(self, user):
        if not self.is_active:
            self.log_access(user.get_username(), "Denied - Non-compliant device")
            return False

        if self.check_compliance != "compliant":
            if not self.check_privileges("admin"):
                self.log_access(user.get_username(), "Denied - Non-compliant device")
                return False
        
        if self.owner != user.get_username() and not user.check_privileges("admin"):
            self.log_access(user.get_username(), "Denied - Not owner")
            return False
        
        self.log_access(user.get_username(), "Access granted")
        return True
    
    def run_security_scan(self):
        self.last_security_scan = datetime.now()
        self.compliance_status = 'compliant'
        self.log_access('SYSTEM', 'Security scan completed')
    
    def check_compliance(self):
        if self.last_security_scan is None:
            self.compliance_status = "unknown"
            return False
        
        days_since_scan = (datetime.now() - self.last_security_scan).days
        if days_since_scan > 30:
            self.compliance_status = 'non-compliant'
            return False
    
        return self.compliance_status == 'compliant'
    
    def update_firmware(self, version, user):
        if not user.check_privileges('admin'):
            return False
        
        self.firmware_version = version
        self.log_access(user.get_username(), f'Firmware updated to {version}')
        return True

    def quarantine(self, user):
        if not user.check_privileges('admin'):
            return False
        
        self.is_active = False
        self.log_access(user.get_username(), 'Device quarantined')
        return True
    
    def get_device_info(self):
        return {
        'device_id': self.device_id,
        'device_type': self.device_type,
        'firmware_version': self.firmware_version,
        'compliance_status': self.compliance_status,
        'owner': self.owner,
        'is_active': self.is_active
        }
    
class DeviceManager:
    def __init__(self):
        self.devices =   {}

    def add_device(self, device):
        device_info = device.get_device_info()
        self.devices[device_info['device_id']] = device

    def remove_device(self, device_id, user):
        if not user.check_privileges('admin'):
            return False
        if device_id in self.devices:
            del self.devices[device_id]
            return True
        return False
    
    def generate_security_report(self, user):
        if not user.check_privileges('admin'):
            return None
        
        report = []
        for device_id, device in self.devices:
            device.check_compliance()
            info = device.get_device_info()
            report.append(info)
        return report

class User:
    def __init__(self, username, admin=False):
        self.username = username
        self.admin = admin
    
    def get_username(self):
        return self.username
    
    def check_privileges(self, privilege):
        if privilege == 'admin':
            return self.is_admin
        return False
