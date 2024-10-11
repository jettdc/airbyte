import logging
from typing import Dict, Any

from airbyte_cdk.models.airbyte_protocol import AirbyteStream, AirbyteRecordMessage

from destination_palantir_foundry.foundry_schema.converters.airbyte_field_converter import AirbyteToFoundryConverter
from destination_palantir_foundry.foundry_schema.converters.streams.airbyte_to_stream_schema import \
    convert_ab_to_foundry_stream_schema
from destination_palantir_foundry.foundry_schema.foundry_schema import FoundrySchema, TimestampFieldSchema, StringFieldSchema
from destination_palantir_foundry.foundry_schema.providers.streams.stream_schema_provider import StreamSchemaProvider


logger = logging.getLogger("airbyte")


class StructuredStreamSchemaProvider(StreamSchemaProvider):
    def get_foundry_stream_schema(self, airbyte_stream: AirbyteStream) -> FoundrySchema:
        foundry_schema = convert_ab_to_foundry_stream_schema(
            airbyte_stream.json_schema)

        metadata_fields = [
            TimestampFieldSchema(
                name="_ab_extracted_at",
                nullable=False,
            ),
            StringFieldSchema(
                name="_airbyte_raw_id",
                nullable=False
            ),
            StringFieldSchema(
                name="_airbyte_meta",
                nullable=True
            )
        ]

        foundry_schema.fieldSchemaList = [
            *metadata_fields, *foundry_schema.fieldSchemaList]

        return foundry_schema

    def get_converted_record(
            self,
            airbyte_record: AirbyteRecordMessage,
            foundry_schema: FoundrySchema,
    ) -> Dict[str, Any]:

        return {
            "_ab_emittedAt": airbyte_record.emitted_at,
            **AirbyteToFoundryConverter.convert_ab_record(airbyte_record.data, foundry_schema)
        }
