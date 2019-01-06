from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from shudong import app
from exts import db
from models import User,Question,Answer,followers

manager = Manager(app)

migrate = Migrate(app,db)

#添加迁移脚本的命令道manager
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()