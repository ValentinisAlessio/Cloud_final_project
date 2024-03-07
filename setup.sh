#!/bin/bash

# Set the path to the file to upload
FILE_TO_UPLOAD="test_data/test.txt"

# Loop to create users
for user in $(seq 0 39); do
    # Create user using Docker exec
    docker exec -e OC_PASS=test_password1234! --user www-data nextcloud /var/www/html/occ user:add --password-from-env "locust_user${user}"
    
    # # Create directory for user's files
    # docker exec nextcloud mkdir -p "/var/www/html/data/locust_user${user}/files"
    
    # # Upload file using Docker cp
    # curl -k -u "locust_user${user}:test_password1234!" -X -PUT -T "${FILE_TO_UPLOAD}" "http://localhost:8080/remote.php/dav/files/locust_user${user}/test.txt"
done