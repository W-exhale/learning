## Part 1 网络层功能
- ![[Pasted image 20251231151536.png]]

- 为传输层提供服务，将传输层数据封装成“IP数据包”（分组）。网络中的路由器根据IP数据包首部中的源IP地址、目的IP地址进行“分组转发”
- 实现“主机到主机”的传输
- 数据链路层
	- 实现节点到节点的传输
- 路由与转发
- SDN概念
- 拥塞控制
![[Pasted image 20251231152458.png]]
## Part 2 IPv4
### 1. IPv4分组
- 各协议之间的关系
	- ![[Pasted image 20251231212357.png]]

- ip数据报
	- ![[Pasted image 20251231212447.png]]
- IPv4分组
	- ![[Pasted image 20251231212547.png]]
	- ![[Pasted image 20251231212631.png]]
	- ![[Pasted image 20251231212703.png]]
	- 格式
		- ![[Pasted image 20251231212800.png]]
		- ![[Pasted image 20251231212847.png]]
- 生存时间
	- ![[Pasted image 20251231212941.png]]
	- ![[Pasted image 20251231213001.png]]
- ![[Pasted image 20251231213038.png]]

### 2. IPv4地址与NAT
- ![[Pasted image 20251231213702.png]]
- ![[Pasted image 20251231213752.png]]
- ![[Pasted image 20251231213913.png]]
- ![[Pasted image 20251231214023.png]]
	- ![[Pasted image 20251231214216.png]]
- 


### 3. 子网划分与子网掩码

- ![[Pasted image 20251231214400.png]]
- ![[Pasted image 20251231214425.png]]
- ![[Pasted image 20251231214657.png]]
- ![[Pasted image 20251231214733.png]]

### 4. 无分类编址CIDR
- 为什么提出？
	- ![[Pasted image 20251231215050.png]]

- 介绍
	- ![[Pasted image 20251231215134.png]]




- CIDR地址块的子网划分
	- 定长子网划分
		- ![[Pasted image 20251231215210.png]]
		- 传统定长子网划分
			- ![[Pasted image 20251231215345.png]]
	- 变长子网划分
		- ![[Pasted image 20251231215220.png]]
		- ![[Pasted image 20251231215519.png]]
		- 使用哈夫曼树
			- ![[Pasted image 20251231220139.png]]
		- 
- ![[Pasted image 20251231220541.png]]

### 5. 路由聚合
- ![[Pasted image 20251231220747.png]]
- 理解
	- 最长哈夫曼顶端
	- ![[Pasted image 20251231221031.png]]
	- ![[Pasted image 20251231220925.png]]
- ![[Pasted image 20251231221755.png]]
- ![[Pasted image 20251231221819.png]]


### 6. NAT网络地址转换
- network address translation
- ![[Pasted image 20251231222733.png]]
- ![[Pasted image 20251231222812.png]]
- ![[Pasted image 20251231223447.png]]

- ![[Pasted image 20251231223608.png]]

- 缓解IP地址不够用的问题（设置端口号）
	- ![[Pasted image 20251231225033.png]]
	- ![[Pasted image 20251231225300.png]]
	- ![[Pasted image 20251231225338.png]]
- 原理示意
	- ![[Pasted image 20251231225504.png]]


### 7. ARP地址解析协议
- ![[Pasted image 20251231225721.png]]
- ![[Pasted image 20251231225808.png]]
- ![[Pasted image 20251231230046.png]]
- ![[Pasted image 20251231230106.png]]
- ![[Pasted image 20251231230136.png]]

### 8. DHCP与ICMP
#### DHCP动态主机配置协议
- ![[Pasted image 20251231230241.png]]
- ![[Pasted image 20251231230319.png]]

- ![[Pasted image 20251231230414.png]]
- ![[Pasted image 20251231230507.png]]

#### ICMP
- 网际控制报文协议
	- Internet Control Message Protocol

- ![[Pasted image 20251231230724.png]]
- ![[Pasted image 20251231230736.png]]
- 差错报告
	- ![[Pasted image 20251231230907.png]]
	- ![[Pasted image 20251231230938.png]]
		- ![[Pasted image 20251231231430.png]]
	- ![[Pasted image 20251231231020.png]]
	- ![[Pasted image 20251231231105.png]]
	- ![[Pasted image 20251231231136.png]]
- 询问报文
	- ![[Pasted image 20251231231229.png]]
		- ![[Pasted image 20251231231241.png]]
	- ![[Pasted image 20251231231314.png]]

## Part 3 IPv6
- 特点
	- ![[Pasted image 20251231231614.png]]
- “冒号十六进制”
- IPv6地址
	- ![[Pasted image 20251231231719.png]]
