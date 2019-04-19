from FirstHW.model import *


class User(Model):
    id = IntField()
    name = StringField()

    class Meta:
        table_name = 'user'


class Man(User):
    class Meta:
        table_name = 'man'

    sex = StringField(False, 'Null')


def _main():
    user = User(name='name', id=1)
    user.save()
    user.id = 2
    user.save()
    user.delete()

    user = User(name='name2', id=2)
    user.delete()

    Man.objects.create(name='name1', id=1)
    Man.objects.create(name='name2', id=2, sex='w')
    Man.objects.create(name='name3', id=3, sex='m')

    people = Man.objects.all()

    men = Man.objects.filter(sex='m').get()

    usver = Man.objects.filter(sex='m').filter(id=1).get()

    for us in men:
        us.sex = 'man'
        us.save()

    print('allok!')


if __name__ == "__main__":
    _main()
