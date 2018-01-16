End-to-end testing design
=========================
The goal of this project is to develop a framework for running system tests that
check the Kolibri platform works as expected.

  - Test scenarios and test components are stored in the folder `checks/`
  - Test server landscape provisioning is defined by docker compose files in the
    `landscapes/` directory. These in turn depend on
      - Dockerfiles server provisioning is `dockerfiles/`
      - Server provisioning scripts in `dockerfiles/scripts/`
      - Fixtures in `fixtures/`
      - Build assets in `build/`



Strategy
--------
The testing matrix (testing tensor) has the following dimensions:
  - Version of `ricecooker`
  - Version of `kolibri` used
  - Packaging method for `kolibri` (src, pip, pex, whl, deb)
  - Linux variants ([Debian, Ubuntu 14.04, 16.04, 17.04, 17.10]()
    Can't use docker for MAC, WIN, ANDROID so will need a new provision/scripting approach.
  - Version of Python used for `kolibri` (py27, py34, py35, py36)
    See [current state](https://docs.google.com/spreadsheets/d/1CAzop-fEZyF-mra9ByJRWHqg4irco1MrTArcJKM8P-4/edit#gid=0) .
  - Version of `studio` used
  - TODO: version of Python used for `studio` (py27, py35, py36)

The full suite of end-to-end checks for a particular combination of version in the
testing tensor could take 1h/2h and can be performed on a daily basis.
Running the full checks suite on all possible combinations can take days.
Assume checks are performed spare server capacity: home servers contributed by LE staff.



Technological uncertainties
---------------------------

  - passing commands from fabric to inside containers
  - accessing files inside containers from fabric
    - copy db file to volume on docker host and connect to it there?
      save in `YYYYMMDD-hhmm-{landscape}-{checkname}/`
  - implement common layer to compare yaml/json, SQL dumps, and sqlite API calls
    that supports set rel'ns and equality testing
     - list of dicts?
     - list of named tuples?






Software components
-------------------

    src/
      kolibri/     # clone of <account>/kolibri with checkout of branch/pr#/tag/commit
      studio/      # clone of fle-internal/content-curation with checkout of branch/pr#/tag/commit
      ricecooker/  # clone of learnignequality/ricecooker
      sushibar/    # clone of fle-internal/sushibar

    build/
      kolibri/
        kolibri-0.7.0.pex   # pre-built pex files
        kolibri-0.8.0.pex
        kolibri-0.7.0.whl ?
        kolibri-0.7.0.deb ?




Infrastructure checks
---------------------
In addition to software checks, the correct operation of the Kolibri ecosystem
requires a number of infrastructure components:

  - Check production Kolibri Studio server is up and responsive
  - Perform DNS checks for all world-facing LE systems
    (see [checks/infrastructure/dnschecks.py](../checks/infrastructure/dnschecks.py)

Can perform these as part of [release process](https://docs.google.com/document/d/1Z06ING-sgMoq5EqZPVK2Zu1cUIpF9SKJunG17Q8Fcr8/edit#heading=h.2au4supzswn5).




State
-----
Filesystem state and scripting for the checks is provided by different layers:

  - Docker image build time (specified as a `Dockerfile`)
  - First-run time: docker container init script (ENTRYPOINT)
      - Kolibri-only: Download
      - Initialize application: migrate, buildstatic
      - Load initial data: deviceprovision, loadconstants, create admin user, importchannels
  - Runtime: when `kolibri` starts (CMD)
      - Koibri internal checks every time Kolibri starts
  - Docker `exec` commands (called from Fabric scripts to perform actual tests)
      - importchannel
      - generate user data
      - loaddata
      - `django-admin dumpdata [app_label[.ModelName] [app_label[.ModelName] ...]]`
      - `equal_tables(db1, table1, db2, table2, ignore_cols=['uuid', 'created_at', '…'])`
      - `equal_results(db1, query1, db2, query2)`
      - `equal_count(db1, query1, db2, query2)` (assume COUNT statement that returns an int)
      - `contains_table(db1, table1, db2, table2, ignore_cols=['uuid', 'created_at', '…'])`

Configuration is managed by setting environment variables
  - credentials end
  - landscape-specific env
  - in the docker-compose.yml file for this landscape
  - in the docker-compose.ovveride.yml with customizations for current check script



Dockerfiles
-----------
Define basic ubuntu-based image with all necessary packages installed and dirs created.



Startup scripts
---------------
When docker starts a container, the "init" chain is as follows:

    /scripts/<appname>/entrypoint.sh  --exec-->  kolibri start --foreground --port=80

The process that will actually run as PID 1 inside the container will be kolibri,
but the entrypoint script performs makes sure Kolibri is installed and initialized.



Checks as `fabfile` tasks
-------------------------
See [fabfile.py][../fabfile.py] for POC end-to-end scripted checks.




