from orm import *


class User(Model):
    id = IntField()
    name = StringField()

    class Meta:
        table_name = 'user'


class Man(User):
    class Meta:
        table_name = 'man'
    sex = StringField()


def _main():
    user = User(name='name', id=1)
    user.save()
    User.objects.create(id=1, name='name')
    User.objects.update(id=1)
    User.objects.delete(id=1)
    try:
        pass
    except User.dne as identifier:
        pass

    for i in User.objects.filter(id=2).filter(name__gt='petya').get():
        i.update()


if __name__ == "__main__":
    _main()
