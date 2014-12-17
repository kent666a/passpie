from glob import glob
import os

from .credential import Credential
from .crypt import create_gpg


class Database(object):

    def __init__(self, path, passphrase, gpg_bin="gpg2"):
        self.path = path
        self.gpg = create_gpg(gpg_bin, self.path, passphrase)

    @property
    def gpg_key(self, secret=False):
        return self.gpg.list_keys(secret=secret)[0]

    def add(self, credential):
        encrypted_password = self.gpg.encrypt(
            credential.password,
            self.gpg_key
        )
        credential.password = str(encrypted_password)
        credential.save(database_path=self.path)

    def credential(self, name):
        credential_path = os.path.join(self.path, name)
        credential = Credential.from_path(credential_path)
        return credential

    @property
    def credentials(self):
        return [self.credential(os.path.basename(c))
                for c in glob(self.path + "/**")]
