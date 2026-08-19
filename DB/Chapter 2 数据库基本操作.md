## Part 1 数据库的基本操作
### Section 1 databases解释
进入mysql后可以通过 `show databases;` 命令的方式查看数据库

![Pasted image 20240919200849](images/Pasted%20image%2020240919200849.png)

如上图有四个仓库，都是不同的。一个公司里会有DBA（数据库管理员）或架构师，专门管理数据库，搭建数据库（集群搭建....）
1. information_schema 表示存储这个数据库整个仓库的信息
2. mysql 存一些系统用户的信息，比如说进入mysql的密码之类的
3. information_schema 存储服务器性能
4. sys 表示一些系统文件
5. 可能还会有一个test，这个就是测试用的
![Pasted image 20240919202233](images/Pasted%20image%2020240919202233.png)

### Section 2 创建数据库

`create database student;`
再次输入`show databases;`
就会发现多了一个student的仓库，这个仓库的名字要注意不要使用关键字

`create database database;`就会报错
如果强制使用：create database \`database\`（不建议使用关键字）
已经用过的名字也会报错

所以在创建数据库之前可以先检查是否已经创建过该数据库（即是否使用该名字）
`create database if not exists student;`
这种方式会更规范：create database if not exists \`student\`;

输入之后如果已经存在该仓库，那么就会出现一条警告，就不会报错，如果不存在，就会帮助创建。

### Section 3 删除数据库
- 删除存在的库
`drop database student;`

- 假设删除了不存在的库，就会报错，所以可以用下面的方式来进行删除
`drop database if exists student;`
也可以加上反单引号更规范

### Section 4 查看创建的库

`show create database student;`
之后就会出现
![Pasted image 20240919205142](images/Pasted%20image%2020240919205142.png)
可以查看这个仓库曾经是怎样创建的

### Section 5 字符编码
#### 创建库时指定字符编码
我们创建数据库的时候可以创建字符编码。
有的时候我们写C语言可能会出现乱码，这就是字符编码没有控制好。
常见的国际通用的字符编码是：GBK，UTF-8。GBK是中文简体
- 如下，终端会显示中文就是因为我们设置是GBK。
可以找到cmd的属性选项可以看到是GBK
![Pasted image 20240919205638](images/Pasted%20image%2020240919205638.png)

- create database if not exists \`students\` charset=gbk
可以通过上面的方式在创建的时候设置字符编码，但是我们实际开发的时候要注意使用utf8，windows上比较特殊，因为它的cmd是gbk的，所以在windows上学习的时候使用gbk。

#### 查看字符编码
- 设置好后查看新创建的库就可以看到字符编码
![Pasted image 20240919211302](images/Pasted%20image%2020240919211302.png)
右下角：默认字符设置

#### 修改字符编码
修改字符编码：假设在创建库的时候忘记设置字符编码
`alter database student charset=gbk;`

alter就表示更改等操作。

## Part 2 表的基本操作
- 什么是表？
表被包含于数据库，相当于一个柜子（数据库），第一格放电子产品，第二格放化妆品，第三个格放日用品...
电子产品中的一格还包括电脑，手机...等等分类

### Section 1 引用数据库和查看数据库
- 创建好一个数据库之后当我们需要使用某数据库（这一步就是引用数据库，类似于JD物流发配）
就需要使用`use school;`（假设创建的库是school）
当我们需要查看该数据库中的表时：`show tables;`
![Pasted image 20240922173714](images/Pasted%20image%2020240922173714.png)

### Section 2 创建表

```mysql
create table student(
id int,
name varchar(30),
age int
);
```
![Pasted image 20240922195049](images/Pasted%20image%2020240922195049.png)

- 更规范的写法
```mysql
create table if not exists teacher(
id int auto_increment primary key comment '主键id',
name varchar(30) not null comment '老师的名字',
phone varchar(20) comment '电话号码',
address varchar(100) default '暂时未知' comment '住址'
)engine=innodb;
```

- auto_increment 表示自动增长，比如说学号id，
- primary key 表示主键，关系型数据库的核心
- comment 表示注释
- not null 表示不能为空，就是这个名字必须填的意思
- default 表示默认值，就是如果不填address，那么address就会是暂时未知
- engine=innodb,待查(事务要在该引擎下才能使用)
id不用default是已经声明了是primary key，所以没有default
如果不输default，那么系统的默认值就会是NULL。
id，name，phone等等都叫字段
![Pasted image 20240922204420](images/Pasted%20image%2020240922204420.png)

### Section 3 查看表

有两种方式
`show create table teacher;`：这种方式显示出的是sql语句
`desc teacher;`：这种方式会展示一个表，更为直观

![Pasted image 20240922204517](images/Pasted%20image%2020240922204517.png)

![Pasted image 20240922204529](images/Pasted%20image%2020240922204529.png)

### Section 4 删除表
`drop table if exists abc;`

![Pasted image 20240922205034](images/Pasted%20image%2020240922205034.png)

如上图，创建了abc，zhang两个废表，可以用逗号隔开删除两张表，如果加了if exists，即使abcd表不存在也可以将abc和zhang两张表删掉。

### Section 5 修改表

- 假如说需要添加一行在表尾：`alter table student add phone varchar(20);`
![Pasted image 20240922211121](images/Pasted%20image%2020240922211121.png)
- 如果要指定位置：`alter table student add gender varchar(1) after name;`
![Pasted image 20240922211154](images/Pasted%20image%2020240922211154.png)

- 如果要放在表头：`alter table student add address varchar(1) first;`
![Pasted image 20240922211254](images/Pasted%20image%2020240922211254.png)

- 如果要删除某一行：`alter table student drop address;`
![Pasted image 20240922211410](images/Pasted%20image%2020240922211410.png)

- 修改某一行(change可以修改名字（字段）和类型)：`alter table student change phone telephone int(11);`
![Pasted image 20240922211505](images/Pasted%20image%2020240922211505.png)

modify只能修改类型：`alter table student modify telephone varchar(13);`
![Pasted image 20240922211658](images/Pasted%20image%2020240922211658.png)

- 改表名：`alter table student rename to students;`
（注意在使用数据库的过程中，表名不要用复数）。
