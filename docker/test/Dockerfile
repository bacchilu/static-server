FROM busybox

ENV TEST=xxx

CMD ["sh", "-c", "USER_ID=$(id -u) GROUP_ID=$(id -g); echo $TEST, $PATH, [userid $USER_ID], [groupid $GROUP_ID]"]