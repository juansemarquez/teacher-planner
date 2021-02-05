FROM python:3
COPY .  /usr/src/app
WORKDIR /usr/src/app/teacher_planner
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
