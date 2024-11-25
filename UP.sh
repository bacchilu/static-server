docker build -t static-server:dev --build-arg USER_ID=`id -u` --build-arg GROUP_ID=`id -g` .
docker run --rm -it -p 8000:8000 -v ./src/:/app static-server:dev