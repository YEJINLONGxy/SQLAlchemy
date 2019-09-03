from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


# Column 定义字段，Integer、String 分别为整数和字符串数据类型
# 参数说明： 数据库类型 + 驱动://用户名:密码@主机:端口号/数据库名字?charset=编码格式
# mysql 自带驱动，密码为root用户登录密码，没有这不用，端口号可省略

#engine = create_engine('mysql://root:123456@localhost/study?charset=utf8')
engine = create_engine('mysql://root@localhost/study?charset=utf8')

# 创建映射类需要继承声明基累
# 声名基类时传入引擎
Base = declarative_base(engine)

# 创建 user 数据表，此表存放用户数据，也就是课程作者的数据：
class User(Base):		# 继承声明基类
	__tablename__ = 'user'	# 设置数据表名字，不可省略
	id = Column(Integer, primary_key = True)	# 设置该字段为主键
	# unique 设置唯一约束， nullable 设置非空约束
	name = Column(String(64), unique=True, nullable=False)
	email = Column(String(64), unique=True)

	# 次特殊方法定义实例的打印样式
	def __repr__(self):
		return '<User: {}>'.format(self.name)


# 建第二个映射类 Course，它对应的数据表 course 存放课程数据。一个课程作者可以创建多个课程，
#一个课程对应唯一的课程作者，这种关系被称为一对多或者多对一关系，这是最常用的数据表关系类型：
class Course(Base):
	__tablename__ = 'course'
	id = Column(Integer, primary_key=True)
	name = Column(String(64))
	# ForeignKey 设置外键关联，第一个参数为字符串，user 为数据表名，id 为字段名
    	# 第二个参数 ondelete, 设置删除 User 实例后对关联的 Course 实例的处理规则
    	# 'CASCADE' 表示级联删除，删除用户实例后，对应的课程实例也会被连带删除
	user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
	# relationship 设置查询接口，以便后期进行数据库查询操作
    	# 第一个参数为位置参数，参数值为外键关联的映射类名，数据类型为字符串
    	# 第二个参数 backref 设置反向查询接口
    	# backref 的第一个参数 'course' 为查询属性，User 实例使用该属性可以获得相关课程实例的列表
    	# backref 的第二个参数 cascade 如此设置即可实现 Python 语句删除用户数据时级联删除课程数据
	user = relationship('User',
		backref=backref('course', cascade='all, delete-orphan'))

	def __repr__(self):
        	return '<Course: {}>'.format(self.name)

# 创建数据表:
# 声明基类 Base 在创建之后并不会主动连接数据库，因为它的默认设置为惰性模式。Base 的 metadata 有个
#  create_all 方法，执行此方法会主动连接数据库并创建全部数据表，完成之后自动断开与数据库的连接：

if __name__ == '__main__':
	# 使用声明基类的 metadata 对象的 create_all 方法创建数据表：
	Base.metadata.create_all()

#定义列时常用参数表：
#
#参数		说明
#primary_key	如果设为 True，这列就是表的主键
#unique		默认值为 False，如果设为 True，这列不允许出现重复的值
#index		如果设为 True，为这列创建索引，提升查询效率
#nullable	默认值为 True，这列允许使用空值；如果设为 False，这列不允许使用空值
#default		为这列定义默认值
#
#
#常用的 SQLAlchemy 查询关系选项（在 backref 中使用）：
#
#选项		说明
#backref		在关系的另一个映射类中添加反向引用
#lazy		指定如何加载查询记录。可选值有 select (首次访问时按需加载)、immediate (源对象加 载后
#		就加载)、joined (加载记录，但使用联结)， noload (永不加载)和 dynamic (不加载记录，但
#		提供加载记录的查询，比较常用)
#cascade		设置级联删除的方式
#uselist		如果设为 False ，查询结果不使用列表，而使用映射类实例（下节课程会用到）
#order_by	指定查询记录的排序方式
#secondary	指定多对多关系中关系表的名字


#运行程序
# 在终端使用 Python 解释器运行文件，在此之前先安装一个必要的依赖包 mysqlclient，该依赖包的作用是连接数据库：

#$ sudo pip3 install mysqlclient  # 安装依赖包
# $ python3 db.py                  # 运行文件，使用映射类创建对应的数据表
