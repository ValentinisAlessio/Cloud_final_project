#!/bin/bash

# Loop to create users
for user in $(seq 0 39); do
    # Create user using Docker exec
    docker exec -e OC_PASS=test_password1234! --user www-data nextcloud /var/www/html/occ user:add --password-from-env "locust_user${user}"
done