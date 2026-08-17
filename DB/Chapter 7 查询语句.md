## Part 1 单表查询

### Section 1 关键字
1. select \`你好 \`; select 2 * 7;
2. as：起别名：select 2 * 7 as res;
	![[Pasted image 20241019143551.png|300]]
3. from（后面计算笛卡尔积）表1.1对表2.1,表1.2对表2.1....，表1.1对表2.2...
4. dual：默认的伪表（上面2号语句的表实际上是select 2 * 7 as res from dual）
5. where：条件筛选（select * from teacher where ....），and，or，大于(>)，小于(<)，!=, ...
	in：select * from t4 where address in('beijing','shanghai');
	not：可以放在in等的前面表示非
	between ... and ...：就不用写大于等于xx and 小于等于 xx
	is null：查找为空的（select * from t3 where age is null;）还有一种：is not null.

- 空值：在数据库中，null代表的是unknown，也就是说，在数据库中有三个逻辑值，true，false，unknown，空值可以用is null和is not null来判断是否是空值，也可以用is unkonwn
### Section 2 聚合函数（mysql自带的函数用于计算等等）

1. 求和sum()
	![[Pasted image 20241019152314.png|400]]

2. 求平均值avg
	![[Pasted image 20241019152558.png]]
3. 最大值，最小值
	![[Pasted image 20241019152626.png]]
4. 计算多少个数据
![[Pasted image 20241019152700.png]]

但是注意尽量不要使用count(\*) ，注意区别count(1)和count(\*)，前面计算数据时不会计算null行，后面会计算所有行的数量，除了count(\*)，其他所有的聚合函数都会忽略null

### Section 4 客户端的使用
下载Navicat Premium
可以找注册工具


可以通过新建查询的方式来select（带提示，不推荐）
![[Pasted image 20241019163929.png|300]]

![[Pasted image 20241019164007.png|300]]

### Section 5 模糊查询（like）
使用like关键字

- 百分号可以代表多个字符，
![[Pasted image 20241019163402.png]]

- 一个下划线代表一个字符
![[Pasted image 20241019163435.png]]

'% comp%'可以匹配任何含有comp子串的字符串
‘`___%`’
转义字符的使用，可以使用escape来定义转义字符
`like ‘ab\%cd%’ escape ‘\’`匹配所有以ab%cd为开头的字符串



- 字符串运算

就需要使用2个单引号字符来表示，例如字符串"it's right"可以表示为"it 's right"，
需要注意的是SQL中字符串的相等运算是大小写敏感的，但是MySQL和SQL server中不一定
SQL中字符串有多种函数，不同数据库系统提供的不一样



### Section 6 分组查询（group by）
![[Pasted image 20241019165729.png|300]]

![[Pasted image 20241019165103.png]]

查年龄平均值和性别，依照来自info表的性别分组来显示

![[Pasted image 20241019165628.png]]

- 格式必须是：`select 聚合函数 (as ...), 依据分组项 (as ...) from table group by 依据分组项;`

- 还可以加desc降序（根据地址来的）
![[Pasted image 20241019170249.png]]

聚合使用：![[Pasted image 20241019185153.png]]
### Section 7 having（与where同级）
- where的筛选方式是一条一条筛选，比如说查语文成绩，先看id为1的语文成绩再判断是否符合要求，符合要求就拿出来，再看id为2的....（从原本的表里去筛选）

```MYSQL
select avg(age) as '年龄平均值',address as '地址' from info group by address where '年龄平均值' > 23.0;
```
如果想要在选出来的伪表里面进行筛选就不能用where，因为where是用于原始表的，像上面的查询方式就是错误的。这时候就要用到having
![[Pasted image 20241019190929.png]]

having是对查询之后的内容进行筛选
where和having可以同时用
### Section 8 limit 范围查询
`select * from info limit 起始位置,数据个数;`
![[Pasted image 20241019192243.png|400]]

offset 跳过数据
`select * from info limit 3 offset 1`：跳过第一条数据，留下剩下的三条
如果只有一个数就默认从0开始
![[Pasted image 20241019192330.png|400]]
- 排序
也可以用order by进行指定
![[Pasted image 20241019192653.png]]

用desc降序，升序用asc，mysql默认是升序
![[Pasted image 20241019192711.png]]

- 注：limit后面的数不能是运算表达式，如下方式是不合法的
```sql
            select distinct salary
            from Employee
            order by salary desc
            limit (N-1),1
