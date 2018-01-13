#!/bin/bash
# Setup script for creting kolibri facility admin user `devowner:admin123`
set -eo pipefail


generate_post_data()
{
  cat <<EOF
{
  "facility": {
    "name": "$KOLIBRI_DEVICEPROVISION_FACILTY_NAME"
  },
  "preset": "$KOLIBRI_DEVICEPROVISION_PRESETS",
  "superuser": {
    "username": "$KOLIBRI_DEVICEPROVISION_SUPERUSER_USERNAME",
    "password": "$KOLIBRI_DEVICEPROVISION_SUPERUSER_PASSWORD"
  },
  "language_id": "$KOLIBRI_LANG"
}
EOF
}


echo "Setting up facility using POST to /api/deviceprovision/ with POST --data="
echo "$(generate_post_data)"
curl -i \
  -H "Content-Type:application/json" \
  --data "$(generate_post_data)" \
  -X POST "http://localhost:$KOLIBRI_PORT/api/deviceprovision/"
