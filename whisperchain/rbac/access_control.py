from auth.register import get_user_role

# Define role permissions
ROLE_PERMISSIONS = {
    'Sender': {
        'get_token': True,
        'send_message': True,
        'view_messages': False,
        'flag_message': False
    },
    'Receiver': {
        'get_token': False,
        'send_message': False,
        'view_messages': True,
        'flag_message': False
    },
    'Moderator': {
        'get_token': False,
        'send_message': False,
        'view_messages': True,
        'flag_message': True
    }
}

def check_permission(username: str, permission: str) -> bool:
    """
    Check if a user has permission to perform an action.
    
    Args:
        username: The username to check permissions for
        permission: The permission to check (e.g., 'send_message', 'view_messages')
    
    Returns:
        bool: True if the user has permission, False otherwise
    """
    try:
        role = get_user_role(username)
        return ROLE_PERMISSIONS[role].get(permission, False)
    except ValueError:
        return False

def get_user_permissions(username: str) -> dict:
    """
    Get all permissions for a user.
    
    Args:
        username: The username to get permissions for
    
    Returns:
        dict: Dictionary of permission: bool pairs
    """
    try:
        role = get_user_role(username)
        return ROLE_PERMISSIONS[role].copy()
    except ValueError:
        return {} 