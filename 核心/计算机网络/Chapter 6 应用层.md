## Part 1 功能
- ![Pasted image 20260101011425](images/Pasted%20image%2020260101011425.png)
- 网络应用模型
	- ![Pasted image 20260101011521](images/Pasted%20image%2020260101011521.png)
	- ![Pasted image 20260101011556](images/Pasted%20image%2020260101011556.png)

- DNS
	- ![Pasted image 20260101011634](images/Pasted%20image%2020260101011634.png)
	- ![Pasted image 20260101011730](images/Pasted%20image%2020260101011730.png)
	- ![Pasted image 20260101011806](images/Pasted%20image%2020260101011806.png)
	- ![Pasted image 20260101011850](images/Pasted%20image%2020260101011850.png)
- www
	- ![Pasted image 20260101011951](images/Pasted%20image%2020260101011951.png)
	- ![Pasted image 20260101012020](images/Pasted%20image%2020260101012020.png)
	- ![Pasted image 20260101012052](images/Pasted%20image%2020260101012052.png)
	- ![Pasted image 20260101012117](images/Pasted%20image%2020260101012117.png)
	- ![Pasted image 20260101012202](images/Pasted%20image%2020260101012202.png)
- ![Pasted image 20260101012242](images/Pasted%20image%2020260101012242.png)
- ![Pasted image 20260101012259](images/Pasted%20image%2020260101012259.png)

- HTTP
	- ![Pasted image 20260101012342](images/Pasted%20image%2020260101012342.png)
	- ![Pasted image 20260101012501](images/Pasted%20image%2020260101012501.png)
- ![Pasted image 20260101012528](images/Pasted%20image%2020260101012528.png)





- ![[Pasted image 20251021102836.png|500]]

- DNS
	- UDP53
	- 域名解析协议，记录域名与IP的映射关系
	- 作用
		- 简化网址记忆
		- 将域名（文字标识的网址）解析为IP地址
		- 负载均衡
		- 故障转移
- DHCP，Dynamic Host Configuration Protocol（动态主机配器协议）
	- UDP67
	- *IP地址自动分配*
	- DHCP客户机首次启动时
		- 客户机向DHCP服务器发送一个Dhcgdiscover数据包，该数据包表达了客户机的IP租用请示
		- 在大多数情况下，客户机接受收到的第一个dhcpoffero使用DHCP服务时，可以通过保留IP与MAC地址保证某台计算机使用固定的地址。
- SNMP
	- 简单网络管理协议，支持*网络管理系统*
	- 用以监测连接到网络上的设备是否有任何引起管理上关注的情况
	- 端口：UDP161
- TFTP 
	- 简单文件传输协议
	- 用来在客户机与服务器之间进行简单文件传输的协议，提供不复杂、开销不大的文件传输服务。
	- TFTP建立在UDP之上
	- 提供不可靠的数据流传输服务，不提供存取授权与认证机制，使用超时重传方式保证数据的到达。





- HTTP（HyperText Transfer Protocol，超文本传输协议）
	- 超文本传输协议
	- 网页传输
	- 客户端浏览器或其他程序与WEB服务器之间的应用层通信协议
	- 端口：TCP80

- FTP 
	- 文件传输协议
	- 网络上两台计算机传送文件的协议
	- 控制连接由客户端主动建立
	- FTP在客户机与服务器之间需建立两条连接
	- 端口
		- TCP21：传送控制信息
		- TCP20：传送文件内容

- SMTP（Simple Mail Transfer Protocol，简单邮件传输协议）
	- *邮件发送*
	- 端口：TCP25
	- 传输的邮件报文采用（ ASCII ）格式表示

- POP
	- 邮局协议，用于*接收邮件*
	- POP3，全名为“Post Office Protocol - Version 3”
		- 协议特性
			- 默认端口：TCP110；
			- 适用的构架结构：C/S；  
			- 访问模式：离线访问。
		- 采用（ C/S ）模式进行通信
		- 当客户机需要服务时，客户端软件与POP3服务器建立（ TCP ）连接