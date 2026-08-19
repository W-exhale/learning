- 下载安装软件的地方很分散，于是出现了包管理系统（PMS，package management system）
- PMS作用：软件安装，更新，卸载
- 但是不同的linux发行版有不同的PMS（pms一般是自动配置环境变量）
- 还有一个原因：存在工具依赖（使用朋友圈一定要下微信）
- 不同发行版最主要的工具（两种）：
	- dpkg（ubuntu，即debian系列）：apt-get，apt-cache，aptitude（使用最后一个可以彻底解决工具依赖问题，但是最好不要用）
		- `sudo apt install sl`（小火车）
		- `apt -h`：apt帮助文档
		- `sudo apt update`相当于软件管家的查找更新（更新软件的）和`sudo apt upgrade`相当于软件管家的一键更新（更新当前的系统和软件）
		- 卸载：`sudo apt remove sl`
		- 
	- rpm（redhat）：yum，urpm

如果要在server上设置镜像源（[Ubuntu 24.04 抢先体验换国内源 清华源 阿里源 中科大源 163源_ubuntu24.04-CSDN博客](https://blog.csdn.net/xiangxianghehe/article/details/136529419)）
![Pasted image 20250218193704](images/Pasted%20image%2020250218193704.png)

- 安装第三方软件（PMS中没有的）
- 假设安装github上的一个项目thefuck
	1. 查看项目的readme
	2. 要添加一下三个依赖（Unbuntu自带python，在`/usr/bin`中查看）![Pasted image 20250218202815](images/Pasted%20image%2020250218202815.png)
	3. 安装依赖及软件，可以使用pip镜像源安装更快![Pasted image 20250218202903](images/Pasted%20image%2020250218202903.png)
	4. 基于debian的系统可能不支持pip![Pasted image 20250218203229](images/Pasted%20image%2020250218203229.png)
	5. 解决方案：1.使用系统包管理器安装；2.创建python虚拟环境，这里使用第二种（[参考](https://blog.csdn.net/iblade/article/details/135002063)）![Pasted image 20250218204008](images/Pasted%20image%2020250218204008.png)
	6. 好吧还是不行...