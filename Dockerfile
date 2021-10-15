FROM python:3
COPY ./requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /usr/app/
COPY . .
CMD [ "python", "SpotifyAuthPage.py" ]