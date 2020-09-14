FROM python:3.8.1
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN sh create_env.sh
EXPOSE 5000
CMD python app.py