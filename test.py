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
    user.id = 2
    user.save()

    user = User(name='name2', id=3)
    user.delete()

    for i in User.objects.filter(id=2).get():
        i.update()


if __name__ == "__main__":
    _main()
