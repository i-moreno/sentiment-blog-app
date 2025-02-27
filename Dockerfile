FROM public.ecr.aws/lambda/python:3.10

# Install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Copy the entire `app` folder into /code/app
COPY ./app /var/task/app

# Copy Pipfile and install dependencies
COPY Pipfile Pipfile.lock* ./
RUN pipenv install --system --deploy --ignore-pipfile

# (Optional) Expose port 80 for local runs
EXPOSE 80

# Reference the `handler` in `app/main.py`
CMD ["app.main.handler"]