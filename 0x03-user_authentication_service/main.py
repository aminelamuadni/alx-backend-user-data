"""
End-to-end integration test script for the Flask user authentication service.
"""

import requests


def register_user(email: str, password: str) -> None:
    """
    Register a new user.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Raises:
        AssertionError: If the response status code is not 200.
    """
    url = 'http://localhost:5000/users'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}")


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the wrong password.

    Args:
        email (str): The email of the user.
        password (str): The incorrect password.

    Raises:
        AssertionError: If the response status code is not 401.
    """
    url = 'http://localhost:5000/sessions'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 401, (
        f"Expected status code 401, got {response.status_code}")


def log_in(email: str, password: str) -> str:
    """
    Log in with the correct email and password.

    Args:
        email (str): The email of the user.
        password (str): The correct password.

    Returns:
        str: The session ID from the response cookies.

    Raises:
        AssertionError: If the response status code is not 200.
    """
    url = 'http://localhost:5000/sessions'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}")
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """
    Attempt to access the profile without being logged in.

    Raises:
        AssertionError: If the response status code is not 403.
    """
    url = 'http://localhost:5000/profile'
    response = requests.get(url)
    assert response.status_code == 403, (
        f"Expected status code 403, got {response.status_code}")


def profile_logged(session_id: str) -> None:
    """
    Access the profile while logged in.

    Args:
        session_id (str): The session ID of the logged-in user.

    Raises:
        AssertionError: If the response status code is not 200.
    """
    url = 'http://localhost:5000/profile'
    response = requests.get(url, cookies={'session_id': session_id})
    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}")


def log_out(session_id: str) -> None:
    """
    Log out the user by destroying the session.

    Args:
        session_id (str): The session ID of the user.

    Raises:
        AssertionError: If the response status code is not 200.
    """
    url = 'http://localhost:5000/sessions'
    response = requests.delete(url, cookies={'session_id': session_id})
    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}")


def reset_password_token(email: str) -> str:
    """
    Request a password reset token.

    Args:
        email (str): The email of the user.

    Returns:
        str: The reset password token from the response.

    Raises:
        AssertionError: If the response status code is not 200.
    """
    url = 'http://localhost:5000/reset_password'
    response = requests.post(url, data={'email': email})
    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}")
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password using the reset token.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset token provided for password reset.
        new_password (str): The new password to set.

    Raises:
        AssertionError: If the response status code is not 200.
    """
    url = 'http://localhost:5000/reset_password'
    response = requests.put(url, data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    })
    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
