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

COPY ./src .

ENV PATH="$PATH:/home/$USERNAME/.local/bin"
RUN pip3 install -r requirements-lock.txt

CMD ["fastapi", "run", "main.py"]

EXPOSE 8000
