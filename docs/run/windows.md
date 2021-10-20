## Running dev environment

### 1. Build the containers using the command.

`set POSTGRES_USER=andrii`

`set POSTGRES_PASSWORD=11111111`

`set POSTGRES_DB=fithm`

`docker-compose -f docker-compose.yml -f docker-compose.dev.yml build`

### 2. Create tables and default data. Postgres user and password need to be same as the next step

`set POSTGRES_USER=andrii`

`set POSTGRES_PASSWORD=11111111`

`set SECRET_KEY=test_sec_key`

`set FITHM_ADMIN_MAIL=info@fithm.com`

`set FITHM_ADMIN_PASS=Horse@20180902`

`set FLASK_APP=apps\fithm-gateway\manage`

`flask db create`

### 3. Set some environment variables and run the containers. You can make a script for this purpose. Sample script is given below.

`set POSTGRES_USER=andrii`

`set POSTGRES_PASSWORD=11111111`

`set POSTGRES_DB=fithm`

`set DEBUG=True`

`set FITHM_USE_SMTP=False`

`set FITHM_SMTP_HOST=smtp.fithm.com`

`set FITHM_SMTP_PORT=587`

`set FITHM_SMTP_USER=info@fithm.com`

`set FITHM_SMTP_PASS=Horse@20180902`

`set FITHM_ADMIN_MAIL=info@fithm.com`

`set FITHM_ADMIN_PASS=Horse@20180902`

`set FITHM_QUOVO_KEY=ps_7eb7eb0c854510856e8e2ce86bce5e56861bcd5d1223aa2a1de09489d1e4fa3c`

`set TRADESHOP_SEC_KEY=tradeshop_test_key`

`set GATEWAY_SEC_KEY=test_sec_key`

`docker-compose -f docker-compose.yml -f docker-compose.dev.yml up`

Please store this content in bat file(named e.g. run.bat) and run the script. 

Note: In order to run docker on windows, you have to install the docker-desktop for windows. You can download it [here](https://hub.docker.com/editions/community/docker-ce-desktop-windows)

## Running prod environment

The project is under development. This part of the document would be written later.
