import re
import unicodedata


def sanitize_avro_field_name(input_string):
    """
    Replaces any special characters in the input string with their Unicode names.

    Avro field names must adhere to specific naming rules. Avro field names must start with a letter or 
    an underscore and can only contain letters, digits, and underscores. Special 
    characters such as hyphens, at symbols, etc., are not allowed in Avro field names.
    """

    def replace(match):
        char = match.group()
        char_name = unicodedata.name(char, f'char_{ord(char)}')
        pascal_case_name = ''.join(word.capitalize() for word in re.split(r'\W+', char_name))
        return f'__{pascal_case_name}__'

    pattern = re.compile(r'[^a-zA-Z0-9_ ]')

    return pattern.sub(replace, input_string).replace(' ', '_')
