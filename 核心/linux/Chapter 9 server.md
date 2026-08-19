## 下载安装
- 工具：putty
- 下载：官网下载LTS
- 装好虚拟机后开启，![Pasted image 20250220095705](images/Pasted%20image%2020250220095705.png)

## SSH
- 将服务器连接到putty
	- 先安装相关软件：`sudo apt install net-tools`
	- 使用`ifconfig`命令查看地址：找inet
	- 输入之后发现没有网络，要下载ssh：`sudo apt install ssh`
	- 然后在putty上输入inet
	- 连接成功后，可以修改字体等
	- `apt list --upgradable`：进行更新
	- `sudo apt update`进行更新
- 如果是自己买的服务器，服务器主页的控制面板上会有一个公开的ip，将这个ip输入putty即可
- 也可以用windows自带的终端来连接：输入`ssh ip地址`
- windows中的wsl（可以直接在windows中使用ubuntu）
	- 打开windows功能![Pasted image 20250220150433](images/Pasted%20image%2020250220150433.png)
	- 微软商店中搜索ubuntu选择一个下载