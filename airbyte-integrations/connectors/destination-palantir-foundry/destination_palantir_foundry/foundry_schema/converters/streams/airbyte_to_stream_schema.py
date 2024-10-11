from typing import Dict, Any

from foundry.v2.core.models import Scheam

from destination_palantir_foundry.foundry_schema.converters.airbyte_field_converter import AirbyteToFoundryConverter
from destination_palantir_foundry.foundry_schema.foundry_schema import FoundrySchema
from destination_palantir_foundry.foundry_schema.providers.streams.common import STREAM_DATA_FRAME_READER_CLASS


def convert_ab_to_foundry_stream_schema(ab_json_schema: Dict[str, Any]) -> FoundrySchema:
    field_schemas = []
    for property_name, property_schema in ab_json_schema.get("properties", {}).items():
        field_schemas.append(AirbyteToFoundryConverter.convert_ab_to_foundry_field_schema(
            property_name, property_schema))

    return FoundrySchema(
        fieldSchemaList=field_schemas,
        dataFrameReaderClass=STREAM_DATA_FRAME_READER_CLASS,
        customMetadata={
            "streaming": {
                "type": "avro"
            },
            "format": "avro"
        }
    )
