import pysftp
import io

# This class is a wrapper for pysftp.Connection
class SftpAgent:
    def __init__(self, host, username, password, default_path=None, port=22,
                 private_key=None, private_key_pass=None,
                 ciphers=None):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        self.sftp = pysftp.Connection(host=host, username=username, password=password,
                                      default_path=default_path, port=int(port),
                                      private_key=private_key, private_key_pass=private_key_pass,
                                      ciphers=ciphers, cnopts=cnopts)

    def listdir(self):
        return self.sftp.listdir()

    def chdir(self, remotepath):
        self.sftp.chdir(remotepath)

    def remove(self, file_name):
        self.sftp.remove(file_name)
    
    def get(self, file_name, localpath='./.sftp_backup'):
        self.sftp.get(file_name, localpath=localpath)

    def listdir_attr(self):
        return self.sftp.listdir_attr()

    def putfo(self, file_name, content):
        bio = io.BytesIO(content.encode('utf-8'))
        self.sftp.putfo(bio, remotepath=file_name)

    def close(self):
        self.sftp.close()