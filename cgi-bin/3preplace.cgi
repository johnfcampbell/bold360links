#!/usr/bin/env python

from URLtools360 import valid360URL
from URLtools360 import boldSome
import os, cgi, re

import commands
import cgitb
cgitb.enable() # commented for alpha test
alpha=True # debug  flag
alpha = False
tabAction = " "
dubQuote = '"'
singleQuote = "'"
boldSomeRegexen = []

#freshBoldLink =  re.compile(r'(\<a href.*?>)(.*?)(\<\/a\>)',r'\1<strong>\2</strong>\3')
#boldStartInside =  re.compile(r'\<strong\>(\<a href.*?>)',r'\1<strong>')
#boldEndInside =  re.compile(r'(\<\/a\>)\<\/strong>',r'</strong>\1')


freshBoldLinkSearch =  re.compile(r'(<a _QQ_href.*?>)(.*?)(<\/a>)')
boldStartInsideSearch =  re.compile(r'<strong\>(<a href.*?>)')
boldEndInsideSearch =  re.compile(r'(<\/a>)<\/strong>')

# (<a href=.*?www.law360.com\/articles\/\d{6}|<a href=.\/articles\/\d{6}.*?>|<a href=.*?lexmachina.com.*?>)

#l360OnlyLinkSearch = re.compile(r'(<a href=.*?www.law360.com\/articles\/\d{6}|<a href=.\/articles\/\d{6}.*?>|<a href=.*?lexmachina.com.*?>)')

l360OnlyLinkSearch = re.compile(r'(<a href=.*?www.law360.com\/articles\/\d{6,}.*?>)(.*?)(<.a>)')
l360UKOnlyLinkSearch = re.compile(r'(<a href=.\/articles\/\d{6}.*?>)(.*?)(<.a>)')
lexMachOnlySearch = re.compile(r'(<a href=.*?lexmachina.com.*?>)(.*?)(<.a>)')

boldSomeRegexen.append(l360OnlyLinkSearch)
boldSomeRegexen.append(l360UKOnlyLinkSearch)
boldSomeRegexen.append(l360UKOnlyLinkSearch)

# l360OnlyLinkSearch, l360UKOnlyLinkSearch, lexMachOnlySearch

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
    sh=open("../source.txt")
    source=sh.read()

#validURL = valid360URL(URL) # validation logic is in URLtools360.py
validURL = False

#print("source:")
#print source
    
# Copy the source text transferred in the form to our working copies.

workSource = source
hrWorkSource = source

hasHr = re.search(r'<hr \/>',hrWorkSource)
if hasHr:
    # has a horizontal rule, so follow 3rd-party convention.
    # we want to separate text above the rule 
    # from text below the rule. 
    #
    # before that, we want to turn every bare URL into a link.
    # for third party stories, we want the link to open
    # in a new window.
    #
    if re.search(r'\ http[s]*:\/\/[a-zA-z0-9]',workSource):
        workSource = re.sub(r'\ (http[s]*:\/\/[^ ,]+)',r' <a href="\1" _qZZq_>\1</a>', workSource)
        workSource = re.sub(r'_qZZq_',r'target="_bLaNk"',workSource)
    #hrBeforeSource = re.sub(r'(.*)<hr .>.*?','\1',hrWorkSource)
    #hrAfterSource = re.sub(r'.*<hr .>(.*?)','\1',hrWorkSource)
    hrSplitSource = workSource.split('<hr />')
    if alpha:
        print("len(hrSplitSource) = " + str(len(hrSplitSource)))
        
    # the <!join> and <!plus> comments are for testing, 
    # so we know which regex gave us the horizontal-rule tag.
    hrBeforeSource = hrSplitSource[0]
    hrAfterSource = '<hr /><!join>'.join(hrSplitSource[1:])      
    hrBeforeSource =  re.sub(freshBoldLinkSearch,r'\1<strong>\2</strong>\3',hrBeforeSource)
    
    if alpha:
        print("len(hrSplitSource) = " + str(len(hrSplitSource)))
        print("calling boldSome, hasHr")
    
    hrBeforeSource = boldSome(hrBeforeSource, l360OnlyLinkSearch, l360UKOnlyLinkSearch, lexMachOnlySearch)
    hrBeforeSource = boldSome(hrBeforeSource, boldSomeRegexen)
        
    
    workSource = hrBeforeSource + '<hr /><!plus>' + hrAfterSource
    
else:
    # Add the 
    # also add boldface tags, positioning them to enclose the text within the link.
    #workSource =  re.sub(freshBoldLinkSearch,r'\1<strong>\2</strong>\3',workSource) #replaced by boldSome call.
    if alpha:    
        print("calling boldSome, else ...")    
    #workSource =  boldSome(workSource, l360OnlyLinkSearch, l360UKOnlyLinkSearch, lexMachOnlySearch)
    workSource =  boldSome(workSource, boldSomeRegexen)

    

# The following two lines look for an existing set of tags just outside the link
# and moves the tags inside the link.
#
workSource =  re.sub(boldStartInsideSearch,r'\1<strong>',workSource)
workSource =  re.sub(boldEndInsideSearch,r'</strong>\1',workSource)


# If the link text was already bolded, this consolidates into a single set of such tags.

workSource =  re.sub(r'(\<a href.*?>)\<strong\>\<strong\>(.*?)\<\/strong>\<\/strong>',r'\1<strong>\2_CONS_</strong>',workSource)

# If the space next to the first or last link word is inside the link 
# (some of us don't have the dexterity to swipe that precisely)
# we move the space to the outside.

workSource =  re.sub(r'(\<a href[^>]*?>\<strong>) ',r' \1',workSource)
workSource =  re.sub(r' \<.strong\>\<.a>',r'_MOVEO_</strong></a> ',workSource)
#workSource =  re.sub(r'([\.\,\"\']{1,2})\<.strong\>\<.a>',r'</strong></a>\1',workSource)


# While we are here we can change curly quotes and apostrophes to the straight ascii quotes.
# (This is no longer needed)

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

print '<strong>Copy the contents of this textbox, return to the source version of the test story, select all and paste this text on top</strong></br >'

#print '<textarea rows="19" cols="120" name="source-orig" wrap="physical" disabled>' 
print '<textarea rows="19" cols="120" name="source-orig" wrap="physical">' 
print workSource
print '</textarea>'

