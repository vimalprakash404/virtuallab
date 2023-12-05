# Stage 1: Clone repository and prepare environment
FROM continuumio/miniconda3 as builder

ARG REPOSITORY_URL

WORKDIR /app

# Clone the repository
RUN apt-get update && apt-get install -y git
RUN git clone $REPOSITORY_URL .


# Stage 2: Create the final image with only necessary files
FROM continuumio/miniconda3

WORKDIR /app

# Copy only the files needed for the application
COPY --from=builder /app .

EXPOSE 8845

# Set the working directory to the desired folder
WORKDIR /app

CMD ["jupyter", "lab", "--ip='0.0.0.0'", "--port=8845", "--no-browser", "--allow-root"]
