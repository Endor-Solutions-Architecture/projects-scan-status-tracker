# Projects Scan Status Tracker (PSST)

## Overview

This README documentation is intended for the Endor Labs Projects Scan Status Tracker. This tool will list all the projects in your Endor Labs namespace and also add functionality of filtering and sorting them based on latest project scan status. Currently supports projects scanned on Github. (Gitlab and BitBucket will be added soon)

## No Warranty

Please be advised that this software is provided on an "as is" basis, without warranty of any kind, express or implied. The authors and contributors make no representations or warranties of any kind concerning the safety, suitability, lack of viruses, inaccuracies, typographical errors, or other harmful components of this software. There are inherent dangers in the use of any software, and you are solely responsible for determining whether this software is compatible with your equipment and other software installed on your equipment.

By using this software, you acknowledge that you have read this disclaimer, understand it, and agree to be bound by its terms and conditions. You also agree that the authors and contributors of this software are not liable for any damages you may suffer as a result of using, modifying, or distributing this software.

## Features

- Allows user to fetch all projects within the namespace
- Allows users to filter and sort projects based on latest scan status

## Installation

### Create certificate for PSST domain psst.localhost

You will be requested for below details while creating certificate creation, only domain field is mandatory rest can be blank:

```
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []: **psst.localhost**
Email Address []:
```

```
mkdir certs && cd certs
openssl req -newkey rsa:2048 -nodes -keyout psst.key -x509 -days 365 -out psst.crt
cat psst.crt psst.key > psst.pem
```

You can use certificate from Let's Encrypt if needed.

### Prepare nginx.conf

Modify the hostname in nginx.conf in case you are using any other domain, if you are using psst.localhost no change required

### Add domain to /etc/hosts

`127.0.0.1 psst.localhost`

### Setup environment variables and tokens in .env

Look into .env.sample for details

### Start the application

`docker-compose up -d`

In case this step fails on Mac, run `docker pull python:3.11.9` and run `docker-compose up -d` again.

### Access PSST

You should be able to access the app on https://psst.localhost