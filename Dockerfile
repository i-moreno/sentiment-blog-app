FROM python:3.10.4

WORKDIR /code

# Upgrade pip and install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock  before installing
COPY Pipfile Pipfile.lock* /code/

# --system: installs packages into the system Python environment (rather than creating a virtualenv).
# --deploy: ensures the Pipfile.lock is used (if present) and will fail if there’s a mismatch.
#	--ignore-pipfile: ensures it only uses the lock file for consistent builds.
RUN pipenv install --system --deploy --ignore-pipfile

COPY ./app /code/app

# Expose port 80 (optional, but a good practice for clarity)
EXPOSE 80

CMD [ "fastapi", "run", "app/main.py", "--port", "80" ]