#!/bin/bash
# Initialize Studio instance (assumes all commands are idempotent) Are they?
set -e

if [ ! -z ${STUDIO_FIXTURES} ] ; then
    echo "Loading" "$STUDIO_FIXTURES" "TODO<<<<<<"
fi




cd /contentcuration

# Initialize application: migrate, collectstatic, crowdin messages
################################################################################
# migrate
# python contentcuration/manage.py makemigrations
python contentcuration/manage.py migrate || true
# collectstatic
python contentcuration/manage.py collectstatic --noinput
python contentcuration/manage.py collectstatic_js_reverse
python contentcuration/manage.py loadconstants
# crowdin messages
ls -l crowdin-cli.jar || curl -L https://storage.googleapis.com/le-downloads/crowdin-cli/crowdin-cli.jar -o crowdin-cli.jar
java -jar crowdin-cli.jar download
python contentcuration/manage.py compilemessages
# ???
# python contentcuration/manage.py calculateresources --init




exec "$@"


