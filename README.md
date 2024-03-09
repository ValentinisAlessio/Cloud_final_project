# Cloud_final_project
Repository of the final assignment for cloud computing exam

## Deployement
First, to spool up the container images, a `docker-compose.yml` file is provided, so just run

```sh
docker-compose up -d
```
This way you are able to access the nextcloud instance with your browser through `http://localhost:8080`.

To be able to perform tests, I've set up a Locust container, but before running it, you first need to create various users that will be used.

In order to do this, before creating the actual users, just perform
```sh
docker exec --user www-data nextcloud /var/www/html/occ config:system:set trusted_domains 1 --value=nextcloud
```
as otherwise nextcloud by default only authorizes operations made by `localhost`.

Now you can create user instances, in my framework 40, by running
```bash
sh setup.sh
```

Now you are free to begin to stress the nextcloud instance by loggin to Locust through `http://localhost:8089` and lounching your stress test.

## NGINX proxy manager
Before starting with nextcloud, start by configuring a secure access pattern through the use of an nginx reverse proxy. First connect to the port to which it is attached, so by running `localhost:81`.

Then insert the default admin user and password which are
```
username: admin@example.com
password: changeme
```

Now you need to change them, for example with:
```
username: admin@nextcloud.com
password: whatever-you-want
```

Now you can add a new proxy host by 
```
Hosts -> Proxy Hosts -> Add Proxy Host
```

Now set a new proxy host with the settings you like.
