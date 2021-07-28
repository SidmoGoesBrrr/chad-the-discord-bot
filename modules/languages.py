def translate(language_to_translate_to):
    customBOOL = True

    if "afrikaans" in language_to_translate_to or "Afrikaans" in language_to_translate_to or "AFRIKAANS" in language_to_translate_to:
        translate_language = "aa"

    elif "arabic" in language_to_translate_to or "Arabic" in language_to_translate_to or "ARABIC" in language_to_translate_to:
        translate_language = "ar"

    elif "assamese" in language_to_translate_to or "Assamese" in language_to_translate_to or "ASSAMESE" in language_to_translate_to:
        translate_language = "as"

    elif "bihari" in language_to_translate_to or "Bihari" in language_to_translate_to or "BIHARI" in language_to_translate_to:
        translate_language = "bh"

    elif "bengali" in language_to_translate_to or "Bengali" in language_to_translate_to or "BENGALI" in language_to_translate_to:
        translate_language = "bn"

    elif "tibetan" in language_to_translate_to or "Tibetan" in language_to_translate_to or "TIBETAN" in language_to_translate_to:
        translate_language = "bo"

    elif "bosnian" in language_to_translate_to or "Bosnian" in language_to_translate_to or "BOSNIAN" in language_to_translate_to:
        translate_language = "bs"
    elif "german" in language_to_translate_to or "German" in language_to_translate_to or "GERMAN" in language_to_translate_to:
        translate_language = "de"

    elif "greek" in language_to_translate_to or "Greek" in language_to_translate_to or "GREEK" in language_to_translate_to:
        translate_language = "el"

    elif "english" in language_to_translate_to or "English" in language_to_translate_to or "ENGLISH" in language_to_translate_to:
        translate_language = "en"

    elif "spanish" in language_to_translate_to or "Spanish" in language_to_translate_to or "SPANISH" in language_to_translate_to:
        translate_language = "es"

    elif "french" in language_to_translate_to or "French" in language_to_translate_to or "FRENCH" in language_to_translate_to:
        translate_language = "fr"

    elif "gujarati" in language_to_translate_to or "Gujarati" in language_to_translate_to or "GUJARATI" in language_to_translate_to:
        translate_language = "gu"

    elif "hindi" in language_to_translate_to or "Hindi" in language_to_translate_to or "HINDI" in language_to_translate_to:
        translate_language = "hi"

    elif "kashmiri" in language_to_translate_to or "Kashmiri" in language_to_translate_to or "KASHMIRI" in language_to_translate_to:
        translate_language = "ks"

    elif "malayalam" in language_to_translate_to or "Malayalam" in language_to_translate_to or "MALAYALAM" in language_to_translate_to:
        translate_language = "ml"

    elif "marathi" in language_to_translate_to or "Marathi" in language_to_translate_to or "MARATHI" in language_to_translate_to:
        translate_language = "mr"

    elif "burmese" in language_to_translate_to or "Burmese" in language_to_translate_to or "BURMESE" in language_to_translate_to:
        translate_language = "my"

    elif "nepali" in language_to_translate_to or "Nepali" in language_to_translate_to or "NEPALI" in language_to_translate_to:
        translate_language = "ne"

    elif "oriya" in language_to_translate_to or "Oriya" in language_to_translate_to or "ORIYA" in language_to_translate_to:
        translate_language = "or"

    elif "punjabi" in language_to_translate_to or "Punjabi" in language_to_translate_to or "PUNJABI" in language_to_translate_to:
        translate_language = "pa"

    elif "sanskrit" in language_to_translate_to or "Sanskrit" in language_to_translate_to or "SANSKRIT" in language_to_translate_to:
        translate_language = "sa"

    elif "albanian" in language_to_translate_to or "Albanian" in language_to_translate_to or "ALBANIAN" in language_to_translate_to:
        translate_language = "sq"

    elif "tamil" in language_to_translate_to or "Tamil" in language_to_translate_to or "TAMIL" in language_to_translate_to:
        translate_language = "ta"

    elif "telugu" in language_to_translate_to or "Telugu" in language_to_translate_to or "TELUGU" in language_to_translate_to:
        translate_language = "te"

    elif "urdu" in language_to_translate_to or "Urdu" in language_to_translate_to or "URDU" in language_to_translate_to:
        translate_language = "ur"

    elif "chinese" in language_to_translate_to or "Chinese" in language_to_translate_to or "CHINESE" in language_to_translate_to:
        translate_language = "zh"

    else:
        translate_language = "Undetected"

    return translate_language