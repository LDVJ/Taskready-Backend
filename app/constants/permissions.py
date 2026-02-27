from enum import Enum

class PermissionEnum(str, Enum):
    DASHBOARD = "dashboard"
    USERS = "users"
    TASKS = "tasks"
    
    