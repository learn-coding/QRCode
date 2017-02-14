"""

Maintains user information

"""

from itsdangerous import URLSafeTimedSerializer
from flask_login import UserMixin

# list of user objects
USERS = list()

secret_key = "amvobyul$%#!@"
loginSerializer = URLSafeTimedSerializer(secret_key)

########################################################################


class User(UserMixin):
  """

  User Class for flask-Login

  """
  ########################################################################

  def __init__(self, qr_id):
    self.id = qr_id
    #self.password = password

  ########################################################################
  def isAuthenticated(self):
    return True

  ########################################################################
  def isActive(self):
    return True

  ########################################################################
  def isAnonymous(self):
    return False

  ########################################################################
  def getAuthToken(self):
    """

    Encode a secure token for cookie

    """
    #data = [str(self.id), self.password]
    data = [str(self.id)]
    return loginSerializer.dumps(data)

  ########################################################################
  @staticmethod
  def get(qr_id):
    for user in USERS:
      if user == qr_id:
        return user
