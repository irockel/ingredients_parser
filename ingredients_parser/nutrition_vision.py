import re
import json

from google.cloud import storage

# from google.cloud import vision_v1 as vision  # Alpha API
from google.cloud import vision

from . import config

BUCKET = config.BUCKET_NAME

vision_client = vision.ImageAnnotatorClient.from_service_account_json(
    config.KEYFILE_PATH
)
storage_client = storage.Client.from_service_account_json(
    config.KEYFILE_PATH
)


def get_destination_uri(gcs_source_uri):
    return gcs_source_uri + "-output-1-to-1.json"  # TBD


def detect_tables_write_to_cloud_storage(gcs_source_uri):
    """Table Detection with PDF/TIFF as source files on Google Cloud Storage
    We are using async because the documentation uses async, even though we're processing one file at a time.
    Could be refactored
    """
    mime_type = "image/tiff"  # TODO

    # How many pages should be grouped into each json output file.
    batch_size = 1
    client = vision_client
    feature = vision.types.Feature(type=vision.enums.Feature.Type.DOCUMENT_PARSING)
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
    gcs_destination = vision.types.GcsDestination(uri=gcs_source_uri + "-")
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=10000)
    return 1  # destinatino URI?


def read_json_from_cloud_storage(destination_uri):
    match = re.match(r"gs://([^/]+)/(.+)", destination_uri)
    bucket_name = match.group(1)
    filename = match.group(2)
    bucket = storage_client.get_bucket(bucket_name=bucket_name)
    blob = storage.Blob(filename, bucket)
    json_string = blob.download_as_string()
    return json.loads(json_string)


if __name__ == "__main__":
    detect_tables_write_to_cloud_storage(BUCKET + "doritos.tiff")
    print(
        json.dumps(
            (read_json_from_cloud_storage(get_destination_uri(BUCKET + "doritos.tiff")))
        )
    )
