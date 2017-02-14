"""

User login API

"""

import cPickle
#import pam
import os
import time
import shutil
import base64

#from common import exception
from filelock import FileLock
from flask import *
from flask_restful import Resource
from flask_restful import abort as flask_abort
from functools import wraps
from users import *

#logger = getLogger('sanblox')


########################################################################
class Login(Resource):


  ########################################################################
  def post(self):
    #curl cmd : curl -i -H "Content-Type: application/json" -X POST -d "{\"qrid\": \"4608679FA0A87A2D\"}" http://127.0.0.1:8888/qrcode/login
	#curl cmd with encoded data : curl -i -H "Accept:application/json" -H "Authorization:Basic IjQ2MDg2NzlGQTBBODdBMkQi" -X POST http://127.0.0.1:8888/qrcode/login
    """

    This function validates an user.It generates the
    unique token per user which is later used through
    out the session to validate the user. The token
    expiry time depend upon 'rememberme' option.

    """
    try:
      tokenDir = '/tmp/tokens'
      tokenDict = dict()
      codedStr = request.headers["Authorization"]
      codedCredentials = codedStr.split(' ')[1]
      decodedCredentials = base64.b64decode(codedCredentials)
      #qr_id = request.get_json('qrid')
      qr_id = decodedCredentials.split(':')[0]
      #password = decodedCredentials.split(':')[1]
      rememberMe = False  # request.json['rememberme']

      #if pam.authenticate(qr_id):
      user = User(qr_id)
      USERS.append(user.id)
      #logger.info('Logged in as user: %s' % qr_id)

      token = user.getAuthToken()
      if not os.path.exists('/tmp/tokens/'):
          os.mkdir('/tmp/tokens/')
      tokenDir = '/tmp/tokens'

      return self.sendResponse(tokenDir, token, tokenDict, qr_id, rememberMe)

      #else:
        #raise exception.AuthError("Unauthorized User")

    except Exception, e:
      import traceback; traceback.print_exc()
      stat = 'false'
      #code = 'AUTH-3001'
      mesg = getattr(e, 'value', 'Authentication error')
      flask_abort(503)


  #######################################################################
  def sendResponse(self, tokenDir, token, tokenDict, qr_id, rememberMe):
    """

    pickle token related file in /tmp or /mnt/sbx-config directory which will be
    used for validating token

    """
    with open("%s/%s" % (tokenDir, token.split('.')[-1]), "w") as fd:
      tokenDict[token] = qr_id
      tokenDict['time'] = int(time.time())
      tokenDict['expireTime'] = int(
        time.time()) + (60 * 60 * 24) if rememberMe else int(time.time()) + 60 * 5 #timeout of 120 seconds
      cPickle.dump(tokenDict, fd)

    code = '200'
    response = make_response(code)
    if rememberMe:
      response.set_cookie('token', token, max_age=60 * 60 * 24)  # 1 day
    else:
      response.set_cookie('token', token)

    return response


########################################################################
def loginRequired(f):
  """

  This is a decorator that's checks the authenticity
  of user. It checks whether the token is valid/invalid
  or expired.

  """
  ########################################################################
  @wraps(f)
  def decoratedFunction(*args, **kwargs):
    try:
      tokenDir = '/tmp/tokens'
      tokenDict = dict()
      if g.user is None:
        raise exception.AuthError('')

      authenticated = False

      # load pickle file which will be used to validate token
      token = request.cookies.get("token")
      if not token:
        raise exception.AuthError('Token not provided')


      filePath = "%s/%s" % (tokenDir, token.split('.')[-1])

      if not os.path.isfile(filePath):
        tempDir = '/tmp/tokens'
        tempPath = "%s/%s" % ('/tmp/tokens', token.split('.')[-1])
        if os.path.isfile(tempPath) and os.path.exists('/tmp/tokens/'):
          for file in os.listdir(tempDir):
            path = os.path.join(tempDir, file)
            shutil.move(path, tokenDir)
        else:
          raise exception.AuthError('Invalid token')

      with FileLock(filePath + ".lock"):
        with open(filePath, "r") as fd:
          tokenDict = cPickle.load(fd)

      #print int(time.time()), '---> current time'
	  print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
      print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tokenDict['expireTime'])) #tokenDict['expireTime'], '--> expireTime'
      print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tokenDict['time'])) #tokenDict['expireTime'], '--> expireTime'
      print tokenDict
      print "-------------------------------------"
      if int(time.time()) > tokenDict['expireTime']:
        print tokenDict['expireTime'],"========="
        #logger.error('Session has been timed out')
        os.remove(filePath)
        raise exception.AuthError('Session has been timed out')

      for token in tokenDict.iterkeys():
        if token == request.cookies.get("token"):
          authenticated = True

      if not authenticated:
        #logger.error("Not authenticated %d" % authenticated)
        raise exception.AuthError('')

      #with FileLock(filePath + ".lock"):
        #with open(filePath, "w") as fd:
          #tokenDict['expireTime'] += int(
            #time.time()) - tokenDict['time']
          #cPickle.dump(tokenDict, fd)

      return f(*args, **kwargs)

    except Exception, e:
      stat = 'false'
      #code = 'AUTH-3001'
      mesg = getattr(e, 'value', 'Authentication error')
      flask_abort(401)

  return decoratedFunction
