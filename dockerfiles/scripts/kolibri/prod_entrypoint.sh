#!/bin/bash
# Initialize Kolibri instance if not initialized already
set -e


if [ -z ${var+x} ]; then
    echo "var is unset";
else
    echo "var is set to '$var'";
fi


if [ ! -z ${KOLIBRI_PEX_PATH} ] && [ -f "$KOLIBRI_PEX_PATH" ] && [ ! -f /kolibrihome/kolibri.pex ] ; then
    cp "$KOLIBRI_PEX_PATH" /kolibrihome/kolibri.pex
fi

if [ ! -f /kolibrihome/kolibri.pex ]; then
    wget --no-verbose "$KOLIBRI_PEX_URL" -O /kolibrihome/kolibri.pex
fi


if [ ! -f /kolibrihome/kolibri_settings.json ]; then
    echo "RUnnigg /kolibrihome/kolibri.pex language setdefault $KOLIBRI_LANG"
    python /kolibrihome/kolibri.pex language setdefault $KOLIBRI_LANG
    echo "\n\nTemporarily starting Kolibri to run deficeprovision.sh ..."
    python /kolibrihome/kolibri.pex start --foreground --port=$KOLIBRI_PORT &
    echo $! >/tmp/deficeprovision_kolibri.pid
    sleep 5
    /scripts/kolibri/deviceprovision.sh
    kill -9 `cat /tmp/deficeprovision_kolibri.pid`
    rm /tmp/deficeprovision_kolibri.pid
    sleep 1
    echo "deviceprovision.sh done"
fi


if [ ! -z ${CHANNELS_TO_IMPORT} ]; then
    echo 'Importing channels $CHANNELS_TO_IMPORT'
    cd /kolibrihome
    for channel_id in $(echo "$CHANNELS_TO_IMPORT" | sed "s/,/ /g"); do
        python /kolibrihome/kolibri.pex manage importchannel network $channel_id
        python /kolibrihome/kolibri.pex manage importcontent network $channel_id
        echo "Channel $channel_id finished importing"
    done
fi



# until psql $DATABASE_URL -c '\l'; do
#   >&2 echo "Postgres is unavailable - sleeping"
#   sleep 1
# done
#
# >&2 echo "Postgres is up - continuing"
#
# if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
#     /venv/bin/python manage.py migrate --noinput
# Fi
#
# if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
#     /venv/bin/python manage.py collectstatic --noinput
# fi


exec "$@"
