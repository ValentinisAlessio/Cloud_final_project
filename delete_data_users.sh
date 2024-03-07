#!/bin/bash

docker exec --user www-data nextcloud /bin/bash -c "rm /var/www/html/data/locust_user0/files/Documents/Example.md"

curl -X DELETE -u locust_user0:test_password1234! "http://localhost:8080/remote.php/dav/files/locust_user0/**/*_file_*"

# Set Nextcloud credentials
USERNAME="locust_user0"
PASSWORD="test_password1234!"

# Set Nextcloud base URL
BASE_URL="http://localhost:8080"

# List files matching the pattern
FILE_LIST=$(curl -u "$USERNAME:$PASSWORD" "$BASE_URL/remote.php/dav/files/$USERNAME" | grep '_file_' | awk '{print $2}')

# Iterate over the list of file paths and send DELETE requests
for FILE_PATH in $FILE_LIST; do
    curl -X DELETE -u "$USERNAME:$PASSWORD" "$BASE_URL$FILE_PATH"
done


# Loop to create users
for user in $(seq 0 39); do
    # Create user using Docker exec
    docker exec --user www-data nextcloud /bin/bash -c "rm /var/www/html/data/locust_user${user}/files/*_file_*"
done