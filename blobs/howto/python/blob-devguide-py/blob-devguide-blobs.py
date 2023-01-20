import io
import os, uuid
import random
import time
from azure.core.exceptions import HttpResponseError, ResourceExistsError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobLeaseClient, BlobPrefix, ContentSettings

class BlobSamples(object):

    # <Snippet_upload_blob_data>
    def upload_blob_data(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")
        data = "Sample data for blob"
        blob_client.upload_blob(data, blob_type="BlockBlob")
    # </Snippet_upload_blob_data>

    # <Snippet_upload_blob_stream>
    def get_random_bytes(self, size):
        rand = random.Random()
        result = bytearray(size)
        for i in range(size):
            result[i] = rand.randint(0, 255)
        return bytes(result)
        
    def upload_blob_stream(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")
        input_stream = io.BytesIO(self.get_random_bytes(15))
        blob_client.upload_blob(input_stream, blob_type="BlockBlob")
    # </Snippet_upload_blob_stream>

    # <Snippet_upload_blob_file>
    def upload_blob_file(self, blob_service_client: BlobServiceClient, container_name):
        container_client = blob_service_client.get_container_client(container=container_name)
        with open(file=os.path.join('filepath', 'filename'), mode="rb") as data:
            blob_client = container_client.upload_blob(name="sample-blob.txt", data=data, overwrite=True)
    # </Snippet_upload_blob_file>

    # <Snippet_upload_blob_tags>
    def upload_blob_tags(self, blob_service_client: BlobServiceClient, container_name):
        container_client = blob_service_client.get_container_client(container=container_name)
        sample_tags = {"Content": "image", "Date": "2022-01-01"}
        with open(file=os.path.join('filepath', 'filename'), mode="rb") as data:
            blob_client = container_client.upload_blob(name="sample-blob.txt", data=data, tags=sample_tags)
    # </Snippet_upload_blob_tags>

    # <Snippet_download_blob_file>
    def download_blob_to_file(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")
        with open(file=os.path.join('filepath', 'filename'), mode="wb") as sample_blob:
            download_stream = blob_client.download_blob()
            sample_blob.write(download_stream.readall())
    # </Snippet_download_blob_file>

    # <Snippet_download_blob_chunks>
    def download_blob_chunks(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        # This returns a StorageStreamDownloader
        stream = blob_client.download_blob()
        chunk_list = []

        # Read data in chunks to avoid loading all into memory at once
        for chunk in stream.chunks():
            # Process your data (anything can be done here - `chunk` is a byte array)
            chunk_list.append(chunk)
    # </Snippet_download_blob_chunks>

    # <Snippet_download_blob_stream>
    def download_blob_to_stream(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        # readinto() downloads the blob contents to a stream and returns the number of bytes read
        stream = io.BytesIO()
        num_bytes = blob_client.download_blob().readinto(stream)
        print(f"Number of bytes: {num_bytes}")
    # </Snippet_download_blob_stream>

    # <Snippet_download_blob_text>
    def download_blob_to_string(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        # content_as_text() downloads the blob contents and decodes as text - default values are shown for parameters
        blob_text = blob_client.download_blob().content_as_text(max_concurrency=1, encoding='UTF-8')
        print(f"Blob contents: {blob_text}")
    # </Snippet_download_blob_text>

    # <Snippet_list_containers>
    def list_containers(self, blob_service_client: BlobServiceClient):
        i=0
        all_pages = blob_service_client.list_containers(include_metadata=True, results_per_page=5).by_page()
        for container_page in all_pages:
            i += 1
            print(f"Page {i}")
            for container in container_page:
                print(container['name'], container['metadata'])
    # </Snippet_list_containers>

    # <Snippet_list_containers_prefix>
    def list_containers_prefix(self, blob_service_client: BlobServiceClient):
        containers = blob_service_client.list_containers(name_starts_with='test-')
        for container in containers:
            print(container['name'])
    # </Snippet_list_containers_prefix>

    # <Snippet_acquire_blob_lease>
    def acquire_blob_lease(self, blob_service_client: BlobServiceClient, container_name):
        # Instantiate a ContainerClient
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        # Acquire a 30-second lease on the container
        lease_client = blob_client.acquire_lease(30)

        return lease_client
    # </Snippet_acquire_blob_lease>

    # <Snippet_renew_blob_lease>
    def renew_blob_lease(self, lease_client: BlobLeaseClient):
        # Renew a lease on a blob
        lease_client.renew()
    # </Snippet_renew_blob_lease>

    # <Snippet_release_blob_lease>
    def release_blob_lease(self, lease_client: BlobLeaseClient):
        # Release a lease on a blob
        lease_client.release()
    # </Snippet_release_blob_lease>

    # <Snippet_break_blob_lease>
    def break_blob_lease(self, lease_client: BlobLeaseClient):
        # Break a lease on a blob
        lease_client.break_lease()
    # </Snippet_break_blob_lease>

    # <Snippet_get_blob_properties>
    def get_properties(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        properties = blob_client.get_blob_properties()

        print(f"Blob type: {properties.blob_type}")
        print(f"Blob size: {properties.size}")
        print(f"Content type: {properties.content_settings.content_type}")
        print(f"Content language: {properties.content_settings.content_language}")
    # </Snippet_set_blob_properties>

    # <Snippet_set_blob_properties>
    def set_properties(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        properties = blob_client.get_blob_properties()

        # Set the content_type and content_language headers, and populate the remaining headers from the existing properties
        blob_headers = ContentSettings(content_type="text/plain",
                                       content_encoding=properties.content_settings.content_encoding,
                                       content_language="en-US",
                                       content_disposition=properties.content_settings.content_disposition,
                                       cache_control=properties.content_settings.cache_control,
                                       content_md5=properties.content_settings.content_md5)
        
        blob_client.set_http_headers(blob_headers)
    # </Snippet_set_blob_properties>

    # <Snippet_set_blob_metadata>
    def set_metadata(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        # Retrieve existing metadata, if desired
        metadata = dict(blob_client.get_blob_properties().metadata)

        more_metadata = {'docType': 'text', 'docCategory': 'reference'}
        metadata.update(more_metadata)

        # Set metadata on the blob
        blob_client.set_blob_metadata(metadata=metadata)
    # </Snippet_set_blob_metadata>

    # <Snippet_get_blob_metadata>
    def get_metadata(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        # Retrieve existing metadata, if desired
        metadata = dict(blob_client.get_blob_properties().metadata)

        for key, value in metadata.items():
            print(key, value)
    # </Snippet_get_blob_metadata>

    # <Snippet_list_blobs_flat>
    def list_blobs_flat(self, blob_service_client: BlobServiceClient, container_name):
        container_client = blob_service_client.get_container_client(container=container_name)

        blob_list = container_client.list_blobs()

        for blob in blob_list:
            print(f"Name: {blob.name}")
    # </Snippet_list_blobs_flat>

    # <Snippet_list_blobs_flat_options>
    def list_blobs_flat_options(self, blob_service_client: BlobServiceClient, container_name):
        container_client = blob_service_client.get_container_client(container=container_name)

        blob_list = container_client.list_blobs(include=['tags'])

        for blob in blob_list:
            print(f"Name: {blob['name']}, Tags: {blob['tags']}")
    # </Snippet_list_blobs_flat_options> 

    # <Snippet_list_blobs_hierarchical>
    depth = 0
    indent = "  "
    def list_blobs_hierarchical(self, container_client: ContainerClient, prefix):
        for blob in container_client.walk_blobs(name_starts_with=prefix, delimiter='/'):
            if isinstance(blob, BlobPrefix):
                # Indentation is only added to show nesting in the output
                print(f"{self.indent * self.depth}{blob.name}")
                self.depth += 1
                self.list_blobs_hierarchical(container_client, prefix=blob.name)
                self.depth -= 1
            else:
                print(f"{self.indent * self.depth}{blob.name}")
    # </Snippet_list_blobs_hierarchical> 

    # <Snippet_set_blob_tags>
    def set_blob_tags(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        # Get any existing tags for the blob if they need to be preserved
        tags = blob_client.get_blob_tags()

        # Add or modify tags
        updated_tags = {'Sealed': 'false', 'Content': 'image', 'Date': '2022-01-01'}
        tags.update(updated_tags)

        blob_client.set_blob_tags(tags)
    # </Snippet_set_blob_tags>

    # <Snippet_get_blob_tags>
    def get_blob_tags(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        tags = blob_client.get_blob_tags()
        print("Blob tags: ")
        for k, v in tags.items():
            print(k, v)
    # </Snippet_get_blob_tags>

    # <Snippet_clear_blob_tags>
    def clear_blob_tags(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")

        tags = dict()
        blob_client.set_blob_tags(tags)
    # </Snippet_clear_blob_tags>

    # <Snippet_find_blobs_by_tags>
    def find_blobs_by_tags(self, blob_service_client: BlobServiceClient, container_name):
        container_client = blob_service_client.get_container_client(container=container_name)

        query = "\"Content\"='image'"
        blob_list = container_client.find_blobs_by_tags(filter_expression=query)
        
        print("Blobs tagged as images")
        for blob in blob_list:
            print(blob.name)
    # </Snippet_find_blobs_by_tags>

    # <Snippet_delete_blob>
    def delete_blob(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")
        blob_client.delete_blob()
    # </Snippet_delete_blob>

    # <Snippet_delete_blob_snapshots
    def delete_blob_snapshots(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")
        blob_client.delete_blob(delete_snapshots="include")
    # </Snippet_delete_blob_snapshots>

    # <Snippet_restore_blob>
    def restore_deleted_blob(self, blob_service_client: BlobServiceClient, container_name):
        blob_client = blob_service_client.get_container_client(container=container_name).get_blob_client("sample-blob.txt")
        blob_client.undelete_blob()
    # </Snippet_restore_blob>

    # <Snippet_restore_blob_version>
    def restore_deleted_blob_version(self, blob_service_client: BlobServiceClient, container_name):
        blob_name = "sample-blob.txt"
        container_client = blob_service_client.get_container_client(container=container_name)
        blob_client = container_client.get_blob_client(blob_name)

        blob_list = container_client.list_blobs(name_starts_with=blob_name, include=['deleted','versions'])

        blob_versions = []
        for blob in blob_list:
            blob_versions.append(blob.version_id)
        
        blob_versions.sort(reverse=True)
        latest_version = blob_versions[0]

        versioned_blob_properties = blob_client.get_blob_properties(version_id=latest_version)
        versioned_blob_url = container_client.get_blob_client(versioned_blob_properties).primary_endpoint

        # Restore the latest version by copying it to the base blob
        blob_client.start_copy_from_url(versioned_blob_url)
    # </Snippet_restore_blob_version>

if __name__ == '__main__':
    # TODO: Replace <storage-account-name> with your actual storage account name
    account_url = "https://pjstorageaccounttest.blob.core.windows.net"
    credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    sample = BlobSamples()

    #sample.upload_blob_data(blob_service_client, "sample-container")
    #sample.upload_blob_stream(blob_service_client, "sample-container")
    #sample.upload_blob_file(blob_service_client, "sample-container")
    #sample.upload_blob_tags(blob_service_client, "sample-container")

    #sample.download_blob_to_file(blob_service_client, "sample-container")
    #sample.download_blob_chunks(blob_service_client, "sample-container")
    #sample.download_blob_to_stream(blob_service_client, "sample-container")
    #sample.download_blob_to_string(blob_service_client, "sample-container")

    #sample.list_blobs_flat(blob_service_client, "sample-container")
    #sample.list_blobs_flat_options(blob_service_client, "sample-container")

    #container_client = blob_service_client.get_container_client(container="sample-container")
    #sample.list_blobs_hierarchical(container_client, "")

    #lease_client = sample.acquire_blob_lease(blob_service_client, "sample-container")
    #sample.renew_blob_lease(lease_client)
    #sample.release_blob_lease(lease_client)
    #sample.break_blob_lease(lease_client)

    #sample.set_properties(blob_service_client, "sample-container")
    #sample.get_properties(blob_service_client, "sample-container")
    #sample.set_metadata(blob_service_client, "sample-container")
    #sample.get_metadata(blob_service_client, "sample-container")

    sample.set_blob_tags(blob_service_client, "sample-container")
    sample.get_blob_tags(blob_service_client, "sample-container")
    sample.clear_blob_tags(blob_service_client, "sample-container")
    sample.find_blobs_by_tags(blob_service_client, "sample-container")

    #sample.copy_blob(blob_service_client, "sample-container")

    #sample.delete_blob(blob_service_client, "sample-container")