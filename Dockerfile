FROM acait/django-container:1.0.38 as app-container

USER root
RUN apt-get update && apt-get install mysql-client libmysqlclient-dev -y
USER acait

ADD --chown=acait:acait . /app/
RUN /app/bin/pip install -r requirements.txt

ADD --chown=acait:acait docker/ project/

RUN . /app/bin/activate && pip install nodeenv && nodeenv -p &&\
    npm install -g npm && ./bin/npm install less -g

RUN . /app/bin/activate && python manage.py collectstatic --noinput &&\
    python manage.py compress -f

FROM acait/django-test-container:1.0.38 as app-test-container

COPY --from=0 /app/ /app/
COPY --from=0 /static/ /static/
