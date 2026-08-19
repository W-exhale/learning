## 事务

- 跟钱有关的会用到事务

下单了没付款，钱去哪了

要有一个东西必须确定之后才能进行更新，这个东西就是事务

![Pasted image 20241105205818](images/Pasted%20image%2020241105205818.png)

假设把1号的钱转到2号，要存在一个确定的动作使得数据更新

![Pasted image 20241105211001](images/Pasted%20image%2020241105211001.png)

当数据输入错误，但是还没有commit时，就可以回滚rollback，不会改变数据

commit后就不能rollback

![Pasted image 20241105211901](images/Pasted%20image%2020241105211901.png)

- savepoint类似于一个快照的功能，可以用rollback回滚到相对应的点

ACID（事务的四个特性）：
A：atomicity       原子性（不能再分了，事务是一个整体，要执行就一起执行）
C：consistency  一致性（commit后所有的数据应该都是相对应的）
I：isolation          隔离性（事务和事务之间是隔离的）
D：durability       持久性（commit后在数据库中的数据一直保持）


- 注意事项：
事务不是随时都能用的，
创建数据库的时候可以设置一个引擎，必须保证是innodb才行


## 索引  index
用来查东西的，查询速度快
如果把一个东西设置为索引，那么这个东西增删改的效率就会变的很低（不是一般的低），索引还占空间，有的东西强制不能设置为索引

primary key主键索引
- 添加索引
![Pasted image 20241105213617](images/Pasted%20image%2020241105213617.png)

不带东西的是普通索引，unique index是唯一键索引，

- 更新索引
`alter table wallet add index balance_index (balance);`

- 删除
`drop index balance_index on wallet;`

-条件
经常要查的一列数据
数据多（数据少不建议用索引）



sphinx