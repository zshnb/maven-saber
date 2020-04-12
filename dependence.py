class Dependence(object):
    def __init__(self, artifact_id, group_id, version):
        self.artifact_id = artifact_id
        self.group_id = group_id
        self.version = version

    def to_string(self):
        print('<groupId>{}</groupId>\n<artifactId>{}</artifactId>\n<version>{}</version>\n'
              .format(self.group_id, self.artifact_id, self.version))

    def __eq__(self, other):
        if self.artifact_id == other.artifact_id and \
                self.group_id == other.group_id and \
                self.version == other.version:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.artifact_id + self.group_id + self.version)