```


### Section 8 distinct
作用：去重
![[Pasted image 20241019193155.png]]

平时写语句`select address from info;`，这个是隐藏all的，其实有一个all`select all address from info;`

## Part 2 多表查询
### Section 1 联合查询union
```mysql
select age,gender from info union (all/distinct) select `name`,phone from teacher;
```
- 注意：union前后的字段个数要一样

![[Pasted image 20241024211614.png]]

union是并，intersect是交，except是差

### Section 2 inner join 内连接
两个表之间一定要有公共字段，逗号隔开加where是内连接
- 通过指定相同的字段来访问
```sql
select name,chinese from student inner join score_student on student.id=score_student.id;
```
![[Pasted image 20241024213251.png|300]]
![[Pasted image 20241024213302.png|300]]

![[Pasted image 20241024213333.png|300]]

### Section 3 left join左连接
以左表为基准，左表忽略的表会设置为null，

```sql
select name,chinese from student left join score_student on student.id=score.id;
```

![[Pasted image 20241024214218.png]]

### Section 4 right join 右连接
以右边为基准，右表的内容必须在
![[Pasted image 20241024214603.png]]

### Section 5 crossing join 
- 返回的笛卡尔积
```mysql
select * from info crossing join student;
```
![[Pasted image 20241024214849.png]]

- 如果后面加上where的约束条件就不是笛卡尔积

### Section 6 natural join
自动匹配名字相同的字段，然后选出该字段中值相同的
- 自然内连接
```mysql
select * from t1 natural join t3;
```
t1表A行有一个d列和t3B行一个d列的一个一样，两个表的d列就重合，A行和B行其他的拼到一行，没有一样的就没对上，删掉（只能有一个字段一样），内连接就不会删掉会有两个d列

- 自然左连接
向左看齐，左边表有，右边表没有的，会补齐，只是没有的值会定为NULL
- 自然右连接
向右看齐

- 没有一个公共字段的情况，会返回笛卡尔积

- 如果有两个及以上相同的字段，使用自然连接，就会出现选出来的表都是null的情况

这时候可以使用using来指定要用的字段（一般不用），一般是用on，两个表的属性名相同时可以用using，不同用on
```mysql
select * from t1 natural join t3 using(id);
```

### Section 7 哪个最实用
- 实际应用的时候一般不使用自然连接，using等

- 一般是写全，即使用inner join

## Part 3 子查询

### Section 1 介绍
- 多层查

假如说需要查出分数大于85的学生信息，这时候就要用到子查询（分数表和学生信息表不是同一个）
```mysql
select * from student where id in (select stuid from score where score>=85);
```

注意这里stuid的位置不能用\*，不然就是给多个了，会出现问题，in的地方不能给=因为后面括号中有多个id数据，一个数据才能用=

### Section 2 in和not in

```mysql
select * from student where id not in (select stuid from score where score>=85);
```

多个的方法：（要打括号）
```sql
select distinct Department.name as Department,Employee.name as Employee,Employee.salary as Salary
from Employee inner join Department on Employee.departmentId = Department.id
where (salary,departmentId) in (select max(salary),departmentId from Employee group by departmentId)
```
### Section 3 exists 和 not exists

用上面的例子来说，只要存在括号里的情况，就把所有的学生信息打印出来
```mysql
select * from student where exists (select stuid from score where score>=85);
```
- 比较
`>some`表示至少比某一个大


## Part 3 NULL值相关
### Section 1 数据相关
- count(\*)会算是null的数据

### Section 2 查询时显示null值
- 注：一般null都是空字符串）
以下面题目为例（leetcode176.第二高的薪水）
![[Pasted image 20241119144107.png|300]]
- 要求：查询并返回 `Employee` 表中第二高的 **不同** 薪水 。如果不存在第二高的薪水，查询应该返回 `null(Pandas 则返回 None)` 。
- 例表：![[Pasted image 20241119144253.png|400]]
	![[Pasted image 20241119144413.png|400]]
1. 使用聚合函数，在select后使用聚合函数，如果没有数据会返回null而不是空字符串
```sql
select max(salary) as SecondHighestSalary
from Employee
where salary < (select max(salary) from Employee);
```
2. 不使用from
```sql
select (select distinct salary
from Employee
order by salary desc
limit 1 offset 1)
as SecondHighestSalary
```
3. 使用IFNULLN或ULLIF函数
- 两种函数的介绍
IFNULL(expr1,expr2)，如果expr1的值为null就返回expr2；否则，返回expr1
```sql
select ifnull(select distinct salary
			 from Employee
			 order by salary desc
			 limit 1 offset 1),NULL)
			 as SecondHighestSalary
```

NULLIF(expr1,expr2)，如果expr1=expr2，返回NULL，否则返回expr1，和上面类似用法

### Section 3 涉及函数
如果返回的是整型，就不用担心空结果集的情况，会自动返回NULL
- 例题，leetcode，177.第n高的薪水
![[Pasted image 20241119154646.png|400]]

查询 `Employee` 表中第 `n` 高（要去重）的工资。如果没有第 `n` 个最高工资，查询结果应该为 `null` 。
![[Pasted image 20241119154915.png]]

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
DECLARE M INT;
    SET M = N-1;
  RETURN (
            select distinct salary
            from Employee
            order by salary desc
            limit M,1
  );
END
```
这里函数的定义返回了int类型，所以不用上面的方式使结果为null，也不用重命名，返回的表头就是函数名