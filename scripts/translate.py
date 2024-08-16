from googletrans import Translator

# Initialize the Translator
translator = Translator()

# German text to be translated
german_text = "General and Comparative Literature"

# Translate from German to English
translation = translator.translate(german_text, src='de', dest='en')

# Output the translated text
print(f"Original (German): {german_text}")
print(f"Translated (English): {translation.text}")



def translate_german_to_english(german_text):
    # Initialize the Translator
    translator = Translator()

    # Translate from German to English
    translation = translator.translate(german_text, src='de', dest='en')

    # Output the translated text
    return translation.text