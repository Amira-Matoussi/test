"""
Phone utility functions for RAG Server
Handles phone number normalization
"""


def normalize_phone_number(phone: str) -> str:
    """Normalize phone number format"""
    # Remove all non-digits
    digits_only = ''.join(filter(str.isdigit, phone))

    # Add country code if missing
    if len(digits_only) == 8 and digits_only.startswith('2'):  # Tunisia local number
        return f"+216{digits_only}"
    elif len(digits_only) == 11 and digits_only.startswith('216'):  # Tunisia with country code
        return f"+{digits_only}"
    elif not phone.startswith('+'):
        return f"+{digits_only}"
    else:
        return phone
