FROM jjanzic/docker-python3-opencv:latest

RUN pip3 install --upgrade pip 

WORKDIR /
COPY . /
RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]

# start web server
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]





