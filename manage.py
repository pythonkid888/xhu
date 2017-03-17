#-*- coding:utf-8 -*-

from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role, Post, Permission, Comment


import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch= True, include= 'app/*')
    COV.start()
    

#支持中文
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app = app, db = db, User = User, Role = Role,
                Post = Post, Permission = Permission, Comment = Comment)

manager.add_command('shell', Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage = False):
    """Run the unit tests"""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def deploy():
    """Run deployment tasks"""
    from flask_migrate import upgrade
    from app.models import Role, User, Category, Alembic
    
    #清楚Alembic version
    Alembic.clear_A()
    
    #把数据库迁移到最新修订版本
    upgrade()
    
    #创建用户角色
    Role.insert_roles()
    
    #创建Todolist类别
    Category.insert_categorys()

    # 自关注
    User.add_self_follows()


if __name__ == '__main__':
    manager.run()