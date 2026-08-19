## Linux的任务管理器
- 图形化工具：System Monitor
- top：
	- 显示或管理执行中的程序（任务管理器中的进程），可以查看 CPU 使用率、内存使用率、运行时间等信息。
	- **使用**：在终端输入 `top` 即可启动。
	- q退出
- ps（process status）：有很多不同版本的使用方法，所以解释十分的复杂，用于报告当前系统的进程状态
	- `ps axo pid,comm,pcpu`：查看进程的PID、名称以及CPU 占用率
	- `ps -aux | grep named`：查看named进程详细信息

- pid控制器：类似叫号的代号，每次基本都不同
- 进程的命令大多与ps有关（运维...）
![Pasted image 20250210194451](images/Pasted%20image%2020250210194451.png)

- kill：类似于结束任务（通过pid来结束）：`kill 3009`(pid)
    *   `kill <PID>`：向指定 PID 的进程发送终止信号。
    *   `kill -9 <PID>`：强制终止指定 PID 的进程（发送 `KILL` 信号，应谨慎使用）。
    *   **示例**：`kill 3009` (尝试结束 PID 为 3009 的进程)。
## 挂载
### 概念
*   **挂载 (Mounting)**：将一个存储设备（如硬盘分区、U盘）或文件系统关联到 Linux 文件系统目录树中的一个指定目录（称为**挂载点**，Mount Point）的过程。挂载后，就可以通过访问这个挂载点目录来访问存储设备上的文件。
- **windows中**，电脑插入U盘时，可以选择插入主机还是虚拟机，插入windows系统时，电脑中会多一个USB的盘（有盘符，这是一个虚拟的临时使用盘供用户使用）：虚拟盘创建使用就是挂载，系统的硬盘开启创建属于系统挂载。
- **Linux 中**，设备本身由设备文件表示（如 `/dev/sdb1`），需要通过 `mount` 命令将其关联到一个目录（如 `/mnt/usb_disk`）才能访问。
*   **系统挂载**：系统启动时会自动挂载定义在 `/etc/fstab` 文件中的硬盘分区。
- 在/的mnt目录中创建目录失败，因为mnt是自动挂载的目录，使用权限不能写
	![Pasted image 20250210213636](images/Pasted%20image%2020250210213636.png)

### 手动挂载与卸载
1.  **查看设备**：使用`sudo fdisk -l`：用于列出系统中所有的磁盘和分区信息，可以找到目标设备文件（例如 U 盘对应的 `/dev/sdc1`）。
2. **创建挂载点**：选择或创建一个空目录作为挂载点，通常在 `/mnt` 下，例如 `sudo mkdir /mnt/myusb`。
    *   **注意**：`/mnt` 目录本身通常需要 `root` 权限才能写入（创建子目录）。
3. **挂载设备**：使用 `mount` 命令。
	1.  **命令格式**：`sudo mount <设备文件> <挂载点目录>`
	2. ：`sudo mount /dev/sdc1 /mnt/myusb`
	3. 前面是usb盘的设备文件（在linux上的分区），使用df命令（显示磁盘信息）查看，后面是我们指定的挂载点目录）
4.  **访问文件**：挂载成功后，访问 `/mnt/myusb` 目录即可读写设备中的文件
5.  **卸载设备**：使用 `umount` 命令断开连接。**拔出设备前必须卸载**。
    *   **命令格式**：`sudo umount <挂载点目录>` （取消挂载点）或 `sudo umount <设备文件>`
    *   **示例**：`sudo umount /mnt/myusb`

- 也可以不创建挂载点，直接mount设置挂载点，改变挂载点后去/mnt目录看，会发现usb中的文件在这里也有（相当于映射到两个地方，一个在media，media是自动挂载，一个在mnt）

### 自动挂载
- 自动挂载会为挂载点的目录自动分配目录（media），之前的挂载需要手动操作，不会自动分配、就需要用mount来挂载
*   **挂载点**：自动挂载通常发生在 `/media/<用户名>/<设备标签>` 或 `/run/media/<用户名>/<设备标签>`。
- 自动挂载好处：有的目录没有写入权限，有的有，
	- 防止错误规定挂载点对应目录可以更好的避免安全隐患；
	- 防止恶意自动播放脚本

