FROM python:3.13.0
LABEL maintainer="Luca Bacchi <bacchilu@gmail.com> (https://github.com/bacchilu)"

ARG USER_ID
ARG GROUP_ID
ARG UPLOAD_DIRECTORY=/tmp/uploads
ARG USERNAME=python

ENV UPLOAD_DIRECTORY=${UPLOAD_DIRECTORY}

RUN groupadd -g ${GROUP_ID} ${USERNAME}
RUN useradd -ms /bin/bash -l -u ${USER_ID} -g ${USERNAME} ${USERNAME}
RUN install -d -m 0755 -o ${USERNAME} -g ${USERNAME} /home/${USERNAME}

USER ${USERNAME}

WORKDIR /app

COPY ./src .

ENV PATH="/home/$USERNAME/.local/bin:$PATH"
RUN pip3 install -r requirements-lock.txt

EXPOSE 8000