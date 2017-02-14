"""

User logout API

"""

import os

from flask import *
from flask_restful import Resource
from flask_login import logout_user
from login import loginRequired

########################################################################


class Logout(Resource):
  ########################################################################

  @loginRequired
  def get(self):
    #curl cmd : curl -i -H "Content-Type: application/json" -X GET --cookie "token=WyJ0dXNoYXIucGhpcmtlIiwiY1FLNiY5JnozaEBGckJGdSJd.BosE7w.mmNjtEvuspwZOFtfa6OzhkGZC1I" http://127.0.0.1:8888/qrcode/logout
    """

    This function removes the user token from the disk.

    """
    code = '200'
    resp = make_response(code)

    # remove token related file from /tmp
    token = request.cookies.get("token")

    if not token:
      code = '400'
      resp = make_response(code)
      return resp

    if os.path.exists('/tmp/tokens/'):
        filePath = "/tmp/tokens/%s" % (token.split('.')[-1])
        if not os.path.isfile(filePath):
          code = '400'
          resp = make_response(code)
          return resp
        else:
          os.remove(filePath)

    logout_user()
    return resp
