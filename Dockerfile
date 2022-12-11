FROM python:3.9

COPY . /app
ENV PYTHONPATH=/app
RUN pip install -r /app/requirements.txt

WORKDIR /app
#CMD python /app/tweetfake/app.py
CMD python -m flask run --host 0.0.0.0 --port 5000
