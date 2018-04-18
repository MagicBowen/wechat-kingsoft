class UserId:
    def __init__(self):
        self.roles = {}
    
    def set_role(self, id, role):
        print('User id {0} set role to {1}'.format(id, role))
        self.roles[id] = role

    def get_role(self, id):
        return self.roles[id] if id in self.roles else 'kingsoft-qiuye'

    def get_role_name(self, role):
        return '秋叶青' if role == 'kingsoft-qiuye' else '李复'

    def role_modified_reply(self, role):
        return '注意，您当前的对话角色已经变为{0}了哦😀'.format(self.get_role_name(role))