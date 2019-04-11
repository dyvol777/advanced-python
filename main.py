from orm import *


class User(Model):
    id = IntField()
    name = StringField()

    class Meta:
        table_name = 'User'


class Man(User):
    sex = StringField()


if __name__ == '__main__':
    user = User(id=1, name='name')
    User.objects.create(id=1, name='name')
    User.objects.update(id=1)
    User.objects.delete(id=1)

    User.objects.filter(id=2).filter(name='petya')

    user.name = '2'
    user.save()
    user.delete()
