from data.db_session import global_init, create_session
from data.users import User

global_init(input())
session = create_session()
users = session.query(User).filter(User.address == 'module_1',
                                   User.speciality.notlike('%engineer%'),
                                   User.speciality.notlike('%engineer%')).all()
for user in users:
    print(user)