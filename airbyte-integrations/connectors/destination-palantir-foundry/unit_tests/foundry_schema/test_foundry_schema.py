import unittest

from destination_palantir_foundry.foundry_schema import foundry_schema
from destination_palantir_foundry.foundry_schema.foundry_schema import TimestampFieldSchema, DateFieldSchema, \
    BooleanFieldSchema, \
    StringFieldSchema, IntegerFieldSchema, ArrayFieldSchema, DoubleFieldSchema, StructFieldSchema, FoundrySchema


# TODO(jcrowson): Add additional tests for other field types


class TestFoundryFields(unittest.TestCase):
    def test_arrayField_basicArrayType(self):
        array_field = foundry_schema.ArrayFieldSchema(
            name="array",
            nullable=False,
            customMetadata={},
            arraySubtype=foundry_schema.StringFieldSchema(
                nullable=False,
                customMetadata={},
            )
        )

        result = array_field.model_dump(by_alias=True, exclude_unset=True)

        self.assertEqual(result, {
            "type": "ARRAY",
            "nullable": False,
            "name": "array",
            "customMetadata": {},
            "arraySubtype": {
                "type": "STRING",
                "nullable": False,
                "customMetadata": {},
            }
        })

    def test_arrayField_nestedArrayType(self):
        array_field = foundry_schema.ArrayFieldSchema(
            name="array",
            nullable=False,
            arraySubtype=foundry_schema.ArrayFieldSchema(
                nullable=False,
                arraySubtype=foundry_schema.StringFieldSchema(
                    nullable=False,
                )
            )
        )

        result = array_field.model_dump(by_alias=True, exclude_unset=True)

        self.assertEqual(result, {
            "type": "ARRAY",
            "nullable": False,
            "name": "array",
            "customMetadata": {},
            "arraySubtype": {
                "type": "ARRAY",
                "nullable": False,
                "customMetadata": {},
                "arraySubtype": {
                    "type": "STRING",
                    "nullable": False,
                    "customMetadata": {},
                }
            }
        })

    def test_allFieldTypes_serializes(self):
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
                IntegerFieldSchema(name="integerField", nullable=False),
                IntegerFieldSchema(name="integerFieldWithAirbyte", nullable=False),
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
                        arraySubtype=IntegerFieldSchema(
                            nullable=False
                        )
                    )
                ]),
                StringFieldSchema(name="unionField", nullable=False)
            ],
            dataFrameReaderClass="fakereader",
            customMetadata={}
        )

        result = schema.model_dump(by_alias=True, exclude_unset=True)

        expected_json = {
            "customMetadata": {},
            "dataFrameReaderClass": "fakereader",
            "fieldSchemaList": [
                {
                    "customMetadata": {},
                    "name": "stringField",
                    "nullable": False,
                    "type": "STRING"
                },
                {
                    "customMetadata": {},
                    "name": "booleanField",
                    "nullable": False,
                    "type": "BOOLEAN"
                },
                {
                    "customMetadata": {},
                    "name": "dateField",
                    "nullable": False,
                    "type": "DATE"
                },
                {
                    "customMetadata": {},
                    "name": "timestampWithoutTimezoneField",
                    "nullable": False,
                    "type": "TIMESTAMP"
                },
                {
                    "customMetadata": {},
                    "name": "timestampWithTimezoneField",
                    "nullable": False,
                    "type": "TIMESTAMP"
                },
                {
                    "customMetadata": {},
                    "name": "timestampWithTimezoneField2",
                    "nullable": False,
                    "type": "TIMESTAMP"
                },
                {
                    "customMetadata": {},
                    "name": "timeWithoutTimezoneField",
                    "nullable": False,
                    "type": "STRING"
                },
                {
                    "customMetadata": {},
                    "name": "timeWithTimezoneField",
                    "nullable": False,
                    "type": "STRING"
                },
                {
                    "customMetadata": {},
                    "name": "integerField",
                    "nullable": False,
                    "type": "INTEGER"
                },
                {
                    "customMetadata": {},
                    "name": "integerFieldWithAirbyte",
                    "nullable": False,
                    "type": "INTEGER"
                },
                {
                    "customMetadata": {},
                    "name": "numberField",
                    "nullable": False,
                    "type": "DOUBLE"
                },
                {
                    "arraySubtype": {
                        "customMetadata": {},
                        "nullable": False,
                        "type": "STRING"
                    },
                    "customMetadata": {},
                    "name": "stringArrayField",
                    "nullable": False,
                    "type": "ARRAY"
                },
                {
                    "customMetadata": {},
                    "name": "objectField",
                    "nullable": False,
                    "subSchemas": [
                        {
                            "customMetadata": {},
                            "name": "objStringField",
                            "nullable": False,
                            "type": "STRING"
                        },
                        {
                            "arraySubtype": {
                                "customMetadata": {},
                                "nullable": False,
                                "type": "INTEGER"
                            },
                            "customMetadata": {},
                            "name": "objIntArrayField",
                            "nullable": False,
                            "type": "ARRAY"
                        }
                    ],
                    "type": "STRUCT"
                },
                {
                    "customMetadata": {},
                    "name": "unionField",
                    "nullable": False,
                    "type": "STRING"
                }
            ]
        }

        self.assertEqual(result, expected_json)
