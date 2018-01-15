#!/bin/bash
# Initialize Studio instance (assumes all commands are idempotent) Are they?
set -e

if [ ! -z ${STUDIO_FIXTURES} ] ; then
    echo "Loading" "$STUDIO_FIXTURES" "TODO<<<<<<"
fi


echo "\n\n\nRUNNING nslookup studiodb >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
echo nslookup studiodb





cd /contentcuration/contentcuration

# Initialize application: migrate, collectstatic, crowdin messages
################################################################################
# migrate
# python manage.py makemigrations
python manage.py migrate || true
# collectstatic
python manage.py collectstatic --noinput
python manage.py collectstatic_js_reverse
python manage.py loadconstants

#    # crowdin messages
#    ls -l crowdin-cli.jar || curl -L https://storage.googleapis.com/le-downloads/crowdin-cli/crowdin-cli.jar -o crowdin-cli.jar
#    java -jar crowdin-cli.jar download
#    python manage.py compilemessages

# ???
# python manage.py calculateresources --init



exec "$@"
