- 与数据库管理有关

## Part 1 创建视图
1. 相当于一个虚拟的表，用来筛选，防止看到一些敏感数据，例如银行账户的钱等，
2. 有意识的隐藏表的结构
3. 降低了SQL的复杂度

```mysql
create view vw_stu as
select name,chinese from student inner join score_student on student.id = score_student.stuid
```

- 上面创建了一个名为vm_stu的视图，后面是视图的内容，如果需要查看视图的内容可以通过
`select * from vm_stu`

这样就可以对视图之外的数据进行保密，同时需要知道该视图中的所有数据时，就不用再写一遍SQL语句了更为便捷

## Part 2 显示视图
![[Pasted image 20241028185415.png|300]]
1. 和表类似
![[Pasted image 20241028185427.png]]

2. 和表类似
![[Pasted image 20241028185449.png]]

3. 显示视图信息（没什么用）
![[Pasted image 20241028185530.png]]

## Part 3 更新、删除视图
- 更新
```mysql
alter view vw_stu as
select name from student
```

- 删除
`drop view vw_stu`

## Part 4 视图算法
- 用的情况较少

将子查询用到视图里会出现一些问题，跟视图算法有关，这时候就需要把视图算法调整为临时表算法

所以在创建视图的时候可以指定算法

```mysql
create algorithm=temptable view vw_stu as
select name,chinese from student inner join score_student on student.id = score_student.stuid
```

1. 合并（merge）

2. 临时表算法（temptable）

3. 未定义（undefined） 