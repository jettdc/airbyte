import json
from typing import Optional, Dict, Any, List, NamedTuple, Type, Union

from dateutil import parser, tz

from destination_palantir_foundry.foundry_schema.foundry_schema import FoundryFieldSchema, StringFieldSchema, \
    DateFieldSchema, \
    TimestampFieldSchema, BooleanFieldSchema, ArrayFieldSchema, StructFieldSchema, \
    DoubleFieldSchema, LongFieldSchema, FoundrySchema
from destination_palantir_foundry.utils.avro_names import sanitize_avro_field_name

"""
Type mappings:

| Airbyte Type               | Foundry Type                 | Notes                                                                                               |
|----------------------------|------------------------------|-----------------------------------------------------------------------------------------------------|
| string                     | string                       |                                                                                                     |
| boolean                    | boolean                      |                                                                                                     |
| date                       | date                         | Currently does not accept "BC" dates, but needs to                                                  |
| timestamp without timezone | timestamp                    | Currently does not accept "BC" dates, but needs to                                                  |
| timestamp with timezone    | timestamp                    | Currently does not accept "BC" dates, but needs to                                                  |
| time without timezone      | string                       |                                                                                                     |
| time with timezone         | string                       |                                                                                                     |
| integer                    | long                         |                                                                                                     |
| number                     | double                       |                                                                                                     |
| array[type, types]         | array[type] or array[string] | If array accepts multiple types (items: [{...type1}, {...type2}]), whole field will be jsonified
| object                     | struct                       |                                                                                                     |
| union                      | string                       | jsonified                                                                                           |

All types can be nullable.
"""

IS_JSON = {"is_json": True}


def _find_field_schema(field_name: str, field_schemas: List[FoundryFieldSchema]) -> Optional[FoundryFieldSchema]:
    for field_schema in field_schemas:
        if field_schema.name == field_name:
            return field_schema

    return None


def _convert_timestamp_to_unix_ms(timestamp: str) -> float:
    dt = parser.parse(timestamp)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz.UTC)

    unix_timestamp = dt.timestamp()
    return int(unix_timestamp) * 1000


class AirbyteFieldDescription(NamedTuple):
    type_name: Optional[str] = None
    format: Optional[str] = None
    airbyte_type: Optional[str] = None

    arr_is_union: Optional[bool] = None
    obj_is_union: Optional[bool] = None


class FoundryFieldDescription(NamedTuple):
    field_schema: Type[FoundryFieldSchema]
    custom_metadata: Optional[Dict[str, Any]] = None


DEFAULT_FOUNDRY_FIELD_DESCRIPTION = FoundryFieldDescription(
    field_schema=StringFieldSchema, custom_metadata=IS_JSON)


def _get_ab_type_from_arr(types: List[str]) -> Optional[str]:
    types_without_null = list(
        filter(lambda field_type: field_type != "null", types))
    return types_without_null[0] if len(types_without_null) > 0 else None


