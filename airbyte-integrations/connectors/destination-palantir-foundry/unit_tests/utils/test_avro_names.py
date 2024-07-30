import unittest

from destination_palantir_foundry.utils.avro_names import sanitize_avro_field_name


class TestSanitizeAvroFieldName(unittest.TestCase):

    def test_spaces(self):
        input_string = "user name"
        expected_output = "user_name"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)

    def test_hyphen(self):
        input_string = "user-name"
        expected_output = "user__HyphenMinus__name"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)

    def test_at_symbol(self):
        input_string = "user@domain"
        expected_output = "user__CommercialAt__domain"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)

    def test_dot(self):
        input_string = "user.name"
        expected_output = "user__FullStop__name"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)

    def test_mixed(self):
        input_string = "user name@domain.com"
        expected_output = "user_name__CommercialAt__domain__FullStop__com"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)

    def test_no_special_characters(self):
        input_string = "username"
        expected_output = "username"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)

    def test_underscores(self):
        input_string = "user_name"
        expected_output = "user_name"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)

    def test_emoji(self):
        input_string = "user🏓name"
        expected_output = "user__TableTennisPaddleAndBall__name"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)

    def test_plus(self):
        input_string = "user+name"
        expected_output = "user__PlusSign__name"
        self.assertEqual(sanitize_avro_field_name(
            input_string), expected_output)
