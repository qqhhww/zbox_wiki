#!/usr/bin/env python

"""
Trac - Syntax Coloring of Source Code
- http://trac.edgewall.org/wiki/TracSyntaxColoring
"""

import os
import re

from markdown import markdown as _markdown
import markdown_plus
import zlatex
from zpath import convert_path_to_hierarchy

osp = os.path

__all__ = ["convert_static_file_url",
           "convert_path_to_hierarchy",
           "convert_text_path_to_button_path",
           "trac_wiki_code_block_to_markdown_code",
           "convert_latex_code",
           "markdown"]


def trac_wiki_code_block_to_markdown_code(text):
    alias_p = '[a-zA-Z0-9#\-\+ \.]'
    shebang_p = '(?P<shebang_line>[\s]*#!%s{1,21}[\s]*?)' % alias_p

    code_p = '(?P<code>[^\f\v]+?)'

    code_block_p = "^\{\{\{[\s]*%s*%s[\s]*\}\}\}" % (shebang_p, code_p)
    code_block_p_obj = re.compile(code_block_p, re.MULTILINE)

    def code_repl(match_obj):
        code = match_obj.group('code')
        buf = "\n    ".join(code.split(os.linesep))
        buf = "    %s" % (buf)
        return buf

    return code_block_p_obj.sub(code_repl, text)

def convert_latex_code(text, save_to_prefix):
    shebang_p = "#![lL]atex"
    code_p = '(?P<code>[^\f\v]+?)'
    code_block_p = "^\{\{\{[\s]*%s*%s[\s]*\}\}\}" % (shebang_p, code_p)
    code_block_p_obj = re.compile(code_block_p, re.MULTILINE)

    def code_repl(match_obj):
        code = match_obj.group('code')
        png_filename = zlatex.latex2png(text=code, save_to_prefix=save_to_prefix)

        return "![%s](%s)" % (png_filename, png_filename)

    return code_block_p_obj.sub(code_repl, text)

# def hook_pre_rm_latex_code(text, save_to_prefix):
#     """ Call this hook before delete page file,
#     this hook will remove all image files generated by convert_latex_code().
#     """
#     shebang_p = "#![lL]atex"

#     code_p = '(?P<code>[^\f\v]+?)'

#     code_block_p = "^\{\{\{[\s]*%s*%s[\s]*\}\}\}" % (shebang_p, code_p)
#     code_block_p_obj = re.compile(code_block_p, re.MULTILINE)

#     def code_repl(match_obj):
#         code = match_obj.group('code')
#         png_filename = zlatex.latex2png(text=code, save_to_prefix=save_to_prefix)

#         fullpath = osp.join(save_to_prefix, i)
#         os.remove(fullpath)

#         return "![%s](%s)" % (png_filename, png_filename)

#     return code_block_p_obj.sub(code_repl, text)


def _fix_img_url(text, static_file_prefix = None):
    """
        >>> text = '![blah blah](20100426-400x339.png)'
        >>> static_file_prefix = '/static/files/'
        >>> _fix_img_url(text, static_file_prefix)
        '![blah blah](/static/files/20100426-400x339.png)'
    """
    def img_url_repl(match_obj):
        img_alt = match_obj.group("img_alt")
        img_url = match_obj.group("img_url")
        if static_file_prefix:
            fixed_img_url = osp.join(static_file_prefix, img_url)
            return '![%s](%s)' % (img_alt, fixed_img_url)
        else:
            return '![%s](%s)' % (img_alt, img_url)

    img_url_p = r"!\[(?P<img_alt>.+?)\]\((?P<img_url>[^\s]+?)\)"
    img_url_p_obj = re.compile(img_url_p, re.MULTILINE)
    return img_url_p_obj.sub(img_url_repl, text)

def _fix_img_url_with_option(text, static_file_prefix = None):
    """
        >>> text = '![blah blah](20100426-400x339.png "png title")'
        >>> static_file_prefix = '/static/files/'
        >>> _fix_img_url_with_option(text, static_file_prefix)
        '![blah blah](/static/files/20100426-400x339.png "png title")'
    """
    def img_url_repl(match_obj):
        img_alt = match_obj.group('img_alt')
        img_url = match_obj.group('img_url')
        img_title = match_obj.group('img_title')
        if static_file_prefix:
            fixed_img_url = osp.join(static_file_prefix, img_url)
            return '![%s](%s "%s")' % (img_alt, fixed_img_url, img_title)
        else:
            return '![%s](%s "%s")' % (img_alt, img_url, img_title)

    img_url_p = r"!\[(?P<img_alt>.+?)\]\((?P<img_url>[^\s]+?)\s\"(?P<img_title>.+?)\"\)"
    img_url_p_obj = re.compile(img_url_p, re.MULTILINE)
    return img_url_p_obj.sub(img_url_repl, text)

def convert_static_file_url(text, static_file_prefix):
    text = _fix_img_url(text, static_file_prefix)
    text = _fix_img_url_with_option(text, static_file_prefix)
    return text

def convert_text_path_to_button_path(path):
    buf = convert_path_to_hierarchy(path)
    IS_ONLY_ONE_LEVEL = len(buf) == 1
    button_path = " / ".join(["[%s](%s/)" % (i[0], i[1]) for i in buf[:-1]])

    latest_level = buf[-1]
    path_name = latest_level[0]

    if IS_ONLY_ONE_LEVEL:
        button_path = path_name
    else:
        button_path = "%s / %s" % (button_path, path_name)

    return button_path

def markdown(text, work_fullpath = None, static_file_prefix = None):
    buf = text    
    
    if work_fullpath:
        try:
            buf = convert_latex_code(buf, save_to_prefix=work_fullpath)
        except Exception:
            print "it seems that latex or dvipng doesn't works well on your box"

    if static_file_prefix:
        buf = convert_static_file_url(buf, static_file_prefix)


    buf = markdown_plus.parse_table(buf)    
    buf = trac_wiki_code_block_to_markdown_code(buf)

    buf = _markdown(buf)
    
    return buf

if __name__ == "__main__":
    import doctest
    doctest.testmod()
