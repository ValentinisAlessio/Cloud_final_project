# Cloud_final_project
Repository containing scrpts and report for the final assignment for the Cloud Computing (basic module) final exam.
Followingly the instructions for deploying the system and the tests. Just a copy-paste of the deployement section of the report.

## Deployement
The infrastructure has been deployed using Docker along with Docker Compose, which serves as a fundamental container orchestration tool developed by Docker.
In particular, leveraging docker-compose orchestrating capabilities, we can deploy several docker containers and the respective network and volumes, only with one command: go to the main directory, containing the \verb|docker-compose.yml| file and perform

```bash
docker-compose up -d
```

Doing this we have spawned:
- **Nextcloud** container with a dedicated volume
- **MariaDB** container with a dedicated volume
- **Locust** container
- A common **network** that connect all the containers.

Also, by just modifing the `docker-compose.yml` file you can easilly modify the backend database, the network of the containers, also with the possibility of connecting it to an existing one.

### Nextcloud setting
Before beginning, if you want to modify the maximum space allocated to each user of Nextcloud, you should modify a .dotfile into the Nextcloud instance.

In order to do this, you can enter the Nextcloud container, through
```bash
docker exec -it nextcloud /bin/bash
apt update
apt install vim
vim .htaccess
```
And then paste this section
```bash
php_value memory_limit 2G
php_value upload_max_filesize 4G
php_value post_max_size 4G
php_value max_input_time 3600
php_value max_execution_time 3600
```

Now you can access the container instantiation through `http://localhost:8080`, and using the admin credentials set in the environment of the instance in the `docker-compose.yml`, you can access in your admin account.
Now your file system is up and running.

## Testing with Locust
As previously announced, in order to assess the performance of my file system, I decided to use the Python library Locust.

Before starting, it's useful to know that as a security measure, docker by default authorizes requests made only by the localhost. So, to le the locust container make all the requests, we have to add it to the `trusted_domains` of the container. In order to achieve this result, we have to do this command:
```bash
docker exec --user www-data nextcloud /var/www/html/occ config:system:set trusted_domains 1 --value=nextcloud
```

**Warning**: If you don't perform this step, even if you are able to create all the users, tests launched from Locust will incur in \verb|permission denied| failure, failing all the tests.

Once you have done this step, you can add all the users for the test, by simply perform the predefined script:
```bash
sh setup.sh
```

Now, you should be up and running to perform your tests by logging to the Locust container through `http://localhost:8089` and start swarming requests.

To perform the test, I provided a `locustest.py` that does different requests:

- PROPFIND: HTTP request that asks to retreive some metadata associated to a directory;
- GET: HTTP method that allows to retreive a default file created for each user;
- PUT: HTTP method that allows to put on the system a file. I developed different methods that allow to upload (and right after delete, in order to preserve space) files of different sizes, namely 1kB, 1MB, 1GB in order to assess scalability of the system.


**Warning**: In the repository I didn't put the 1GB file, as it exceedes the maximum size allowed from GitHub. To create it, just
```bash
dd if=/dev/zero of=test_1gb bs=1M count=1024
```

