FROM python:3.11-slim-bookworm
LABEL org.opencontainers.image.authors="Slavik Svyrydiuk <slavik@svyrydiuk.eu>"
LABEL org.opencontainers.image.source https://github.com/sv0/telega
ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

WORKDIR /app

COPY requirements.txt /tmp/
RUN pip3 install \
    --quiet  \
    --no-cache-dir \
    --disable-pip-version-check \
    --requirement /tmp/requirements.txt && \
    rm -fr \
        /root/.cache \
        /usr/share/zoneinfo && \
    apt-get remove --purge --yes --allow-remove-essential \
        e2fsprogs \
        perl-base \
        bsdutils
COPY . /app
EXPOSE 8000
CMD [ \
    "uvicorn", \
    "telega.app:app", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--log-level", "debug" \
]
