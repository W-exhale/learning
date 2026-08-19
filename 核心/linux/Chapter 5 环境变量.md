
## 什么是环境变量
- 我们执行一个程序的时候，比如说记事本（notepad），必须找到notepad在哪，我们才能执行，计算机（calc）也是如此
- windows中的notepad在C盘windows的system32里，为什么可以在任何目录下使用notepad。![Pasted image 20250218153409](images/Pasted%20image%2020250218153409.png)

## Windows环境变量
- windows环境变量
	- 系统变量
		- 我们可以看到系统变量中有一个![Pasted image 20250218154156](images/Pasted%20image%2020250218154156.png)
		- 比如说在D盘输入notepad，它就会先在环境变量中找（有种预定位置的感觉）
	- 用户变量
		- 电脑有多个用户，系统变量对所有用户有效，用户变量只对特定的用户有用

## Linux中的‘环境变量’
- linux中则分为全局变量和局部变量：全局变量全大写并且用下划线隔开，局部变量全小写用下划线隔开
	- 全局变量：
		- *解释*：比如说ls在任何目录都能用，说明ls就是一个全局变量（本质上是一个软件）。查看所有全局变量的命令：`printenv`![Pasted image 20250218155943](images/Pasted%20image%2020250218155943.png)不同的发行版全局变量是不一样的
		- *查看对应的全局变量*：（`$HOME` 中\$就表示后面跟的是全局变量名的名称，所以`$HOME`就相当于/home/exhale）![Pasted image 20250218161020](images/Pasted%20image%2020250218161020.png)
		- *使用\$*：`ls $HOME`就是查看用户目录的意思`ls /home/exhale`
		- *定义全局变量*：`export $shell`（但是只能在一个shell框里用，退出再打开就不行了）![Pasted image 20250218165514](images/Pasted%20image%2020250218165514.png)
	- 局部变量
		- 解释：只能在当前shell(bash)使用，关掉就不行了
		- 查看局部变量：`set`
		- 用的少
		- 定义局部变量：`hello="world"`（即使是子shell也不行，只能在本shell使用）![Pasted image 20250218162511](images/Pasted%20image%2020250218162511.png)

- 设置linux系统变量：在PATH里设置
- 假如安装mysql，mysql不帮我们配置，在上面path的目录里都没有mysql，我们就要追加命令（但是这种方式设置完之后关掉shell又没有了）![Pasted image 20250218170740](images/Pasted%20image%2020250218170740.png)
## 永久配置linux的path初步认识
- linux有一个启动文件（开机的时候默认执行的文件）
- 环境变量就在这个启动文件里，启动文件最主要的（没有后缀的文件）是`/etc/profile`（ubuntu）![Pasted image 20250218172320](images/Pasted%20image%2020250218172320.png)
- 各种发行版常见的启动配置文件
	- `~/.bashrc`（ubuntu）
	- `~/.bash_profile`
	- `~/.profile`
	- `~/.bash_login`
只有找到这些文件（其中之一）才能够真正的修改系统里的全局变量，如果要编辑上面的文件需要用到vim（或者其他编辑器）
ubuntu：![Pasted image 20250218173037](images/Pasted%20image%2020250218173037.png)
centOS：（centOS用不了ll命令只能用`ls -alF`表示）
![Pasted image 20250218173551](images/Pasted%20image%2020250218173551.png)
