## 主键
对字段的约束：
主键的约束
default尽量不为空（NULL）
auto_increment对应的一定是primary key，使用了自增，删除某个元组后，不能再添加id等于该元组的id的元组

- 拥有主键，保证数据完整性，加快查询，不可能重复，不可能为空，可以由多个字段构成

- 删除主键
`alter table student drop primary key;`

- 增加主键：
`alter table student add primary key (id, name);`

- 组合键：上面的是复合主键，不是两个单独都是主键，算一个主键。
## 唯一键
- 唯一键：不是用来区分数据的，和其他表里的内容无关，可以为空，主键会和其他表相关联，可以有多个，保证数据不重复。

-比如说每个老师的电话号码不一样等等，和其他表关系就不是很大。
如下，如果在唯一键创建了一个重复的值就会报错

![[Pasted image 20241009192653.png]]

- 后期添加唯一键
`alter table test_1 add unique(phone);`

如果括号中是两个，就是组合唯一键。
- 查看唯一键
`show create table test_1;`

- 删除唯一键功能（不会删除属性）
`alter table test_1 drop index phone;`

## 注释

![[Pasted image 20241009194222.png]]

- 一般是看SQL内注释，字段注释，comment
![[Pasted image 20241009194445.png]]

![[Pasted image 20241009194628.png]]

## 数据完整性

- 需要主键，
- 选择合适的数据类型
- NULL的约束
- default，有的字段必须要有约束（学生没来不能给0分，地址不详，原因未知等等）
- 外部的引用
- 自定义约束

## 外键约束

假如说有个学生表，一个食堂订单表，食堂订单表的学生部分要使用学生表中的id，学生部分不能出现学生表中id没有的部分，这就是外键约束

但是实际应用中，对于并发的处理禁止使用外键。

- 后期添加外键
`alter table eatery add foreign key(stuid) references student(id);`
- 查看外键
`show create table eatery;`

使用关系型数据库最好前期就设计好数据库的结构，不建议后期添加，后期添加一般是后期维护或者是数据库发生更改。

- 删除外键
`alter table eatery drop foreign key eatery_ibfk_1;`
注意后面那个是别名，不能直接stuid，需要通过`show create table ...`的方式来看。

如果在key的地方有mul是该属性的值可以重复的意思。

desc的方式看不到外键，只能用show...的方式


学生表中的学生如果去掉一个，那么在食堂订单表中会有两种处理方式：
1. 置空操作：将对应的id换成NULL

2. 级联操作：也全部干掉，如果是更改，这里也是更改
（在删除的时候一般不使用级联使用置空，在更新的时候一般使用级联）

![[Pasted image 20241009204054.png]]

![[Pasted image 20241009204112.png]]

