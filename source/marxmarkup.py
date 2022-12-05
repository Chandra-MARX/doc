'''Custom Sphinx extension for MARX

'''

import re
from itertools import groupby
import csv
import codecs

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.domains import ObjType, Index
from sphinx.directives import ObjectDescription
from sphinx.directives.code import LiteralInclude
from sphinx.directives.code import dedent_lines
from sphinx.util.docfields import TypedField
from sphinx.domains.std import GenericObject, StandardDomain


def indent_lines(lines, indent):
    if not indent:
        return lines

    if indent[0] == '"' and indent[-1] == '"':
        indent = indent[1:-1]

    return [indent + l for l in lines]


class SourceIncludeDirective(LiteralInclude):
    """
    Like ``.. literalinclude:: :literal:``, but adds indent option.
    """
    option_spec = {
        'dedent': int,
        'indent': directives.unchanged,
        'linenos': directives.flag,
        'lineno-start': int,
        'lineno-match': directives.flag,
        'tab-width': int,
        'language': directives.unchanged_required,
        'encoding': directives.encoding,
        'pyobject': directives.unchanged_required,
        'lines': directives.unchanged_required,
        'start-after': directives.unchanged_required,
        'end-before': directives.unchanged_required,
        'prepend': directives.unchanged_required,
        'append': directives.unchanged_required,
        'emphasize-lines': directives.unchanged_required,
        'caption': directives.unchanged,
        'name': directives.unchanged,
        'diff': directives.unchanged_required,
    }

    def read_with_encoding(self, filename, document, codec_info, encoding):
        f = None
        try:
            f = codecs.StreamReaderWriter(open(filename, 'rb'), codec_info[2],
                                          codec_info[3], 'strict')
            lines = f.readlines()
            lines = dedent_lines(lines, self.options.get('dedent'))
            lines = indent_lines(lines, self.options.get('indent'))
            return lines
        except (IOError, OSError):
            return [document.reporter.warning(
                'Include file %r not found or reading it failed' % filename,
                line=self.lineno)]
        except UnicodeError:
            return [document.reporter.warning(
                'Encoding %r used for reading included file %r seems to '
                'be wrong, try giving an :encoding: option' %
                (encoding, filename))]
        finally:
            if f is not None:
                f.close()


class MARXtool(ObjectDescription):
    """
    Description of a MARX tool or script.
    """
    option_spec = {
        'noindex': directives.flag,
        'language': directives.unchanged,
        'annotation': directives.unchanged,
    }

    doc_field_types = [
        TypedField('options', label='Options',
                   names=('param', 'parameter', 'arg', 'argument',
                          'keyword', 'kwarg', 'kwparam', 'option'),
                   typerolename='obj', typenames=('paramtype', 'type'),
                   can_collapse=True),
    ]

    indextext = '%s; MARX tool'

    def needs_arglist(self):
        """May return true if an empty argument list is to be generated even if
        the document contains none.
        """
        return False

    def handle_signature(self, sig, signode):
        match = re.search('(\w+)', sig)
        name = match.groups()[0]
        # At this point, we make no attempt to break up the arglist into
        # reqired parameters, keywords, optional arguments etc.
        # This would be very hard, since we would have to cover the syntax
        # of shell, IDL, S-Lang, ...
        # For our output all we want is to attach it to the name in
        # reasonable formatting.
        arglist = sig[len(name):]

        anno = self.options.get('annotation')
        lang = self.options.get('language')

        signode += addnodes.desc_name(name, name)
        # addname has a good formatting, even if it is meant for a
        # different use in sphinx for python.
        # Sphinx expects name + parameterlist, but unfortunately,
        # the parameterlist is automatically wrapped in (), so we avoid that
        # here.
        signode += addnodes.desc_addname(arglist, arglist)

        if lang:
            signode += addnodes.desc(' ' + lang, ' ' + lang)
        if anno:
            signode += addnodes.desc_annotation(' ' + anno, ' ' + anno)
        return name

    def add_target_and_index(self, name, sig, signode):
        if name not in self.state.document.ids:
            signode['ids'].append(name)
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['std']['objects']
            if name in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % name +
                    'other instance in ' +
                    self.env.doc2path(objects[name][0]) +
                    ', use :noindex: for one of them',
                    line=self.lineno)
            objects['marxtool', name] = (self.env.docname, name)

        indextext = self.indextext % name
        self.indexnode['entries'].append(('pair', indextext, name, '', None))


class MARXpost(MARXtool):
    indextext = '%s; post-processing'


def ciao_reference_role(role, rawtext, text, lineno, inliner,
                        options={}, content=[]):
    '''Automatically construct the right URL for a CIAO tool'''
    ref = "http://cxc.harvard.edu/ciao/ahelp/{0}.html".format(text.strip())
    node = nodes.reference(rawtext, text, refuri=ref, **options)
    return [node], []