### 安卓设备挂载
*   **MTP 模式 (Media Transfer Protocol)**：
	* 这是安卓手机默认的文件传输模式。
	* Linux 系统通常通过 `gvfs` (GNOME Virtual File System) 或 `mtpfs` 与设备交互。
	* 访问路径可能类似 `/run/user/1000/gvfs/mtp:host=%5Busb%3A001%2C007%5D/`。
	* **严格来说不算“挂载”**：MTP 是文件传输协议，并没有以传统文件系统的形式挂载，而是通过协议读取和传输文件，不能像本地文件系统一样进行所有操作。
	- 安卓设备是通过mtp协议访问的，不能将一个协议上的东西挂载到另一个地方
*   **ADB (Android Debug Bridge)**：
	* adb工具，通过ADB工具连接到手机
	* 借助linux系统操纵手机，主要用于开发者调试，需手机开启“USB 调试”。
	* 通过 `adb push/pull` 传输文件，或 `adb shell` 访问手机命令行。
	* 通过adb协议访问手机，也不算挂载
*   **大容量存储模式 (Mass Storage Mode)**：
    *   较旧的安卓设备或 SD 卡可能支持此模式。
    *   手机存储（或 SD 卡）被识别为块设备（如 `/dev/sdb`）。
    * 本质是手机的某个存储分区（比如SD卡）会直接挂载到Linux系统，像一个U盘
    * 算挂载
*   **其他工具**：如 `sshfs` (需手机运行 SSH 服务) 可实现类似挂载的效果。
## `df` 和 `du`：检查磁盘使用情况
### `df` (Disk Free)
* **功能**：显示**已挂载**文件系统的磁盘空间使用情况（总容量、已用、可用、使用率、挂载点）。可用的磁盘空间）。默认单位为kb。
*   **常用选项**：
    *   `df`：默认以 KB 为单位显示。
    *   `df -h` (human-readable)：以 K, M, G 等易读单位显示。
    *   `df -T`：显示文件系统类型。
*   **输出解读**：`Mounted on` 列显示挂载点，即挂载到的地方
- 挂载：将某一个分区挂载到某个目录，而不是将某一个目录挂载到某一个目录
![Pasted image 20250216140459](images/Pasted%20image%2020250216140459.png)

### `du` (Disk Usage)
*   **功能**：估算文件和目录占用的磁盘空间。
*   **常用选项**：
    *   `du <目录或文件>`：递归显示指定目录及其子目录下各项的大小。
    *   `du -h <目录或文件>` (human-readable)：以易读单位显示。
    *   `du -s <目录或文件>` (summarize)：仅显示总大小。
    *   `du -sh <目录或文件>`：显示总大小并使用易读单位。
*   **示例**：`du -sh *` 显示当前目录下所有文件和一级子目录的总大小。
![Pasted image 20250216141442](images/Pasted%20image%2020250216141442.png)

## `sort`：文本排序
- **功能**：只能对文本文件的行进行排序做处理，默认按首字母展示出来，但是不改变原文件
*   **常用选项**：
    *   `sort <文件名>`：按字典序排序。
    *   `sort -n` (numeric sort)：按数值大小排序。√
    *   `sort -r` (reverse)：反向排序。
    *   `sort -M` (month sort)：按非月份、月份名称排序（JAN < FEB < ... < DEC），常用于日志文件。√
    *   `sort -k <字段号>` (key)：按指定字段排序。
    *   `sort -t <分隔符>` (field-separator)：指定字段分隔符。
    *   `sort -u` (unique)：去除重复行（只保留第一次出现的行）。
*   **结合管道 `|` 使用**：对其他命令的输出进行排序。
    *   **示例**：`du -sh * | sort -nr`：计算当前目录下各项的大小，然后按大小（`-n`）降序（`-r`）排列。非递归
![Pasted image 20250216142022](images/Pasted%20image%2020250216142022.png)

*   **相关文件示例**：`/etc/passwd` 文件存储用户信息（保存密码），可以用 `sort` 对其内容排序。

## 解压缩文件
Linux压缩软件
*   `gzip`：压缩文件为 `.gz` 格式。解压用 `gunzip` 或 `gzip -d`。
*   `bzip2`：提供更好的压缩率，生成 `.bz2` 文件。解压用 `bunzip2` 或 `bzip2 -d`。
*   `zip`：跨平台兼容性好，生成 `.zip` 文件。压缩和解压都用 `zip` 和 `unzip` 命令。

*   `tar` (Tape Archive)：打包命令，可以将多个文件和目录**打包**成一个单独的归档文件（`.tar` 文件）
- gzip：压缩命令，只能压缩一个文件
- .tar.gz：先打包成一个文件，再压缩

