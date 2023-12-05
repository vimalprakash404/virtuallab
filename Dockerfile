# Use the official MySQL image as the base image
FROM mysql:latest

# Set the root password for MySQL
ENV MYSQL_ROOT_PASSWORD=mysecretpassword

# Create a new database and user for your application
ENV MYSQL_DATABASE=mydatabase
ENV MYSQL_USER=myuser
ENV MYSQL_PASSWORD=mypassword

# Create a directory to store scripts that will be executed on container startup
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/

# Expose MySQL port
EXPOSE 3306

# Use the official Visual Studio Code server image as the base image
FROM codercom/code-server:latest

# Expose Visual Studio Code server port
EXPOSE 8080

# Set up your development environment here if needed
# For example, you can install extensions, configure settings, etc.

# Start Visual Studio Code server on container startup
CMD ["code-server", "--auth", "none"]
