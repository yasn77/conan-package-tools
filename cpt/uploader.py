class Uploader(object):

    def __init__(self, conan_api, remote_manager, auth_manager, printer, upload_retry):
        self.conan_api = conan_api
        self.remote_manager = remote_manager
        self.auth_manager = auth_manager
        self.printer = printer
        self._upload_retry = upload_retry
        if not self._upload_retry:
            self._upload_retry = 0

    def upload_packages(self, reference, upload, package_id):
        remote_name = self.remote_manager.upload_remote_name
        if not remote_name:
            self.printer.print_message("Upload skipped, not upload remote available")
            return
        if not self.auth_manager.credentials_ready(remote_name):
            self.printer.print_message("Upload skipped, credentials for remote '%s' not available" % remote_name)
            return

        if upload:
            from conans.model.version import Version
            from conans import __version__ as client_version
            self.printer.print_message("Uploading packages for '%s'" % str(reference))
            self.auth_manager.login(remote_name)

            if Version(client_version) < Version("1.7.0"):
                self.conan_api.upload(str(reference),
                                      package=package_id,
                                      remote=remote_name,
                                      force=True,
                                      retry=int(self._upload_retry))
            elif Version(client_version) < Version("1.8.0"):
                self.conan_api.upload(str(reference),
                                      package=package_id,
                                      remote_name=remote_name,
                                      force=True,
                                      retry=int(self._upload_retry))
            elif Version(client_version) < Version("1.12.0"):
                self.conan_api.upload(str(reference),
                                      all_packages=True,
                                      remote_name=remote_name,
                                      retry=int(self._upload_retry))
            else:
                raise Exception("Incompatible installed Conan version found: %s" % client_version)
