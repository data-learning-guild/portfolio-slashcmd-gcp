gcloud functions deploy user_search \
--runtime python37 \
--trigger-http \
--set-env-vars "SLACK_SECRET=$SLACK_SIGNING_SECRET" \
--allow-unauthenticated
