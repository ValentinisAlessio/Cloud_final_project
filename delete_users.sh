# Loop to create users
for user in $(seq 0 39); do
    # Create user using Docker exec
    docker exec --user www-data nextcloud /var/www/html/occ user:delete "locust_user${user}"
done