import json
import unittest

from destination_palantir_foundry.foundry_schema.converters.airbyte_field_converter import \
    AirbyteToFoundryConverter, IS_JSON
from destination_palantir_foundry.foundry_schema.foundry_schema import StringFieldSchema, BooleanFieldSchema, \
    DateFieldSchema, TimestampFieldSchema, DoubleFieldSchema, StructFieldSchema, \
    LongFieldSchema, ArrayFieldSchema, FoundrySchema


class TestAirbyteToFoundryConverter(unittest.TestCase):
    def test_convertAbFieldToFoundryField_stringNotNull_convertsToString(self):
        ab_field_schema = {
            "type": "string",
            "description": "test description",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={"ab_description": "test description"}
        ))

    def test_convertAbFieldToFoundryField_stringNull_convertsToString(self):
        ab_field_schema = {
            "type": ["null", "string"],
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_boolean_convertsToBoolean(self):
        ab_field_schema = {
            "type": "boolean",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, BooleanFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_booleanNullable_convertsToBoolean(self):
        ab_field_schema = {
            "type": ["boolean", "null"],
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, BooleanFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_date_convertsToDate(self):
        ab_field_schema = {
            "type": "string",
            "format": "date"
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, DateFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_dateNullable_convertsToDate(self):
        ab_field_schema = {
            "type": ["null", "string"],
            "format": "date"
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, DateFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timestampWithoutTimezone_convertsToTimestamp(self):
        ab_field_schema = {
            "type": "string",
            "format": "date-time",
            "airbyte_type": "timestamp_without_timezone"
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, TimestampFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timestampWithoutTimezoneNullable_convertsToTimestamp(self):
        ab_field_schema = {
            "type": ["string", "null"],
            "format": "date-time",
            "airbyte_type": "timestamp_without_timezone"
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, TimestampFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timestampWithTimezone_convertsToTimestamp(self):
        ab_field_schema = {
            "type": "string",
            "format": "date-time",
            "airbyte_type": "timestamp_with_timezone"
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, TimestampFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timestampWithTimezoneNullable_convertsToTimestamp(self):
        ab_field_schema = {
            "type": ["null", "string"],
            "format": "date-time",
            "airbyte_type": "timestamp_with_timezone"
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, TimestampFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timestampWithTimezoneNoAirbyteType_convertsToTimestamp(self):
        ab_field_schema = {
            "type": "string",
            "format": "date-time",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, TimestampFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timestampWithTimezoneNoAirbyteTypeAbType_convertsToTimestamp(self):
        ab_field_schema = {
            "type": "string",
            "format": "date-time",
            "airbyte_type": "timestamp_with_timezone"
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, TimestampFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timestampWithTimezoneNoAirbyteTypeNullable_convertsToTimestamp(self):
        ab_field_schema = {
            "type": ["string", "null"],
            "format": "date-time",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, TimestampFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timeWithoutTimezone_convertsToString(self):
        ab_field_schema = {
            "type": "string",
            "format": "time",
            "airbyte_type": "time_without_timezone",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timeWithoutTimezoneNullable_convertsToString(self):
        ab_field_schema = {
            "type": ["string", "null"],
            "format": "time",
            "airbyte_type": "time_without_timezone",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timeWithTimezone_convertsToString(self):
        ab_field_schema = {
            "type": "string",
            "format": "time",
            "airbyte_type": "time_with_timezone",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_timeWithTimezoneNullable_convertsToString(self):
        ab_field_schema = {
            "type": ["null", "string"],
            "format": "time",
            "airbyte_type": "time_with_timezone",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_integer_convertsToLong(self):
        ab_field_schema = {
            "type": "integer",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, LongFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_integerNullable_convertsToLong(self):
        ab_field_schema = {
            "type": ["integer", "null"],
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, LongFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_integerNumberSpecialCase_convertsToInteger(self):
        ab_field_schema = {
            "type": "number",
            "airbyte_type": "integer",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, LongFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_integerNumberSpecialCaseNullable_convertsToInteger(self):
        ab_field_schema = {
            "type": ["number", "null"],
            "airbyte_type": "integer",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, LongFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_number_convertsToDouble(self):
        ab_field_schema = {
            "type": "number",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, DoubleFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_numberNullable_convertsToDouble(self):
        ab_field_schema = {
            "type": ["number", "null"],
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, DoubleFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata={}
        ))

    def test_convertAbFieldToFoundryField_arrayNoItems_convertsItemsToJsonType(self):
        ab_field_schema = {
            "type": "array",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, ArrayFieldSchema(
            name="test_field_name",
            nullable=False,
            arraySubtype=StringFieldSchema(
                nullable=True,
                customMetadata=IS_JSON
            )))

    def test_convertAbFieldToFoundryField_arrayIntegerItems_convertsToArrayWithLongType(self):
        ab_field_schema = {
            "type": "array",
            "items": {
                "type": "number",
                "airbyte_type": "integer",
            }
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, ArrayFieldSchema(
            name="test_field_name",
            nullable=False,
            arraySubtype=LongFieldSchema(nullable=False)
        ))

    def test_convertAbFieldToFoundryField_arrayIntegerItemsNullable_convertsToArrayWithLongType(self):
        ab_field_schema = {
            "type": ["null", "array"],
            "items": {
                "type": ["null", "number"],
                "airbyte_type": "integer",
            }
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, ArrayFieldSchema(
            name="test_field_name",
            nullable=True,
            arraySubtype=LongFieldSchema(nullable=True)
        ))

    def test_convertAbFieldToFoundryField_arrayNestedArrayIntegerItems_convertsToArrayWithLongType(self):
        ab_field_schema = {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number",
                    "airbyte_type": "integer",
                }
            }
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, ArrayFieldSchema(
            name="test_field_name",
            nullable=False,
            arraySubtype=ArrayFieldSchema(
                nullable=False,
                arraySubtype=LongFieldSchema(nullable=False)
            )
        ))

    def test_convertAbFieldToFoundryField_arrayUnionType_convertsToJsonType(self):
        ab_field_schema = {
            "type": "array",
            "items": [
                {
                    "type": "array",
                    "items": {
                        "type": "number",
                        "airbyte_type": "integer",
                    }
                },
                {
                    "type": "number",
                }
            ]
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, ArrayFieldSchema(
            name="test_field_name",
            nullable=False,
            arraySubtype=StringFieldSchema(nullable=True, customMetadata=IS_JSON)
        ))

    def test_convertAbFieldToFoundryField_arrayNestedArrayIntegerItemsNullable_convertsToArrayWithLongType(self):
        ab_field_schema = {
            "type": ["array", "null"],
            "items": {
                "type": ["array", "null"],
                "items": {
                    "type": ["number", "null"],
                    "airbyte_type": "integer",
                }
            }
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, ArrayFieldSchema(
            name="test_field_name",
            nullable=True,
            arraySubtype=ArrayFieldSchema(
                nullable=True,
                arraySubtype=LongFieldSchema(nullable=True)
            )
        ))

    def test_convertAbFieldToFoundryField_objectNoProperties_convertsToEmptyStruct(self):
        ab_field_schema = {
            "type": "object",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata=IS_JSON,
        ))

    def test_convertAbFieldToFoundryField_objectProperties_convertsToStruct(self):
        ab_field_schema = {
            "type": "object",
            "properties": {
                "test_prop_name": {
                    "type": "string",
                }
            }
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StructFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={},
            subSchemas=[StringFieldSchema(
                name="test_prop_name",
                nullable=False,
                customMetadata={},
            )]
        ))

    def test_convertAbFieldToFoundryField_objectPropertiesNested_convertsToStruct(self):
        ab_field_schema = {
            "type": "object",
            "properties": {
                "test_prop_name": {
                    "type": "object",
                    "properties": {
                        "test_prop_name2": {
                            "type": "string",
                        }
                    }
                }
            }
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StructFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={},
            subSchemas=[StructFieldSchema(
                name="test_prop_name",
                nullable=False,
                customMetadata={},
                subSchemas=[StringFieldSchema(
                    name="test_prop_name2",
                    nullable=False,
                    customMetadata={},
                )]
            )]
        ))

    def test_convertAbFieldToFoundryField_objectPropertiesArray_convertsToStruct(self):
        ab_field_schema = {
            "type": "object",
            "properties": {
                "test_prop_name": {
                    "type": "array",
                    "items": {
                        "type": "number",
                        "airbyte_type": "integer",
                    }
                }
            }
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StructFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata={},
            subSchemas=[ArrayFieldSchema(
                name="test_prop_name",
                nullable=False,
                customMetadata={},
                arraySubtype=LongFieldSchema(nullable=False)
            )]
        ))

    def test_convertAbFieldToFoundryField_oneOf_convertsToString(self):
        ab_field_schema = {
            "type": "object",
            "oneOf": [
                {
                    "type": "string"
                },
                {
                    "type": "number"
                }
            ]
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata=IS_JSON,
        ))

    def test_convertAbFieldToFoundryField_oneOfNullable_convertsToString(self):
        ab_field_schema = {
            "type": ["object", "null"],
            "oneOf": [
                {
                    "type": "string"
                },
                {
                    "type": "number"
                }
            ]
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata=IS_JSON,
        ))

    def test_convertAbFieldToFoundryField_oneOfNoType_convertsToString(self):
        ab_field_schema = {
            "oneOf": [
                {
                    "type": "string"
                },
                {
                    "type": "number"
                }
            ]
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=True,
            customMetadata=IS_JSON,
        ))

    def test_convertAbFieldToFoundryField_unknown_convertsToJsonType(self):
        ab_field_schema = {
            "type": "unknown",
        }

        foundry_field_schema = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema("test_field_name", ab_field_schema)

        self.assertEqual(foundry_field_schema, StringFieldSchema(
            name="test_field_name",
            nullable=False,
            customMetadata=IS_JSON,
        ))

    def test_convertRecordField_nullableNone_returnsNone(self):
        value = None

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            StringFieldSchema(
                name="string",
                nullable=True,
            )
        )

        self.assertEqual(result, None)

    def test_convertRecordField_nonNullableNone_raises(self):
        value = None

        with self.assertRaises(ValueError):
            AirbyteToFoundryConverter.convert_record_field(
                value,
                StringFieldSchema(
                    name="string",
                    nullable=False,
                )
            )

    def test_convertRecordField_arrayNoValues_emptyArray(self):
        value = []

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            ArrayFieldSchema(
                name="array",
                nullable=False,
                arraySubtype=StringFieldSchema(
                    nullable=False,
                )
            )
        )

        self.assertEqual(result, [])

    def test_convertRecordField_arrayWithPrimitiveValues_converts(self):
        value = ["test", "test2"]

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            ArrayFieldSchema(
                name="array",
                nullable=False,
                arraySubtype=StringFieldSchema(
                    nullable=False,
                )
            )
        )

        self.assertEqual(result, ["test", "test2"])

    def test_convertRecordField_arrayWithUnionValues_converts(self):
        value = ["test", 1]

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            ArrayFieldSchema(
                name="array",
                nullable=False,
                arraySubtype=StringFieldSchema(
                    nullable=True,
                    customMetadata=IS_JSON
                )
            )
        )

        self.assertEqual(result, [json.dumps(v) for v in value])

    def test_convertRecordField_arrayWithPrimitiveValuesAndNulls_converts(self):
        value = ["test", None]

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            ArrayFieldSchema(
                name="array",
                nullable=False,
                arraySubtype=StringFieldSchema(
                    nullable=True,
                )
            )
        )

        self.assertEqual(result, ["test", None])

    def test_convertRecordField_2dArray_converts(self):
        value = [
            ["test1", "test2"],
            ["test3", None]
        ]

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            ArrayFieldSchema(
                name="array",
                nullable=False,
                arraySubtype=ArrayFieldSchema(
                    nullable=False,
                    arraySubtype=StringFieldSchema(
                        nullable=True,
                    )
                )
            )
        )

        self.assertEqual(result, [["test1", "test2"], ["test3", None]])

    def test_convertRecordField_boolean_converts(self):
        values = [True, False, None]

        results = [AirbyteToFoundryConverter.convert_record_field(
            value,
            BooleanFieldSchema(
                name="boolean",
                nullable=True,
            )
        ) for value in values]

        self.assertEqual(results, [True, False, None])

    def test_convertRecordField_date_converts(self):
        value = "2021-01-23"

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            DateFieldSchema(
                name="date",
                nullable=False,
            )
        )

        self.assertEqual(result, value)

    def test_convertRecordField_dateBC_raises(self):
        value = "2021-01-23 BC"

        with self.assertRaises(ValueError):
            AirbyteToFoundryConverter.convert_record_field(
                value,
                DateFieldSchema(
                    name="date",
                    nullable=False,
                )
            )

    def test_convertRecordField_double_converts(self):
        value = 1.0001

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            DoubleFieldSchema(
                name="double",
                nullable=False,
            )
        )

        self.assertEqual(result, 1.0001)

    def test_convertRecordField_long_converts(self):
        value = 1

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            LongFieldSchema(
                name="integer",
                nullable=False,
            )
        )

        self.assertEqual(result, 1)

    def test_convertRecordField_string_converts(self):
        value = "1"

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            StringFieldSchema(
                name="string",
                nullable=False,
            )
        )

        self.assertEqual(result, "1")

    def test_convertRecordField_struct_convertsNested(self):
        value = {
            "test": {
                "test2": "test2",
                "test3": None,
                "test4": "2023-01-23"
            }
        }

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            StructFieldSchema(
                name="string",
                nullable=False,
                subSchemas=[
                    StructFieldSchema(
                        name="test",
                        nullable=False,
                        subSchemas=[
                            StringFieldSchema(
                                name="test2",
                                nullable=False
                            ),
                            StringFieldSchema(
                                name="test3",
                                nullable=True
                            ),
                            DateFieldSchema(
                                name="test4",
                                nullable=True
                            )
                        ]
                    )
                ]
            )
        )

        self.assertEqual(result, {
            "test": {
                "test2": "test2",
                "test3": None,
                "test4": "2023-01-23"
            }
        })

    def test_convertValue_timestampWithTimezone_converts(self):
        value = "2022-07-22T16:00:00+0:00"

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            TimestampFieldSchema(
                name="timestamp",
                nullable=False,
            )
        )

        self.assertEqual(result, 1658505600000)

    def test_convertValue_timestampWithTimezone2_converts(self):
        value = "2022-07-22T12:00:00+04:00"

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            TimestampFieldSchema(
                name="timestamp",
                nullable=False,
            )
        )

        self.assertEqual(result, 1658476800000)

    def test_convertValue_timestampWithoutTimezone_converts(self):
        value = "2022-07-22T08:00:00"

        result = AirbyteToFoundryConverter.convert_record_field(
            value,
            TimestampFieldSchema(
                name="timestamp",
                nullable=False,
            )
        )

        self.assertEqual(result, 1658476800000)

    def test_convertRecord_nested(self):
        schema = FoundrySchema(
            fieldSchemaList=[
                StringFieldSchema(name="stringField", nullable=False),
                BooleanFieldSchema(name="booleanField", nullable=False),
                DateFieldSchema(name="dateField", nullable=False),
                TimestampFieldSchema(name="timestampWithoutTimezoneField", nullable=False),
                TimestampFieldSchema(name="timestampWithTimezoneField", nullable=False),
                TimestampFieldSchema(name="timestampWithTimezoneField2", nullable=False),
                StringFieldSchema(name="timeWithoutTimezoneField", nullable=False),
                StringFieldSchema(name="timeWithTimezoneField", nullable=False),
                LongFieldSchema(name="integerField", nullable=False),
                LongFieldSchema(name="integerFieldWithAirbyte", nullable=False),
                DoubleFieldSchema(name="numberField", nullable=False),
                ArrayFieldSchema(
                    name="stringArrayField",
                    nullable=False,
                    arraySubtype=StringFieldSchema(
                        nullable=False
                    )
                ),
                StructFieldSchema(name="objectField", nullable=False, subSchemas=[
                    StringFieldSchema(name="objStringField", nullable=False),
                    ArrayFieldSchema(
                        name="objIntArrayField",
                        nullable=False,
                        arraySubtype=LongFieldSchema(
                            nullable=False
                        )
                    )
                ]),
                StringFieldSchema(name="unionField", nullable=False)
            ],
            dataFrameReaderClass="fakereader",
            customMetadata={}
        )

        record = {
            "stringField": "Hello, OpenAI!",
            "booleanField": False,
            "dateField": "2022-01-01",
            "timestampWithoutTimezoneField": "2022-01-01T12:00:00",
            "timestampWithTimezoneField": "2022-01-01T12:00:00Z",
            "timestampWithTimezoneField2": "2022-01-01T12:00:00+00:00",
            "timeWithoutTimezoneField": "12:00:00",
            "timeWithTimezoneField": "12:00:00+00:00",
            "integerField": 12345,
            "integerFieldWithAirbyte": 67890,
            "numberField": 123.45,
            "stringArrayField": ["item1", "item2", "item3"],
            "objectField": {
                "objStringField": "Nested string",
                "objIntArrayField": [1, 2, 3, 4, 5]
            },
            "unionField": "This can be a string, a number, or a boolean"
        }

        result = AirbyteToFoundryConverter.convert_ab_record(record, schema)

        self.assertEqual(result, {
            "stringField": "Hello, OpenAI!",
            "booleanField": False,
            "dateField": "2022-01-01",
            "timestampWithoutTimezoneField": 1641038400000,
            "timestampWithTimezoneField": 1641038400000,
            "timestampWithTimezoneField2": 1641038400000,
            "timeWithoutTimezoneField": "12:00:00",
            "timeWithTimezoneField": "12:00:00+00:00",
            "integerField": 12345,
            "integerFieldWithAirbyte": 67890,
            "numberField": 123.45,
            "stringArrayField": ["item1", "item2", "item3"],
            "objectField": {
                "objStringField": "Nested string",
                "objIntArrayField": [1, 2, 3, 4, 5]
            },
            "unionField": "This can be a string, a number, or a boolean"
        })
