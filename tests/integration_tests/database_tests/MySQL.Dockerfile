# Derived from official mysql image (our base image)
FROM mysql:8.0

# Add a database
ENV MYSQL_DATABASE ${MYSQL_DATABASE}
ENV MYSQL_ROOT_PASSWORD ${MYSQL_ROOT_PASSWORD}
# by default the image lacks UTF-8 support, so add this line:
ENV LANG C.UTF-8

# Add the content of the sql_scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./sql_scripts/ /docker-entrypoint-initdb.d/
