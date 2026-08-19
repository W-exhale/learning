## 介绍与查看
- 早期的电脑是不分管理员和普通用户的（Windows XP），所以非常容易中毒。后来就出现了现在的模式，让电脑更安全。
- 每一个用户都有一个唯一的id（UID），来表示用户，使用的时候是用的用户名。
- linux查看用户：`cat /etc/passwd`（自己创建的用户在最后）![Pasted image 20250219105239](images/Pasted%20image%2020250219105239.png)
- 假如说电脑被黑了，也只是拿到了root的权限，还有其他的系统账户，如果想要彻底掌控这台linux，就需要把所有的用户都黑了才行
- 第二个是UID（系统UID基本都是低于500的，要注意不要去改动），冒号后面的是密码，用x代替，第四个是组ID，然后是类似账户描述的东西（备注字段），最后是用户默认使用的shell，倒数第二个是用户的home目录
- 查看密码：`sudo cat /etc/shadow`（都加密了，！表示不存在密码），第一个是用户；，第二个是密码；从上一次修改密码之后过去的天数（从1970.1.1开始算的），多少天之后能修改密码；多少天之后必须修改密码；如果密码过期了，提前多少天提醒用户更改；密码过期多少天之后禁用；禁用日期，从1970年开始算；预留字段
![Pasted image 20250219110409](images/Pasted%20image%2020250219110409.png)

## 用户增删改
- 可以在设置里添加
- 创建用户之后会添加一些默认的用户设置![Pasted image 20250219113340](images/Pasted%20image%2020250219113340.png)
- 添加用户：`sudo useradd t1`（t1是用户名）
- 删除用户：`sudo userdel t1`
- 修改用户：`usermod`（能修改`/etc/passwd`中的大部分文件）
	- 可以查看usermod怎么用![Pasted image 20250219114020](images/Pasted%20image%2020250219114020.png)
	- 修改密码：`sudo passwd t1`（必须sudo才能用）![Pasted image 20250219124757](images/Pasted%20image%2020250219124757.png)
		- `chpasswd`：通过访问txt文件来修改用户密码
		- `chsh`：修改特定账户的信息
		- `chage`：修改时间（chage -h查看用法），修改`/etc/shadow`中的信息
## group组
- 组的目的：共享资源
- 但是linux中不同的发行版不太一样
	- ubuntu会为每一个用户单独创建一个组（与账户名相同），组密码，组ID（GID），属于该组的用户有哪些![Pasted image 20250219143533](images/Pasted%20image%2020250219143533.png)
	- 有些发行版要把所有的用户都纳入一个组，但是不同的岗位的权限不一样，就会很麻烦
	- 使用组的方式最好是自己创一个组，然后把用户添加进去（使用`usermod`命令,-h使用方法）：创建组`sudo group group1`；修改`groupmod`；删除`groupdel group1`

## 文件和文件夹权限
- 第一个表示什么文件类型
d：文件夹
-：是一个文件
l：link文件（符号链接文件）
![Pasted image 20250219144346](images/Pasted%20image%2020250219144346.png)


后面是三个为一组，一共三组：
- rwx：可读，可写，可执行
- rw-：可读，可写，不可执行
![Pasted image 20250220224020](images/Pasted%20image%2020250220224020.png)
- 为什么要分三组？（rwxr-xr-x）
	- 第一组，rwx：创始人的权限
	- 第二组，r-x：下属成员的权限
	- 第三组，r-x：其他组的成员权限

![Pasted image 20250219145118](images/Pasted%20image%2020250219145118.png)

- `chmod`：修改权限的命令（change mode）
- 修改权限时有两种方式（1.用特定字母代表一种，2.用八进制代替）
- 参数：![Pasted image 20250220225237](images/Pasted%20image%2020250220225237.png)
- 符号模式
	- u：文件所有者(user)，g：组员(group)，o：其他人(others)，a：所有用户(all)
	- +：增加权限，-：去除权限，=：重新设置权限
	- `chmod a+r file.txt`（所有人都可读）
	- `chmod +r file.txt`（所有人都可读）
	- `chmod ug+w,o-w file.txt file1.txt`（ug可写file和file1，o不行）
- 八进制：（要记，随意）
	- ![Pasted image 20250220225333](images/Pasted%20image%2020250220225333.png)
	- `chmod 777 file.txt`（将文件改为ugo都可以rwx）
	- SUID位：普通用户在修改文件时可以临时使用root权限（假如说修改密码的时候）![Pasted image 20250220230633](images/Pasted%20image%2020250220230633.png)
	- 如果文件有SUID位，且拥有者有执行权限则为`s`
	- 如果有SUID位，但是拥有者没有执行权限，则为`S`

