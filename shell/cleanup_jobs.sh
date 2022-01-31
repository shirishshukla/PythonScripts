####
## This will delete all folders in DIR2CLEAN but keep last 20 latest modified.
## Schedule as cron
#- login as root and set as daily at 9:30 am
#  mkdir /root/bin
#  vi /root/bin/jobcleanup.sh
#  chmod 755 /root/bin/jobcleanup.sh
#  crontab -e ## add below line at end
#  30 09 * * * /bin/bash /root/bin/jobcleanup.sh | logger -t CLEANUP_SCRIPT
# *
####
RETENTION=20
TMPFILE=`mktemp -u`
DIR2CLEAN=/var/lib/jenkins/jobs/mytestjob
ls -lrthd "${DIR2CLEAN}"/* | awk '{print $NF}' > ${TMPFILE}.1
tail -n $RETENTION ${TMPFILE}.1 > ${TMPFILE}.2
DIRS2DEL=$(diff ${TMPFILE}.1 ${TMPFILE}.2 | awk '/^</ {print $NF}')
if [ ! -z $DIRS2DEL ]; then
    echo "Deleting ...below directories..."
    for DIR2DEL in $(echo $DIRS2DEL); do
        ls -ld "${DIR2DEL}" && rm -rf "${DIR2DEL}" || true
    done
else
    echo "Nothing to delete.."
fi
rm -rf ${TMPFILE}*
