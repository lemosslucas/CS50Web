FROM python:3
COPY . usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requeriments.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# docker ps
# docker exec -it 'cointainer_id' bash -l
# python manage.py createsuperuser
