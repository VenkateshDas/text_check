FROM python:3.9

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements-freeze.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

## Add the wait script to the image
# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
# RUN chmod +x /wait

# Expose port
EXPOSE 8051

# Copy app and set python path
COPY text_check /app/
CMD ["streamlit", "run", "text_check/text_check_app.py"]

# CMD ["/wait", "&&", "streamlit", "run", "text_check/text_check_app.py"]