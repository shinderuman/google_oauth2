import urlparse
import oauth2 as oauth

scope = "http://www.google.com/reader/api"
sub_url = "%s/0/subscription/list" % scope
reading_url = '%s/0/stream/contents/user/-/state/com.google/reading-list' % scope

request_token_url = "https://www.google.com/accounts/OAuthGetRequestToken?scope=%s" % scope
authorize_url = 'https://www.google.com/accounts/OAuthAuthorizeToken'
access_token_url = 'https://www.google.com/accounts/OAuthGetAccessToken'

oauth_key = "www.asktherelic.com"
oauth_secret = "XXXXXXXXXXXXXX"

consumer = oauth.Consumer(oauth_key, oauth_secret)
client = oauth.Client(consumer)

# Step 1: Get a request token. This is a temporary token that is used for 
# having the user authorize an access token and to sign the request to obtain 
# said access token.

resp, content = client.request(request_token_url, "GET")
request_token = dict(urlparse.parse_qsl(content))

print "Request Token:"
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
print

# Step 2: Redirect to the provider. Since this is a CLI script we do not
# redirect. In a web application you would redirect the user to the URL
# below.

print "Go to the following link in your browser:"
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
print

accepted = 'n'
while accepted.lower() == 'n':
      accepted = raw_input('Have you authorized me? (y/n) ')

# Step 3: Once the consumer has redirected the user back to the oauth_callback
# URL you can request the access token the user has approved. You use the
# request token to sign this request. After this is done you throw away the
# request token and use the access token returned. You should store this
# access token somewhere safe, like a database, for future use.
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, "POST")
print resp
print content
access_token = dict(urlparse.parse_qsl(content))

print "Access Token:"
print "    - oauth_token        = %s" % access_token['oauth_token']
print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
print
print "You may now access protected resources using the access tokens above."

#Authorized client using access tokens
token = oauth.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
client = oauth.Client(consumer, token)

resp, content = client.request(sub_url, 'GET')
print content
print

resp, content = client.request(reading_url, 'GET')
print content
