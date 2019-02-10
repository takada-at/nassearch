FUNCTION=$1
GCLOUD=$HOME/google-cloud-sdk/bin/gcloud

cd ./functions/${FUNCTION}
${GCLOUD} functions deploy ${FUNCTION} \
       --region=asia-northeast1 \
       --runtime=python37 \
       --trigger-resource=tkd-nas-data \
       --trigger-event=google.storage.object.finalize