class AirbyteToFoundryConverter:
    type_mappings: Dict[AirbyteFieldDescription, FoundryFieldDescription] = {
        # String
        AirbyteFieldDescription(type_name="string"): \
        FoundryFieldDescription(field_schema=StringFieldSchema),

        # Boolean
        AirbyteFieldDescription(type_name="boolean"): \
        FoundryFieldDescription(field_schema=BooleanFieldSchema),

        # Date
        AirbyteFieldDescription(type_name="string", format="date"): \
        FoundryFieldDescription(field_schema=DateFieldSchema),

        # Timestamp
        AirbyteFieldDescription(type_name="string", format="date-time", airbyte_type="timestamp_without_timezone"): \
        FoundryFieldDescription(field_schema=TimestampFieldSchema),
        AirbyteFieldDescription(type_name="string", format="date-time", airbyte_type="timestamp_with_timezone"): \
        FoundryFieldDescription(field_schema=TimestampFieldSchema),
        AirbyteFieldDescription(type_name="string", format="date-time"): \
        FoundryFieldDescription(field_schema=TimestampFieldSchema),

        # Time
        AirbyteFieldDescription(type_name="string", format="time", airbyte_type="time_without_timezone"): \
        FoundryFieldDescription(field_schema=StringFieldSchema),
        AirbyteFieldDescription(type_name="string", format="time", airbyte_type="time_with_timezone"): \
        FoundryFieldDescription(field_schema=StringFieldSchema),

        # Integer
        AirbyteFieldDescription(type_name="integer"): \
        FoundryFieldDescription(field_schema=LongFieldSchema),
        AirbyteFieldDescription(type_name="number", airbyte_type="integer"): \
        FoundryFieldDescription(field_schema=LongFieldSchema),

        # Number
        AirbyteFieldDescription(type_name="number"): \
        FoundryFieldDescription(field_schema=DoubleFieldSchema),

        # Array
        AirbyteFieldDescription(type_name="array"): \
        FoundryFieldDescription(field_schema=ArrayFieldSchema),
        AirbyteFieldDescription(type_name="array", arr_is_union=False): \
        FoundryFieldDescription(field_schema=ArrayFieldSchema),
        AirbyteFieldDescription(type_name="array", arr_is_union=True): \
        FoundryFieldDescription(field_schema=ArrayFieldSchema),

        # Object
        AirbyteFieldDescription(type_name="object"): \
        FoundryFieldDescription(field_schema=StructFieldSchema),

        # Union
        AirbyteFieldDescription(type_name="object", obj_is_union=True): \
        FoundryFieldDescription(
            field_schema=StringFieldSchema, custom_metadata=IS_JSON),
        AirbyteFieldDescription(obj_is_union=True): \
        FoundryFieldDescription(
            field_schema=StringFieldSchema, custom_metadata=IS_JSON),
    }

    @staticmethod
    def convert_ab_to_foundry_field_schema(ab_field_name: Optional[str], ab_field_schema: Dict[str, Any]) -> FoundryFieldSchema:
        # Can be a single type or [type, "null"]
        ab_field_type: Union[str, List[str],
                             None] = ab_field_schema.get("type", None)

        if ab_field_type is None:
            return StringFieldSchema(
                name=ab_field_name,
                nullable=True,
                customMetadata=IS_JSON
            )

        parsed_type = None
        nullable = False
        if isinstance(ab_field_type, list):
            nullable = "null" in ab_field_type
            parsed_type = _get_ab_type_from_arr(ab_field_type)

            if parsed_type is None:
                return StringFieldSchema(
                    name=ab_field_name,
                    nullable=True,
                    customMetadata=IS_JSON
                )
        else:
            parsed_type = ab_field_type

        format_ = ab_field_schema.get("format", None)
        airbyte_type = ab_field_schema.get("airbyte_type", None)

        items_type = ab_field_schema.get("items", None)
        arr_is_union = None if items_type is None else isinstance(
            items_type, list)

        obj_is_union = None if ab_field_schema.get(
            "oneOf", None) is None else True

        foundry_field_description = AirbyteToFoundryConverter.type_mappings.get(AirbyteFieldDescription(
            type_name=parsed_type,
            format=format_,
            airbyte_type=airbyte_type,
            arr_is_union=arr_is_union,
            obj_is_union=obj_is_union
        ), DEFAULT_FOUNDRY_FIELD_DESCRIPTION)

        foundry_field_schema_kwargs = {
            "name": sanitize_avro_field_name(ab_field_name) if ab_field_name is not None else None,
            "nullable": nullable,
        }

        if foundry_field_description.custom_metadata is not None:
            foundry_field_schema_kwargs["customMetadata"] = foundry_field_description.custom_metadata

        if foundry_field_description.field_schema == ArrayFieldSchema:
            item_type: Optional[Dict] = ab_field_schema.get("items", None)
            if item_type is not None and not isinstance(items_type, list):
                foundry_field_schema_kwargs["arraySubtype"] = AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema(
                    None, item_type)
            else:
                foundry_field_schema_kwargs["arraySubtype"] = StringFieldSchema(
                    nullable=True,
                    customMetadata=IS_JSON
                )

        elif foundry_field_description.field_schema == StructFieldSchema:
            # if additional props, probably make map
            sub_schemas: List[FoundryFieldSchema] = []
            for obj_property_name, obj_property_schema in ab_field_schema.get("properties", {}).items():
                sub_schemas.append(AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema(
                    obj_property_name, obj_property_schema))

            if len(sub_schemas) == 0:
                return StringFieldSchema(
                    name=ab_field_name,
                    nullable=True,
                    customMetadata=IS_JSON
                )
            else:
                foundry_field_schema_kwargs["subSchemas"] = sub_schemas

        ab_description = ab_field_schema.get("description", None)
        if ab_description is not None:
            custom_metadata = foundry_field_schema_kwargs.get(
                "customMetadata", {})
            foundry_field_schema_kwargs["customMetadata"] = {
                **custom_metadata, "ab_description": ab_description}

        return foundry_field_description.field_schema(**foundry_field_schema_kwargs)

    @staticmethod
    def convert_record_field(value: Any, field_schema: FoundryFieldSchema) -> Any:
        if value is None and field_schema.nullable:
            return None

        if field_schema.customMetadata.get("is_json", False):
            return json.dumps(value)
        if value is None and not field_schema.nullable:
            raise ValueError(
                f"Cannot parse null value for nonnullable field: {field_schema.name}")

        if isinstance(field_schema, ArrayFieldSchema):
            if not isinstance(value, list):
                raise ValueError(
                    f"Cannot parse nonlist array type: {field_schema.name}")

            return [AirbyteToFoundryConverter.convert_record_field(item, field_schema.arraySubtype) for item in value]

        elif isinstance(field_schema, BooleanFieldSchema):
            if not isinstance(value, bool):
                raise ValueError(
                    f"Cannot parse nonbool type to bool: {field_schema.name}")

            return value

        elif isinstance(field_schema, DateFieldSchema):
            if not isinstance(value, str):
                raise ValueError(
                    f"Cannot parse nonstring date type: {field_schema.name}")

            if value.endswith("BC"):
                raise ValueError(
                    f"Cannot parse BC date type: {field_schema.name}")

            # Airbyte and foundry are both RFC 3339 date strings
            return value

        elif isinstance(field_schema, DoubleFieldSchema):
            return float(value)

        elif isinstance(field_schema, LongFieldSchema):
            return int(value)

        elif isinstance(field_schema, StringFieldSchema):
            if not isinstance(value, str):
                raise ValueError(
                    f"Cannot parse nonstring string type: {field_schema.name}")

            return value

        elif isinstance(field_schema, StructFieldSchema):
            if not isinstance(value, dict):
                raise ValueError(
                    f"Cannot parse nonobject struct type: {field_schema.name}")

            converted = {}
            for key, value in value.items():
                sanitized_key_name = sanitize_avro_field_name(key)
                field_sub_schema = _find_field_schema(
                    sanitized_key_name, field_schema.subSchemas)
                # TODO(jcrowson): throw an error if not every field is filled
                if field_sub_schema is not None:
                    converted[sanitized_key_name] = AirbyteToFoundryConverter.convert_record_field(
                        value, field_sub_schema)

            return converted

        elif isinstance(field_schema, TimestampFieldSchema):
            if not isinstance(value, str):
                raise ValueError(
                    f"Cannot parse nonstring timestamp type: {field_schema.name}")

            return _convert_timestamp_to_unix_ms(value)

    @staticmethod
    def convert_ab_record(airbyte_record: Dict[str, Any], foundry_schema: FoundrySchema) -> Dict[str, Any]:
        converted = {}

        for key, value in airbyte_record.items():
            sanitized_key = sanitize_avro_field_name(key)
            field_schema = _find_field_schema(
                sanitized_key, foundry_schema.fieldSchemaList)
            # TODO(jcrowson): throw error if not every field is filled
            if field_schema is not None:
                converted[sanitized_key] = AirbyteToFoundryConverter.convert_record_field(
                    value, field_schema)

        return converted
