FROM python:3.7



WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
WORKDIR /usr/src/app/neographviz

ARG version
ENV version=$version

#CMD gunicorn -w 4 -b 0.0.0.0:5000 app:app

CMD ["python", "app.py"]
