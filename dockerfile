FROM python:3.11-slim-buster

WORKDIR /python-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Tell Python to look inside the 'src' folder for your modules
ENV PYTHONPATH=/python-flask/src

# The container must expose the FastAPI application and allow the API to be accessed[cite: 1]
EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]