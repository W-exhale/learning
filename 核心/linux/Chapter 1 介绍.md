## Part 1 常用的Linux发行版
Linux -> Ubuntu、CentOS、Red Hat、Kali
- 主流的三个linux发行版
Debian--->**Ubuntu**、Kali
Fedora--->RedFHat 、**CentOS**
OpenSUSE（德国用的比较多）
类似于小米下面有一个红米，华为下有一个荣耀

- 其他Linux系统：极简版：ArchLinux
- 按是否付费分类
Linux商业发行版：Ubuntu等等
社区发行版

## Part 2 安装
### 安装到vm
假如说vmware中没有对应的版本（比如说kali），就可以直接选它基于的版本（debian）具体的型号需要搜索
![屏幕截图 2024-11-11 091459](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-11%20091459.png)![屏幕截图 2024-11-11 091803](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-11%20091803.png)

![屏幕截图 2024-11-11 091918](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-11%20091918.png)

### 配置镜像源
![屏幕截图 2024-11-11 120704](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-11%20120704.png)
### 下载vmtools
![屏幕截图 2024-11-11 122141](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-11%20122141.png)

![屏幕截图 2024-11-11 122653](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-11%20122653.png)

![屏幕截图 2024-11-11 122726](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-11%20122726.png)

![屏幕截图 2024-11-11 122736](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-11%20122736.png)

## Part 3 Linux 整体概要
linux入门：
1. 体验：比较各个系统的不同点和xiang
2. 正式学习不是GUI（图形界面），而是Shell
[[Linux整体分类.excalidraw|Linux所有部分一览]]
### Section 1 linux操作系统（GNU/Linux）的四个部分
1. Linux kernel 内核
2. GNU工具（重点）
3. GUI desktop环境
4. Application 应用

- 前两点加起来成了linux
[[Linux各部分关系|linux四大部分之间的关系]]：应用软件，GUI，GNU，Linux内核，硬件

### Section 2 Linux的使用环境
实体机，硬件不支持（不推荐）
双系统（不推荐）
虚拟机

### Section 3 Linux内核组成部分
#### 组成部分
鼠标移动：驱动程序（软硬结合）
负责：
1. 连接硬件设备：  管理和使用
2. 软件程序： （系统）->操作软件（操作进程，任务管理器，打开一个应用就会创建一个进程）
3. 系统内存
4. 文件管理：笔记等，保存文件，删除文件，修改文件
#### 细说文件系统
读、写遵循的标准
Linux上有很多文件系统：ext（最早），ext2，ext3，ext4，xfs，brtfs，zfs...（几十个）
windows是NTFS，
![Pasted image 20241120112032](images/Pasted%20image%2020241120112032.png)

- Linux文件系统分区（类似Windows磁盘分区，但是linux没有盘（就一个盘），下面就是linux分的区）
![Pasted image 20241120113345](images/Pasted%20image%2020241120113345.png)
![Pasted image 20241120195303](images/Pasted%20image%2020241120195303.png)

用的比较多的是ext4
U盘文件格式：FAT32 NTFS exFAT
不支持的文件格式可能就会出现一些问题

### Section 4 GNU（是一个组织）
记事本
Unix上具有的一些软件，Linux内核本身没有，所以GNU模仿Unix，为Linux写了一些必要的软件

GNU核心：原本在Unix上的一些命令和工具，被模仿（移植到了Linux上）
供Linux使用的这套工具：coreutils coreutilities 软件包
#### 第一部分工具
1. 用来处理文件的工具
2. 用来操作文本的工具
3. 用来管理进程的工具
#### shell
##### 介绍
 shell ：提供给用户使用的软件，用户用这个来使用电脑，并且和电脑交互

命令行壳层提供一个命令行界面（CLI，command-line interface）；图形壳层提供一个图形用户界面（GUI）
一般说的shell是指CLI
##### shell分类
bash shell：基础shell（最常见）macOS也用的这个shell
zsh：包含了下面三个
ash：不同环境
korn：数学
tcsh：与C语言

oh-my-zsh项目

### Section 5 桌面环境（GUI）
X window ：已过时
KDE：有菜单，任务栏，快捷方式（windows这种）
GNOME：红帽公司（redhat），主要用于linux
Unity：主要用于Ubuntu，和其他的区别是：它不是一个桌面套件