import os
import uuid
import boto3
import json
from django.conf import settings

import random


syllables = ['ba', 'be', 'bo', 'ca', 'ce', 'co', 'da', 'de', 'do', 'fa', 'fe', 'fi', 'ga', 'ge', 'go']




class Util:
    @staticmethod
    def custom_image_filename(instance, filename):
        # Get the file's extension
        extension = os.path.splitext(filename)[1]

        # Generate a unique filename using a UUID
        unique_filename = f"{uuid.uuid4()}{extension}"

        # Return the custom filename with the 'images/' prefix
        return os.path.join('images/', unique_filename)
    def delete_image_from_s3(old_image_url):
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        old_image_path = old_image_url.split(bucket_name+'.s3.amazonaws.com')[1].lstrip('/')  # Extract path after bucket name
        s3.delete_object(Bucket=bucket_name, Key=old_image_path)
    def generate_random_name(input_string):
        # Choose a random number of syllables to form the name
        length = len(input_string)
    
        if length < 4:
            input_string = input_string + random.randint(1000, 9999)

        # Calculate the starting index for the substring
        start_index = (length - 4) // 2

        # Use slicing to get the middle 4 characters
        middle_chars = input_string[start_index:start_index + 4]
        num_syllables = random.randint(2, 4)

        # Generate the random name by combining random syllables
        name = ''.join(random.choice(syllables) for _ in range(num_syllables))
        name += middle_chars
        return name.capitalize()