- stored program 存储过程
可以用来增删改查，也可以用来事务

使用终端时，每使用一个分号执行一个语句，Mysql提供了一个方式：在命令行输入，`delimiter //`

这时，再使用分号就不会执行语句，这时候就必须使用//才能结束语句

当用完事务或存储过程等之后再还原成分号`delimiter ;`

`delimiter //`
`create procedure proc()`
`begin`
`update wallet set balance=balance+50;`（不会发送）
`update t3 set name='tom';`
`end //`

- 执行
`delimiter ;`
`call proc();`

- 删除
`drop procedure proc;`

- 查看
`show create procedure proc;`
`show create procedure status \G;`（显示所有的存储过程）


- 有一点函数的感觉

