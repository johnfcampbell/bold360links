import re

def valid360URL(url):

    validURL = True
    cappedURL = url.upper()
    validURL = validURL and re.match('\ *HTTPS',cappedURL)
    validURL = validURL and re.match(r'.*WWW.LAW360.COM.*',cappedURL)
    validURL = validURL and re.match(r'.*ARTICLES.\d{1,9}.*',cappedURL)
    return validURL
    
def origboldSome(sourceText, l360OnlyLinkSearch, l360UKOnlyLinkSearch, lexMachOnlySearch):

    #print("boldSome")
    sourceText =  re.sub(l360OnlyLinkSearch,r'\1<strong>\2</strong>\3',sourceText)
    sourceText =  re.sub(l360UKOnlyLinkSearch,r'\1<strong>\2</strong>\3',sourceText)
    sourceText =  re.sub(lexMachOnlySearch,r'\1<strong>\2</strong>\3',sourceText)

    return sourceText

def boldSome(sourceText, regexen):
    for regex in regexen:
        sourceText = re.sub(regex,r'\1<strong>\2</strong>\3',sourceText)
    return sourceText

