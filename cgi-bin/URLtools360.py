import re

def valid360URL(url):

    validURL = True
    cappedURL = url.upper()
    validURL = validURL and re.match('\ *HTTPS',cappedURL)
    validURL = validURL and re.match(r'.*WWW.LAW360.COM.*',cappedURL)
    validURL = validURL and re.match(r'.*ARTICLES.\d{1,9}.*',cappedURL)
    return validURL
    
