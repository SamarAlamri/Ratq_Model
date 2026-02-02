# Use Python 3.9
FROM python:3.9

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
# We use --no-cache-dir to keep the image small
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the code
COPY . .

# Create a non-root user (Security requirement for HF Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Command to run the application using Gunicorn
# Hugging Face expects the app to run on port 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "server:app"]