class Parameter(GenericObject):
    '''MARX parameter

    This class masked use of the ``config.par`` variable called
    ``marxmarkup_marxparpath``. It parses the ``marx.par`` file at that
    location and automatically adds the default value to the parameter
    description. (If no description is given for the parameter, then it also
    adds the description from ``marx.par``.
    '''
    # use this line to make them show up in general index
    # indextemplate = 'pair: %s; MARX parameter'
    # use this line to NOT have them in general index
    indextemplate = ''
    marxpar = None

    def read_marxpar(self):
        parfile = self.env.config['marxmarkup_marxparpath']
        if parfile is not None:
            # This is a class attribute so that all parameters can share this
            # dictionary. Otherwise, the marx.par would have to be read and
            # parsed again for every single Parameter instance.
            self.__class__.marxpar = {}
            try:
                with open(parfile, 'r') as f:
                    for row in csv.reader(f):
                        if not row[0][0] == '#':
                            self.__class__.marxpar[row[0]] = (row[3], row[6])
            except IOError as e:
                self.env.warn('config.py', 'marx.par could not be loaded - {0}'.format(str(e)))

    def before_content(self):
        # This is a little hacky way of modifying the content, but I did
        # not find anything better.
        if self.marxpar is None:
            self.read_marxpar()

        if self.names[0] in self.marxpar:
            pardesc = self.marxpar[self.names[0]]
            if len(self.content) == 0:
                self.content.data = ['(*default*: ``{0}``) {1}'.format(*pardesc)]
            else:
                self.content[0] = '(*default*: ``{0}``) '.format(pardesc[0]) + self.content[0]


class ParRole(XRefRole):
    """Role that recognizes MARX parameters in expressions like ``par=5``"""
    def process_link(self, env, refnode, has_explicit_title, title, target):
        """Called after parsing title and target text, and creating the
        reference node (given in *refnode*).  This method can alter the
        reference node and must return a new (or the same) ``(title, target)``
        tuple.
        """
        return title, target.split('=')[0].strip()


class MARXParIndex(Index):
    """
    Index subclass to provide the MARX Parameter index.

    MARXParIndex reads a the ``config.par`` variable called
    ``marxmarkup_marxparpath`` and parses the ``marx.par`` file at that
    location. Short descriptions of the parameters and their default values are
    read from this file and included in the generated parameter index.
    Furthermore, the parameter index tests that all documented parameters have
    a counterpart in ``marx.par`` and the all parameters in ``marx.par`` are
    documented in the source at some point.
    """

    name = 'parindex'
    localname = 'MARX Parameter Index'
    shortname = 'MARX Parameters'

    def read_marxpar(self):
        parfile = self.domain.env.config['marxmarkup_marxparpath']
        if parfile is None:
            self.marxpar = None
        else:
            self.marxpar = {}
            try:
                with open(parfile, 'r') as f:
                    for row in csv.reader(f):
                        if not row[0][0] == '#':
                            self.marxpar[row[0]] = (row[3], row[6])
            except IOError as e:
                self.domain.env.warn('config.py', 'marx.par could not be loaded - {0}'.format(str(e)))


    def generate(self, docnames=None):
        if not hasattr(self, "marxpar"):
            self.read_marxpar()
        entries = []
        objects = self.domain.data.get('objects', [])
        parameters = [o for o in objects if o[0] == 'parameter']
        for p in parameters:
            docname, anchor = objects[p]
            # can use this for more info, e.g.
            # a = one line description of par
            # b = 'default'
            # c = value for default from default file
            #     (I need to check how MARX determines the default)
            # entries.append([p[1], 0, docname, anchor, 'a', 'b', 'c'])
            if self.marxpar is None:
                entries.append([p[1], 0, docname, anchor, '', '', ''])
            else:
                if p[1] in self.marxpar:
                    m = self.marxpar[p[1]]
                else:
                    self.domain.env.warn(docname, 'Marx parameter {0} encountered, but no equivalent parameter found in {1}'.format(p[1], self.domain.env.config['marxmarkup_marxparpath']))
                    m = ('', '')
                entries.append([p[1], 0, docname, anchor, m[1], 'default', m[0]])
        # sort alphabetically, without "key" upper and lower case would
        # be separate
        entries = sorted(entries, key=lambda x: x[0].upper())
        content = []
        # key can be anything!
        for k, g in groupby(entries, key=lambda x: x[0][0].upper()):
            content.append((k, list(g)))

        # This routine gets called multiple times in the build process,
        # sometimes with no content.
        # I don't know why, but if it does this emits useless warnings.
        if (len(content) > 0) and (self.marxpar is not None):
            missingpars = set(self.marxpar.keys()) - set([o[1] for o in parameters])
            if len(missingpars) > 0:
                # parameters that are documented, but don't exist in the
                # marx.par file are called out above one by one.
                # Here, report parameters in marx.par that are undocumented.
                self.domain.env.warn(str(self), 'The following parameters exist in {0}, but are not mentioned in the rst docs: {1}'.format(self.domain.env.config['marxmarkup_marxparpath'], missingpars))

        return content, False


def setup(app):
    app.add_directive('sourceinclude', SourceIncludeDirective)

    app.add_config_value('marxmarkup_marxparpath', None, 'env')

    app.add_directive('marxtool', MARXtool)
    StandardDomain.object_types['marxtool'] = ObjType('marxtool', 'marxtool')
    # (objname or directivename, rolename)
    StandardDomain.roles['marxtool'] = XRefRole(warn_dangling=True)

    app.add_directive('marxpost', MARXpost)
    StandardDomain.object_types['marxpost'] = ObjType('marxpost', 'marxtool')
    StandardDomain.roles['marxpost'] = XRefRole(warn_dangling=True)

    app.add_role('ciao', ciao_reference_role)

    app.add_directive('parameter', Parameter)
    StandardDomain.object_types['parameter'] = ObjType('parameter', 'par')

    StandardDomain.roles['par'] = ParRole()

    app.add_index_to_domain('std', MARXParIndex)
    StandardDomain.initial_data['labels']['parindex'] = ('std-parindex', '', 'Marx Parameters')
    StandardDomain.initial_data['anonlabels']['parindex'] = ('std-parindex', '')
