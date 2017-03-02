import os

from cryptography.fernet import Fernet

crypto = Fernet(os.getenv('ZZIZILY_BTA_CRYPTO'))
package_name = 'bta'
project_home = os.getenv('ZZIZILY_BTA_HOME')
