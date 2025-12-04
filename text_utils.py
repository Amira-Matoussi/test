"""
Text utility functions for RAG Server
Contains pronunciation fixes and system prompt generation
"""
import re


def apply_pronunciation_fixes(text: str, assistant_name: str, language: str) -> str:
    """
    Apply pronunciation fixes to text for proper name pronunciation

    Args:
        text: The text to fix
        assistant_name: "Slah" or "Amira"
        language: "en-US", "fr-FR", or "ar-SA"

    Returns:
        Fixed text with proper pronunciation hints
    """

    # For Arabic, use native spelling
    if language == "ar-SA":
        name_replacements = {
            "Slah": "صلاح",
            "slah": "صلاح",
            "SLAH": "صلاح",
            "Amira": "أميرة",
            "amira": "أميرة",
            "AMIRA": "أميرة",
            "B2C": "بي تو سي",
            "B2B": "بي تو بي",
            "Ooredoo": "أوريدو"
        }
        for eng_name, ar_name in name_replacements.items():
            text = text.replace(eng_name, ar_name)

    # For French, ensure proper spelling
    elif language == "fr-FR":
        # Ensure Slah and Amira are written clearly
        text = re.sub(r'\bSlah\b', 'Slah', text, flags=re.IGNORECASE)
        text = re.sub(r'\bAmira\b', 'Amira', text, flags=re.IGNORECASE)
        # Break down acronyms
        text = text.replace("B2C", "B deux C")
        text = text.replace("B2B", "B deux B")

    # For English, use phonetic hints
    elif language == "en-US":
        # Keep Slah as-is but ensure it's spelled correctly
        text = re.sub(r'\bslah\b', 'Slah', text, flags=re.IGNORECASE)
        text = re.sub(r'\bamira\b', 'Amira', text, flags=re.IGNORECASE)
        # Break down B2C/B2B for better pronunciation
        text = text.replace("B2C", "B two C")
        text = text.replace("B2B", "B two B")

    return text


def get_gender_aware_system_prompt(assistant_id: int, language: str) -> str:
    """Get system prompt with proper gender grammar"""

    assistant_name = "Slah" if assistant_id == 1 else "Amira"
    is_male = assistant_id == 1
    print(f"🟢 PROMPT: id={assistant_id}, name={assistant_name}, male={is_male}, lang={language}")

    prompts = {
        "en-US": {
            True: f"You are {assistant_name}, a friendly human telecom advisor for Ooredoo.",
            False: f"You are {assistant_name}, a friendly human telecom advisor for Ooredoo."
        },
        "fr-FR": {
            True: f"Vous êtes {assistant_name}, un conseiller télécom humain et amical pour Ooredoo.",
            False: f"Vous êtes {assistant_name}, une conseillère télécom humaine et amicale pour Ooredoo."
        },
        "ar-SA": {
            True: f"أنت {assistant_name}، مستشار اتصالات بشري وودود في أوريدو.",
            False: f"أنت {assistant_name}، مستشارة اتصالات بشرية وودودة في أوريدو."
        }
    }

    result = prompts.get(language, prompts["en-US"]).get(is_male, prompts["en-US"][True])
    print(f"🟢 RETURNING: {result[:80]}...")
    return result
