#!/bin/bash
# Initialize Studio instance (assumes all commands are idempotent) Are they?
set -e


cd /contentcuration/contentcuration


echo "\n\n\nRUNNING nslookup studiodb >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
nslookup studiodb


# Wait for studiodb host to come up
################################################################################
until psql studiodb -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"




# Initialize application: migrate, collectstatic, crowdin messages
################################################################################
if [ "x$INITIALIZE_STUDIO" = 'xon' ]; then

    # migrate
    python manage.py migrate || true
    # python manage.py makemigrations

    # collectstatic
    python manage.py collectstatic --noinput
    python manage.py collectstatic_js_reverse
    python manage.py loadconstants

    # rsrc sizes
    python manage.py calculateresources --init

    #    # crowdin messages
    #    ls -l crowdin-cli.jar || curl -L https://storage.googleapis.com/le-downloads/crowdin-cli/crowdin-cli.jar -o crowdin-cli.jar
    #    java -jar crowdin-cli.jar download
    #    python manage.py compilemessages

fi




if [ ! -z ${STUDIO_FIXTURES} ] ; then
    echo "Loading" "$STUDIO_FIXTURES" "TODO<<<<<<"
fi



exec "$@"
