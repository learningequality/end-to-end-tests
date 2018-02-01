#!/usr/bin/env python

import string
import random

from le_utils.constants import format_presets, licenses, exercises
from le_utils.constants.languages import getlang  # see also getlang_by_name, getlang_by_alpha2
from ricecooker.chefs import SushiChef
from ricecooker.classes.nodes import TopicNode

from ricecooker.classes.nodes import DocumentNode, AudioNode, VideoNode, HTML5AppNode
from ricecooker.classes.files import DocumentFile, AudioFile, VideoFile, HTMLZipFile

from ricecooker.classes.nodes import ExerciseNode
from ricecooker.classes.questions import SingleSelectQuestion, MultipleSelectQuestion, InputQuestion, PerseusQuestion

from ricecooker.classes.licenses import get_license
from ricecooker.exceptions import raise_for_invalid_channel



def make_random_subtree(parent, depth):
    for i in range(45):
        istr = str(i)
        title = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        description = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))

        typ =  random.choice("tttttttvadh")

        if typ == 't':
            topic = TopicNode(
                    source_id=title+istr,
                    title=title,
                    description=description,
                    author=None,
                    language=getlang('en').id,
                    thumbnail=None,
            )
            parent.add_child(topic)

            if depth > 0:
                make_random_subtree(topic, depth-1)


        elif typ == 'a':

            content11a = AudioNode(
                    source_id='940ac8ff'+istr,
                    title='Whale sounds',
                    author='First Last (author\'s name)',
                    description='Put file description here',
                    language=getlang('en').id,
                    license=get_license(licenses.CC_BY, copyright_holder='Copyright holder name'),
                    thumbnail=None,
                    files=[],
            )
            parent.add_child(content11a)
            audio_file = AudioFile(
                    path='./content/ricecooker-channel-files/Whale_sounds.mp3',
                    language=getlang('en').id
            )
            content11a.add_file(audio_file)


        elif typ == 'd':

            content12a = DocumentNode(
                  source_id='80b7136f'+istr,
                  title='The Supreme Court\u2019s Ruling in Brown vs. Board of Education',
                  author='First Last (author\'s name)',
                  description='Put file description here',
                  language=getlang('en').id,
                  license=get_license(licenses.CC_BY, copyright_holder='Copyright holder name'),
                  thumbnail=None,
                  files=[DocumentFile(
                                path='./content/ricecooker-channel-files/commonlit_the-supreme-court-s-ruling-in-brown-vs-board-of-education_student.pdf',
                                language=getlang('en').id
                        )]
            )
            parent.add_child(content12a)

        elif typ == 'h':

            content13a = HTML5AppNode(
                  source_id='302723b4'+istr,
                  title='Sample React app',
                  author='First Last (author\'s name)',
                  description='Put file description here',
                  language=getlang('en').id,
                  license=get_license(licenses.CC_BY, copyright_holder='Copyright holder name'),
                  thumbnail='./content/ricecooker-channel-files/html5_react.jpg',
                  files=[HTMLZipFile(
                              path='./content/ricecooker-channel-files/html5_react.zip',
                              language=getlang('en').id
                         )]
            )
            parent.add_child(content13a)

        elif type == 'v':

            content14a = VideoNode(
                    source_id='9e355995',
                    title='Wave particle duality explained in 2 mins',
                    author='First Last (author\'s name)',
                    description='Put file description here',
                    language=getlang('en').id,
                    license=get_license(licenses.CC_BY, copyright_holder='Copyright holder name'),
                    derive_thumbnail=True,  # video-specicig flag
                    thumbnail=None,
                    files=[VideoFile(
                                path='./content/ricecooker-channel-files/Wave_particle_duality.mp4',
                                language=getlang('en').id
                           )]
            )
            parent.add_child(content14a)







class SampleChef(SushiChef):
    """
    The chef class that takes care of uploading channel to Kolibri Studio.
    We'll call its `main()` method from the command line script.
    """

    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': 'source.org',                  # content provider's domain
        'CHANNEL_SOURCE_ID': 'uber-big-ricecooker-channel',       # an alphanumeric channel ID
        'CHANNEL_TITLE': 'UBERRRRRR count of topics',           # a humand-readbale title
        'CHANNEL_LANGUAGE': getlang('en').id,                   # language code of channel
        'CHANNEL_THUMBNAIL': 'http://quantlabs.net/blog/wp-content/uploads/2015/11/pythonlogo.jpg', # (optional) local path or url to image file
        'CHANNEL_DESCRIPTION': 'This channel was created from the files in the '
                               'content/ dir and the metadata provided in Python'
    }


    def construct_channel(self, *args, **kwargs):
        """
        Create ChannelNode and build topic tree.
        """
        channel = self.get_channel(*args, **kwargs)   # create ChannelNode from data in self.channel_info
        self.create_content_nodes(channel)
        raise_for_invalid_channel(channel)
        return channel


    def create_content_nodes(self, channel):
        """
        This function uses the methods `add_child` and `add_file` to build the
        hierarchy of topic nodes and content nodes. Every content node is associated
        with the underlying file node.
        """
        make_random_subtree(channel, 2)



if __name__ == '__main__':
    """
    This code will run when the sushi chef scripy is called on the command line.
    """
    chef = SampleChef()
    chef.main()
