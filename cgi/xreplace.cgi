#!/usr/bin/env python

from URLtools360 import valid360URL
import os, cgi, re

import commands
import cgitb
cgitb.enable()
alpha=True # debug print flag
alpha = False
tabAction = " "
dubQuote = '"'
singleQuote = "'"

print "Content-type: text/html\n\n"


query = os.environ.get('QUERY_STRING')
arguments = cgi.parse_qs(query) if query else {}

if alpha:
    print "The arguments are: <BR>\n" 
    print arguments
    print "<BR>\n"

# We don't expect to be passed arguments. 
# Rather, we'll take our direction from a form.

objectSource = cgi.FieldStorage()
source = objectSource.getfirst("source-orig")


if alpha:
    print "The URL is:<BR>" 
    print source
    print "<BR>\n"

    print "The  tab behavior is:<BR>" 
    print tabAction
    print "<BR>\n"

#validURL = valid360URL(URL) # validation logic is in URLtools360.py
validURL = False

    
# Copy the source text transferred in the form to our working copy.

workSource = source

# Add the boldbace tags, positioning them to enclose the text within the link.
# The following two lines look for an existing set of tags just outside the link
# and moves the tags inside the link.
#

workSource =  re.sub(r'(\<a href.*?>)(.*?)(\<\/a\>)',r'\1<strong>\2</strong>\3',workSource)
workSource =  re.sub(r'\<strong\>(\<a href.*?>)',r'\1<strong>',workSource)
workSource =  re.sub(r'(\<\/a\>)\<\/strong>',r'</strong>\1',workSource)

# If the link text was already bolded, this consolidates into a single set of such tags.

workSource =  re.sub(r'(\<a href.*?>)\<strong\>\<strong\>(.*?)\<\/strong>\<\/strong>',r'\1<strong>\2</strong>',workSource)

# If the space next to the first or last link word is inside the link 
# (some of us don't have the dexterity to swipe that precisely)
# we move the space to the outside.

workSource =  re.sub(r'(\<a href[^>]*?>\<strong>) ',r' \1',workSource)
workSource =  re.sub(r' \<.strong\>\<.a>',r'</strong></a> ',workSource)
#workSource =  re.sub(r'([\.\,\"\']{1,2})\<.strong\>\<.a>',r'</strong></a>\1',workSource)

# While we are here we can change curly quotes and apostrophes to the straight ascii quotes.

workSource = re.sub(r'\&rdquo\;',r'"',workSource)
workSource = re.sub(r'\&ldquo\;',r'"',workSource)

workSource = re.sub(r'\&lsquo\;',r"'",workSource)
workSource = re.sub(r'\&rsquo\;',r"'",workSource)

# With quotes simplified, move ending punctuation outside the link.
 
workSource =  re.sub(r'([\.\,\"\']{1,2})\<.strong\>\<.a>',r'</strong></a>\1',workSource)

# Some reporters use a double-hyphen in place of a dash. 
# No problem. We make it an em-dash here.

#workSource = re.sub(r' -- ',r' &ampmdash; ',workSource)
workSource = re.sub(r'([a-z]) -- ',r'\1 &ampmdash; ',workSource)
workSource = re.sub(r' -- ',r' &mdash; ',workSource)

# An en-dash surrounded by spaces was almost certainly meant to be an em-dash.

workSource = re.sub(r' &ndash; ',r' &ampmdash; ',workSource)

print '<strong>Copy the contents of this textbox, return to the source version of the story, select all and paste this text on top</strong></br >'

#print '<textarea rows="19" cols="120" name="source-orig" wrap="physical" disabled>' 
print '<textarea rows="19" cols="120" name="source-orig" wrap="physical">' 
print workSource
print '</textarea>'


    

