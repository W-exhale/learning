## 增
- 添加数据
可以打乱顺序，但是不好看
`insert into teacher(id, name, phone, address) values(1, 'Wang', '123457890', 'ShangHai');`

- 查看数据

`select * from teacher;`（\*是全部的意思，查询这张表所有的东西，from是指定表），但是这条语句效率不是很高，在性能上有缺陷

![[Pasted image 20241007170930.png]]

如果不写第一个括号内的内容，就必须按照table的顺序来，写了就按照第一个括号内的顺序来。

不能为空的项必须赋值，可以为空的项可以使用NULL，如果在id的地方填NULL是ok的，显示的时候还是有，因为是自增的，还可以填default。不能少项，会报错。


- 一次性插入多条语句
`insert into teacher values(NULL, 'Tom', NULL, default),(NULL, 'Jerry', NULL, default);`

## 删
- 删除
`delete from teacher where id = 9;`

`delete from teacher where name = "Tom";`（重名的全删）

`delete from student where age>30;`

清空表：
`delete from tercher;`(不建议，比较慢，因为是一个一个删的，遍历表一个一个删)

`truncate table student;`（把原来的表直接报废，然后创建一个新的一样的表）


-这时候，用delete的方式删除teacher表，之前的数据还在，id就会顺着上次id继续顺延，但是truncate的方式就不会。

## 改
- 更新表
`update teacher set name = 'Jeff' where id = 1;`

`update teacher set name = 'Tom' where phone = 12345;`
where后面的phone如果有三个人的phone都是12345，那么这三个人的名字都会改成Tom。

可以改多个值，用逗号隔开即可。
`update teacher set name = 'Tom', address = 'shenzhen' where id = 1;`

-如果后面没有跟上where，那么所有内容都会改成上面的内容。（SQL注入）

-也可以选多个
`update teacher set name = 'Tom', address = 'shenzhen' where id = 1 or id = 2;`

## 查（初级）
- 查询数据
`show datebases;`
`show tables;`(use xxx)

`desc teacher;`

`select phone, address from teacher;`

## SQL语句区分
- DDL(data definition language)：数据定义语言 create alter drop show（给数据库用的）
- DML（data manipulation language）：数据操纵语言 insert update delete select（给数据用的）
- DCL（data control language）：权限分配等等。

在mysql中不等于是：`!=`，Sqlserver中是`<>`
## 字符编码问题
window的cmd是gbk，在使用mysql时，显示的也是gbk，但是在实际的开发过程中是不能使用gbk的，必须使用UTF-8.

![[Pasted image 20241007181039.png]]

如果在使用过程中出现字符编码问题，可以使用下面的语句查看字符编码
`show variables like 'character_set_%'`

![[Pasted image 20241007181443.png]]

client是gbk，返回的results也是gbk，那就没关系，但是实际开发的时候全部都是utf8，除了binary。

自己练习需要修改可以用下面的方式（所以说windows不适合做开发）
`set character_set_client=gbk;`

