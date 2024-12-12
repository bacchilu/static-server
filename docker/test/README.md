    docker build -t test .

    docker run --rm -it -e TEST=yyy test
    docker run --rm -it -e TEST=yyy --user 1111:1111 test