Many-TopicNode test channel
===========================

This is a ricecooker test channel with with 10k+ content nodes (mostly TopicNodes).


Requirements
------------
Before running the chef make sure you have the following files in the `content` dir


    content/
    └── ricecooker-channel-files
        ├── Wave_particle_duality.mp4
        ├── Whale_sounds.mp3
        ├── commonlit_the-supreme-court-s-ruling-in-brown-vs-board-of-education_student.pdf
        ├── html5_react.jpg
        └── html5_react.zip

See the [sample-channels repo](https://github.com/learningequality/sample-channels),
specifically, [update.sh](https://github.com/learningequality/sample-channels/blob/master/channels/ricecooker_channel/update.sh).


Use case
--------
  - Generate a large tree for testing performance of studio's EXPORT channel function


Usage
-----

    ./sushichef.py -v --reset --token="studiotoken.txt"
