
FROM node:18

# Set the working directory in the container
WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y curl wget unzip git

# Install Visual Studio Code Server
RUN curl -fsSL https://code-server.dev/install.sh | sh




# Set environment variables
ENV GIT_REPO https://github.com/example/repo.git
ENV PORT 8080

# Expose the port that code-server will run on
EXPOSE $PORT


# Expose the port the app runs on

# Define environment variable
# Specify the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Start code-server with no authentication and open the cloned repository
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