- ![[Pasted image 20251231231816.png]]
- 分类
	- ![[Pasted image 20251231231836.png]]

- ![[Pasted image 20251231231909.png]]

## Part 4 路由算法与路由协议
### 1. 路由算法
#### 概念
- 路由算法和路由协议
	- ![[Pasted image 20251231232340.png]]
- 本质
	- ![[Pasted image 20251231232419.png]]
- 静态路由与动态路由
	- ![[Pasted image 20251231232520.png]]
- 
#### 距离-向量路由算法（动态路由）
- RIP
- ![[Pasted image 20251231232618.png]]
- ![[Pasted image 20251231232655.png]]
- ![[Pasted image 20251231232721.png]]

#### 链路状态路由算法（动态路由）
- OSPF
- ![[Pasted image 20251231232845.png]]
- ![[Pasted image 20251231232907.png]]
- ![[Pasted image 20251231232927.png]]


#### 分层次的路由协议
- ![[Pasted image 20251231233044.png]]
- 自治系统
	- ![[Pasted image 20251231233225.png]]
	- ![[Pasted image 20251231233255.png]]
	- ![[Pasted image 20251231233321.png]]
- ![[Pasted image 20251231233342.png]]

### 2. 路由协议
#### RIP路由协议
- 路由信息协议（Routing Information Protocol）

- 在协议栈中的位置
	- ![[Pasted image 20251231233618.png]]

- RIP的规定
	- 如何定义路径长度
	- 如何定义路由表（距离向量）格式
	- ![[Pasted image 20251231233728.png]]
- 运行RIP的路由器之间如何交换必要信息
	- ![[Pasted image 20251231233955.png]]
- 工作过程示例
	- ![[Pasted image 20251231234057.png]]
	- ![[Pasted image 20251231234123.png]]
	- ![[Pasted image 20251231234204.png]]
	- ![[Pasted image 20251231234232.png]]
	- ![[Pasted image 20251231234254.png]]
	- ![[Pasted image 20251231234334.png]]
	- ![[Pasted image 20251231234319.png]]
	- ![[Pasted image 20251231234400.png]]


#### OSPF路由协议
- 开放最短路径优先协议

- 在协议栈中的位置
	- ![[Pasted image 20251231234529.png]]
- 特点
	- ![[Pasted image 20251231234555.png]]
	- ![[Pasted image 20251231234615.png]]
	- ![[Pasted image 20251231234639.png]]
	- ![[Pasted image 20251231234702.png]]

- 基本工作原理
	- ![[Pasted image 20251231234730.png]]
	- ![[Pasted image 20251231234906.png]]
	- ![[Pasted image 20251231234920.png]]
		- ![[Pasted image 20251231234937.png]]
	- ![[Pasted image 20251231234949.png]]
- ![[Pasted image 20251231235006.png]]
	- ![[Pasted image 20251231235022.png]]
- ![[Pasted image 20251231235047.png]]
- ![[Pasted image 20251231235059.png]]
- 易混淆的缩写
	- ![[Pasted image 20251231235127.png]]
	- ![[Pasted image 20251231235209.png]]
- 分组类型
	- ![[Pasted image 20251231235239.png]]
	- ![[Pasted image 20251231235323.png]]
		- ![[Pasted image 20251231235358.png]]
	- ![[Pasted image 20251231235422.png]]
	- ![[Pasted image 20251231235442.png]]
	- ![[Pasted image 20251231235505.png]]
	- ![[Pasted image 20251231235525.png]]
	- ![[Pasted image 20251231235537.png]]
	- ![[Pasted image 20251231235600.png]]
	- 
- ![[Pasted image 20251231235305.png]]
	- 
#### BGP路由协议
- 边界网关协议
	- ![[Pasted image 20251231235653.png]]
- 特点
	- ![[Pasted image 20251231235728.png]]
	- ![[Pasted image 20251231235738.png]]
	- ![[Pasted image 20251231235749.png]]
	- ![[Pasted image 20251231235811.png]]
- 概念
	- ![[Pasted image 20251231235828.png]]
	- ![[Pasted image 20251231235857.png]]
	- ![[Pasted image 20251231235916.png]]
- ![[Pasted image 20251231235704.png]]
- 工作原理
	- ![[Pasted image 20260101000825.png]]
	- ![[Pasted image 20260101000845.png]]
- 路由选择
	- ![[Pasted image 20260101000916.png]]
- 四种报文
	- ![[Pasted image 20260101001022.png]]
## Part 5 IP 多播
- 概念
- IP多播地址

## Part 6 网络层设备
- 路由器的组成与功能

- 路由表与路由转发