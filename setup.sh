#!/bin/bash

# Set the path to the file to upload
FILE_TO_UPLOAD="test_data/test.txt"

# Loop to create users
for user in {0..39}; do
    # Create user using Docker exec
    docker exec -e OC_PASS=test_password1234! --user www-data nextcloud /var/www/html/occ user:add --password-from-env "locust_user$user"
    
    # Create directory for user's files
    docker exec nextcloud mkdir -p "/var/www/html/data/locust_user$user/files"
    
    # Upload file using Docker cp
    docker cp "$FILE_TO_UPLOAD" nextcloud:/var/www/html/data/locust_user$user/files/file.txt
done