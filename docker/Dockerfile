FROM python:3.13.2
LABEL maintainer="Luca Bacchi <bacchilu@gmail.com> (https://github.com/bacchilu)"

ARG USER_ID
ARG GROUP_ID
ARG USERNAME=python
ARG GROUPNAME=python

RUN groupadd -g ${GROUP_ID} ${GROUPNAME}
RUN useradd -m -u ${USER_ID} -g ${GROUPNAME} ${USERNAME}

USER ${USERNAME}

WORKDIR /app

COPY ./src .

ENV PATH="$PATH:/home/$USERNAME/.local/bin"
RUN pip3 install -r requirements-lock.txt

EXPOSE 8000