"""
Python-Markdown Extra Extension
===============================

A compilation of various Python-Markdown extensions that imitates
[PHP Markdown Extra](http://michelf.com/projects/php-markdown/extra/).

Note that each of the individual extensions still need to be available
on your PYTHONPATH. This extension simply wraps them all up as a
convenience so that only one extension needs to be listed when
initiating Markdown. See the documentation for each individual
extension for specifics about that extension.

In the event that one or more of the supported extensions are not
available for import, Markdown will issue a warning and simply continue
without that extension.

There may be additional extensions that are distributed with
Python-Markdown that are not included here in Extra. Those extensions
are not part of PHP Markdown Extra, and therefore, not part of
Python-Markdown Extra. If you really would like Extra to include
additional extensions, we suggest creating your own clone of Extra
under a differant name. You could also edit the `extensions` global
variable defined below, but be aware that such changes may be lost
when you upgrade to any future version of Python-Markdown.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import str
from . import Extension
from ..blockprocessors import BlockProcessor
from .. import util
import re

extensions = ['smart_strong',
              'fenced_code',
              'footnotes',
              'attr_list',
              'def_list',
              'tables',
              'abbr',
              ]


class ExtraExtension(Extension):
    """ Add various extensions to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """ Register extension instances. """
        md.registerExtensions(extensions, self.config)
        if not md.safeMode:
            # Turn on processing of markdown text within raw html
            md.preprocessors['html_block'].markdown_in_raw = True
            md.parser.blockprocessors.add('markdown_block',
                                          MarkdownInHtmlProcessor(md.parser),
                                          '_begin')
            md.parser.blockprocessors.tag_counter = -1
            md.parser.blockprocessors.contain_span_tags = re.compile(
                r'^(p|h[1-6]|li|dd|dt|td|th|legend|address)$', re.IGNORECASE)


def makeExtension(configs={}):
    return ExtraExtension(configs=dict(configs))


class MarkdownInHtmlProcessor(BlockProcessor):
    """Process Markdown Inside HTML Blocks."""
    def test(self, parent, block):
        return block == util.TAG_PLACEHOLDER % \
            str(self.parser.blockprocessors.tag_counter + 1)

    def _process_nests(self, element, block):
        """Process the element's child elements in self.run."""
        # Build list of indexes of each nest within the parent element.
        nest_index = []  # a list of tuples: (left index, right index)
        i = self.parser.blockprocessors.tag_counter + 1
        is_nest = self.parser.markdown.htmlStash.tag_data[i]['left_index']
        while len(self.parser.markdown.htmlStash.tag_data) > i and is_nest:
            left_child_index = \
                self.parser.markdown.htmlStash.tag_data[i]['left_index']
            right_child_index = \
                self.parser.markdown.htmlStash.tag_data[i]['right_index']
            nest_index.append((left_child_index - 1, right_child_index))
            i += 1

        # Create each nest subelement.
        for i, (left_index, right_index) in enumerate(nest_index[:-1]):
            self.run(element, block[left_index:right_index],
                     block[right_index:nest_index[i + 1][0]], True)
        self.run(element, block[nest_index[-1][0]:nest_index[-1][1]],  # last
                 block[nest_index[-1][1]:], True)                      # nest

    def run(self, parent, blocks, tail=None, nest=False):
        self.parser.blockprocessors.tag_counter += 1
        tag_data = self.parser.markdown.htmlStash.tag_data[
            self.parser.blockprocessors.tag_counter]

        # Create Element
        markdown_value = tag_data['attrs'].pop('markdown')
        element = util.etree.SubElement(parent, tag_data['tag'],
                                        tag_data['attrs'])

        # Slice Off Block
        if nest:
            self.parser.parseBlocks(parent, tail)  # Process Tail
            block = blocks[1:]
        else:  # includes nests since a third level of nesting isn't supported
            block = blocks[tag_data['left_index'] + 1:
                           tag_data['right_index']]
            del blocks[:tag_data['right_index']]

        # Process Text
        if (self.parser.blockprocessors.contain_span_tags.match(  # Span Mode
                tag_data['tag']) and markdown_value != 'block') or \
                markdown_value == 'span':
            element.text = '\n'.join(block)
        else:                                                     # Block Mode
            i = self.parser.blockprocessors.tag_counter + 1
            if len(self.parser.markdown.htmlStash.tag_data) > i and self.\
                    parser.markdown.htmlStash.tag_data[i]['left_index']:
                first_subelement_index = self.parser.markdown.htmlStash.\
                    tag_data[i]['left_index'] - 1
                self.parser.parseBlocks(
                    element, block[:first_subelement_index])
                if not nest:
                    block = self._process_nests(element, block)
            else:
                self.parser.parseBlocks(element, block)