- **常用命令**：`tar -zcvf /tmp/bin-backup.tar.gz /home/vivek/bin/`，将后面目录打包，并用gzip算法压缩，保存为前面文件
	*   `-c` (create)：创建新的归档文件。
	*   `-z` (gzip)：在创建或提取时通过 `gzip` 过滤（压缩/解压缩）。--gzip, --gunzip, --ungzip 通过 gzip 过滤归档
	*   `-v` (verbose)：详细显示处理过程中的文件名。--warning=KEYWORD 警告控制:（显示出所有被打包的文件）
	*   `-f` (file)：这个参数告诉tar后面紧跟的字符串是归档文件的文件名
    *   **仅打包不压缩**：省略 `-z` 选项，输出文件通常命名为 `.tar`。
*   **解压缩包 (`.tar.gz`)**：
    *   命令：`tar -zxvf <压缩文件名.tar.gz> [-C <目标目录>]`
    *   示例：`tar -zxvf mybackup.tar.gz` (解压到当前目录)
    *   选项说明：
        *   `-x` (extract)：从归档文件中提取文件。
        *   `-z`, `-v`, `-f`：含义同上。
        *   `-C <目录>` (可选)：指定解压到的目标目录。

## 在server上安装vmtools
1.  **挂载 VMware Tools ISO**:
    *   首先，在 VMware 软件界面中选择对应虚拟机的菜单选项，通常是 "虚拟机" -> "安装 VMware Tools" (或类似名称)。这会将一个包含安装文件的虚拟 CD-ROM (ISO 镜像) 连接到虚拟机。
    *   在虚拟机内部的 Linux 终端中，使用 `df -h` 或 `lsblk` 命令查找这个虚拟 CD-ROM 的设备文件（也就是vmtools的磁盘分区）路径。它通常显示为 `/dev/sr0` 或 `/dev/cdrom`。
2.  **创建挂载点并挂载**:
    *   创建一个目录作为挂载点，通常在 `/mnt` 下。如果 `/mnt/cdrom` 不存在，则创建它。
		```bash
        sudo mkdir -p /mnt/cdrom 
        ```
    *   使用 `mount` 命令将 CD-ROM 设备挂载到创建的目录。即设置挂载点 *(要将 `/dev/sr0` 替换为上一步找到的实际设备名)*
        ```bash
        sudo mount /dev/sr0 /mnt/cdrom 
        ```
3.  **确认挂载并查找安装包**:
    *   再次运行 `df -h` 确认设备已成功挂载到 `/mnt/cdrom`。
    *   切换到挂载点目录并列出文件，查找 VMware Tools 的压缩包（通常是 `.tar.gz` 文件）。
        ```bash
        cd /mnt/cdrom
        ls
        ```
		*你应该能看到类似 `VMwareTools-x.x.x-xxxx.tar.gz` 的文件。*
4.  **复制并解压安装包**:
    *   将 VMware Tools 压缩包复制到一个临时位置，例如用户的桌面或 `/tmp` 目录，以便进行操作。
        ```bash
        cp VMwareTools-*.tar.gz ~/Desktop/ 
        cd ~/Desktop/
        ```
    *   使用 `tar` 命令解压缩文件。
        ```bash
        tar -zxvf VMwareTools-*.tar.gz
        ```
5.  **运行安装脚本**:
    *   进入解压后生成的目录（通常名为 `vmware-tools-distrib`）。
        ```bash
        cd vmware-tools-distrib/
        ```
    *   以 `root` 权限运行安装脚本 `vmware-install.pl`。根据提示按回车接受默认设置或进行选择。
        ```bash
        sudo ./vmware-install.pl
        ```

6.  **清理**:
    *   安装完成后，可以删除下载的压缩包和解压出的目录。
        ```bash
        cd ~/Desktop/
        rm VMwareTools-*.tar.gz
        rm -rf vmware-tools-distrib/
        ```
    *   卸载之前挂载的 CD-ROM。
        ```bash
        sudo umount /mnt/cdrom
        ```
    *   **注意**: 如果系统自动将 VMware Tools 挂载到了 `/media/<用户名>/VMware Tools` 这样的目录，也需要使用 `umount` 命令卸载它。
        ```bash
        sudo umount /media/<你的用户名>/VMware\ Tools 
        ```
*   **无需复制**: 有时也可以直接在 `/mnt/cdrom` 目录下解压并运行安装脚本，省略第 4 步的复制操作。
*   **挂载点安全**: 在安装软件时，有时会选择非默认的挂载点，并可能设置特定权限（如只读、禁止执行）。这是为了提高安全性，防止潜在的恶意软件利用默认或可写的挂载点进行攻击。
	- 安装软件可能会另选挂载点（设置只读不运行），如果是默认的，可能会被黑客入侵。


