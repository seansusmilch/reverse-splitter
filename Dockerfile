FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium && \
    playwright install-deps chromium

COPY ./setup.py /app/setup.py
COPY ./reverse_splitter /app/reverse_splitter
RUN pip install --no-cache-dir -e .

ENV TZ=Etc/UTC

RUN echo "setting timezone" && \
    echo -e '$TZ' | dpkg-reconfigure tzdata -f teletype

CMD ["python", "reverse_splitter/main.py"]