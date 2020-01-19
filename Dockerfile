FROM python:slim

RUN pip install poetry
RUN poetry config virtualenvs.create false


COPY poetry.lock pyproject.toml /

RUN poetry install

COPY structlog_to_seq /structlog_to_seq
COPY tests/structlog_test.py /structlog_test.py


ENV PYTHONPATH /

CMD ["python",  "./structlog_test.py"]
