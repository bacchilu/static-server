FROM python:3.14.0
LABEL maintainer="Luca Bacchi <bacchilu@gmail.com> (https://github.com/bacchilu)"

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG USERNAME=python
ARG GROUPNAME=python

RUN groupadd -g ${GROUP_ID} ${GROUPNAME}
RUN useradd -m -u ${USER_ID} -g ${GROUPNAME} ${USERNAME}

USER ${USERNAME}

WORKDIR /app

COPY ./requirements-lock.txt ./requirements-lock.txt
COPY ./requirements.txt ./requirements.txt

ENV PATH="$PATH:/home/$USERNAME/.local/bin"
RUN pip3 install -r requirements-lock.txt

COPY ./src .

CMD ["fastapi", "run", "app/main.py"]

EXPOSE 8000
