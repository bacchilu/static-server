FROM ubuntu:24.10

ENV TEST=xxx

# Create a range of users and groups during the build process
RUN for i in $(seq 1001 2000); do \
    groupadd -g $i group$i && useradd -u $i -g $i -m user$i; \
done

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]