import mgraph_db
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Files            import file_contents, path_combine

class Version(Type_Safe):

    FILE_NAME_VERSION = 'version'

    def path_code_root(self):
        return mgraph_db.path

    def path_version_file(self):
        return path_combine(self.path_code_root(), self.FILE_NAME_VERSION)

    def value(self):
        value = file_contents(self.path_version_file()) or ""
        return value.strip()

version__mgraph_db = Version().value()