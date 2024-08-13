FROM apache/airflow:2.4.3-python3.10

COPY ./requirements.txt ./
COPY ./scripts/entrypoint.sh ./
# COPY ./config ./config

USER root

RUN echo 'deb http://deb.debian.org/debian bookworm main' > /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        tree \
        build-essential \
        gcc-12 \
        g++-12 \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 100 \
    && sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 100

USER airflow

# ARG PIP_EXTRA_INDEX_URL
RUN pip install --no-cache-dir --user -r ./requirements.txt

ENTRYPOINT [ "bash", "./entrypoint.sh" ]
CMD [ "--help" ]