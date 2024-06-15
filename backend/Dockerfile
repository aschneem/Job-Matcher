FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY ./src .
EXPOSE 5000
CMD [ "python", "-m","gunicorn", "--bind", "0.0.0.0:5000", "app:app"]