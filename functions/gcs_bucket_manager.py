import os
from google.cloud import storage
from google.cloud import texttospeech_v1 as texttospeech
import uuid
from pydub import AudioSegment
import io
from dotenv import load_dotenv

load_dotenv()

class BucketManager:
    def __init__(self, project_id, location):
        self.storage_client = storage.Client()
        self.bucket_name = f"tts-bucket-{project_id}-{location}".lower()
        self.bucket = self._get_or_create_bucket(location)

    def _get_or_create_bucket(self, location):
        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)
            print(f"Using existing bucket: {self.bucket_name}")
        except Exception:
            bucket = self.storage_client.create_bucket(self.bucket_name, location=location)
            print(f"Created new bucket: {self.bucket_name}")
            
            # Set IAM permissions (only needed for new buckets)
            service_account_email = os.getenv('GOOGLE_CLOUD_SERVICE_ACCOUNT_EMAIL')
            role = "roles/storage.objectAdmin"
            policy = bucket.get_iam_policy(requested_policy_version=3)
            policy.bindings.append({"role": role, "members": {f"serviceAccount:{service_account_email}"}})
            bucket.set_iam_policy(policy)
            print(f"Added {service_account_email} with role {role} to {self.bucket_name}.")

        return bucket

    def upload_string(self, content, filename):
        blob = self.bucket.blob(filename)
        blob.upload_from_string(content)
        return f"gs://{self.bucket_name}/{filename}"

    def download_as_bytes(self, filename):
        blob = self.bucket.blob(filename)
        return blob.download_as_bytes()

    def delete_file(self, filename):
        blob = self.bucket.blob(filename)
        blob.delete()

