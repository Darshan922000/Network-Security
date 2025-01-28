import os 

class S3Sync:
    def sync_folder_to_s3(self, local_folder, aws_bucket_url):
        command = f"aws s3 sync {local_folder} {aws_bucket_url}"
        os.system(command=command)

    def sync_folder_from_s3(self, local_folder, aws_bucket_url):
        command = f"aws s3 sync {aws_bucket_url} {local_folder}"
        os.system(command=command)
