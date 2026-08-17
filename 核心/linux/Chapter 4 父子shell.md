## 父子shell概念
- ubuntu通过软件打开的终端就是bash，也就是自带的shell，从下图可以看出在bin目录里，实际上bash就是一个软件
![[Pasted image 20250217180145.png]]

- 本质上
![[Pasted image 20250217181513.png]]

- 使用`ps --forest`命令可以看出层次
![[Pasted image 20250217181811.png]]

- 使用分号将命令合在一起将会依次执行命令
![[Pasted image 20250217182632.png]]

- 也可以用括号括起来，括号就表示创建了一个子shell来执行（可以用`echo $BASH_SUBSHELL`来看创建了多少子shell，echo是输出指定的字符或变量）
![[Pasted image 20250217183601.png]]

## sleep 和jobs
- sleep命令可以让终端休眠xxx秒后再执行，延迟执行或者放到后台过一段时间执行
![[Pasted image 20250217202059.png]]

300s结束后sleep命令才会消失

- jobs：专门用来查看后台进程
![[Pasted image 20250217202439.png]]

`(tar -zxvf ... ; tar -zxvf ... ; cp ...)&`）（放后台运行，类似最小化）

起别名：`coproc frank_a{ sleep 10; }`（给sleep 10 起了另外一个名字，这种方式叫*协程*，上面那种方式叫*进程*）
这种方式相当于是创建了一个子shell，在子shell的后台里挂着，直接使用`&`，表示在当前shell里最小化

## 外部命令和内建命令
- 任务管理器为什么也算一个进程，`ps -f`为什么也算一个进程
- 执行`ps -f`的时候不能在shell里面看，如果和shell一个进程，就看不全这个shell（如果打开了两个shell，ps是各看各的）
- 这种要跳出去另开一个进程的方式就叫衍生（forking）
- `ps -f`这种要跳去外面单开进程的命令就叫*外部命令*
- `cd`这种不用单开的就叫*非外部命令*（*内建命令*）
- 可以用`type`来检测是什么命令
	- 外部命令：hashed（/usr/bin/ps）（以ps为例）
	- 内建命令：shell bulltin

## history和alias别名
- history命令可以查看之前运行过的所有命令（可以保存一千多条）
- 这一千多条就存在这：![[Pasted image 20250217224350.png]]
- `! 1320`：可以执行history里第1320行命令

- `alias -p`：显示全部已定义的别名![[Pasted image 20250217224802.png]]
- 创建新别名：但是有一点，这种方式重启shell之后就无效了![[Pasted image 20250217225116.png]]