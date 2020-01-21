FROM python:slim

RUN pip install poetry
RUN poetry config virtualenvs.create false


COPY poetry.lock pyproject.toml /

RUN poetry install

COPY structlog_to_seq /structlog_to_seq
COPY structlog_example.py /structlog_example.py


ENV PYTHONPATH /

CMD ["python",  "./structlog_example.py"]
