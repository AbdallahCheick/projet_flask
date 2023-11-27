FROM python:3.8.0



# update pip to minimize dependency errors 

RUN pip install --upgrade pip
RUN pip install --upgrade Flask
RUN pip install maturin
RUN pip install cryptography



# define the present working directory

WORKDIR /docker-flask-test



# copy the contents into the working dir

ADD . /docker-flask-test



# run pip to install the dependencies of the flask app

RUN pip install -r requirements.txt
RUN pip3 install Flask
RUN pip3 install Flask-Cors
RUN pip3 install Werkzeug
RUN pip3 install Flask-SQLAlchemy
RUN pip3 install SQLAlchemy
RUN pip3 install datetime
RUN pip3 install pymysql



# define the command to start the container

CMD ["python","app.py"]

