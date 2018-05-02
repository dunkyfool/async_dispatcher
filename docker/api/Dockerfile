FROM python:2

WORKDIR /usr/src/app

COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD [ "python", "-u", "./app.py" ]
