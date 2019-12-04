FROM python:2.7
ENV PYTHONUNBUFFERED 1

# copy contents of repo into an 'app' directory on container
ADD . /app
WORKDIR /app

# install python dependency packages (via setup.py) on container
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade lxml

# move manage.py out of sampleproj to root directory so that django can start
COPY sampleproj/manage.py /app/manage.py
