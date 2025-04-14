from enum import Enum

class ErrorCode(Enum):
    URL_NOT_FOUND = "url_not_found"
    URL_DEACTIVATED = "url_deactivated"
    FUTURE_DATE = "future_date"
    INVALID_URL_KEY = "invalid_url_key"
    EMAIL_ALREADY_EXIST = "email_already_exist"
    INCORRECT_USER_AUTH_INPUT = "incorrect_user_auth_input"
    UNAUTHORIZED = "unauthorized"


error_messages = {
    ErrorCode.URL_NOT_FOUND: "The requested URL was not found or is no longer available.",
    ErrorCode.URL_DEACTIVATED: "The URL is deactivated by the owner.",
    ErrorCode.FUTURE_DATE: "The expiration date must be in the future. Please enter a valid date.",
    ErrorCode.INVALID_URL_KEY: "The provided key is invalid or the URL does not exist.",
    ErrorCode.EMAIL_ALREADY_EXIST: "Email already exist.",
    ErrorCode.INCORRECT_USER_AUTH_INPUT: "Incorrect email or password.",
    ErrorCode.UNAUTHORIZED: "Could not validate credentials",
}
