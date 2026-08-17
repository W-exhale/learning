- 软件管理系统
- 官方文档：[ScoopInstaller/Scoop：用于 Windows 的命令行安装程序。 ](https://github.com/ScoopInstaller/Scoop)

## 下载
- 检查版本(PowerShell)
`$PSVersionTable.PSVersion # has to be >= 5.1`

- 确保PowerShell执行本地脚本：`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
	- **`Set-ExecutionPolicy`**: 用于更改 PowerShell 的脚本执行策略。
	- **`ExecutionPolicy RemoteSigned`**:
	    - `RemoteSigned` 表示：本地创建的脚本可以运行，但从互联网下载的脚本需要被数字签名。      
	- **`Scope CurrentUser`**:
	    - 仅对当前用户生效，不会影响系统的其他用户。
	    - 适合需要临时或用户级别更改而不影响全局策略的场景。

- 安装：`irm https://get.scoop.sh | iex`，这是`Invoke-RestMethod -Uri "https://get.scoop.sh" | Invoke-Expression`的简写
![[Pasted image 20250326083258.png]]

## 将通过scoop下载的软件安装到其他地方
**使用 `scoop config` 只修改软件安装目录**

如果你只想修改 Scoop 的软件安装路径，而不影响 Scoop 本身的位置，可以运行：
`scoop config global_path D:\ScoopApps`

这样，所有安装的软件都会放到 `D:\ScoopApps`，而 Scoop 本身还是在默认位置。

- 安装的时候要使用全局安装
`scoop install -g maven`
## 使用
- 使用`scoop help`看命令的使用方式，或者`scoop help <command>`
- find app（假如我们要找ssh命令，但是不知道在哪）：`scoop search ssh`![[Pasted image 20250326084121.png]]
- 更新：`scoop update`
	- `scoop update curl`
	- `scoop update *`
- 下载：`scoop install git`

## bucket
- Scoop分为多个分类仓库(`bucket`)，默认情况下，使用的是`main`，如果需要安装其他仓库的软件，可以添加对应的`bucket`
- `scoop bucket list`：![[Pasted image 20250326090501.png]]
- 添加新的`bucket`：`scoop bucket add <仓库名>`
	- 例如：`scoop bucket add extras`
- 删除已添加的`bucket`：`scoop bucket rm <仓库名>`

## aria2
### 使用
- 通过多线程提升下载速度
- `scoop install aria2`
- 确认安装：`aria2c --version`
- 下载文件：`aria2c http://example.com.file.zip`
- 多连接下载（使用`-x`参数指定最大连接数，下面表示最多使用16个连接下载）：`aria2c -x 16 http://example.com.file.zip`
- 批量下载（创建一个包含下载链接的文本文件，如`urls.txt`，-i参数用于指定下载链接文件，每行一个链接）：`aria2c -i urls.txt`
- 限制下载速度：`aria2c --max-download-limit=500K https://example.com/file.zip`
- 断点续传（如果下载被中断，`aria2` 可以从断点处继续下载）：`aria2c -c https://example.com/file.zip`
- 下载种子文件：`aria2c file.torrent`
- 下载磁力链接：`aria2c "magnet:?xt=urn:btih:<磁力链接哈希值>"`
- 自定义输出文件名（如果希望下载的文件保存为特定名称，可以使用 `-o` 参数）：`aria2c -o custom_name.zip https://example.com/file.zip`
### 配置
```
# 最大线程数
max-concurrent-downloads=10
# 每个文件的连接数
split=16
# 下载路径
dir=C:/Downloads
# 启用断点续传
continue=true
# 最大下载速度（单位：字节）
max-download-limit=0
# 启用日志记录
log=C:/aria2/aria2.log
```

### 启用后scoop下载失败
- 临时禁用（禁用后Scoop将恢复到默认的下载方式）：`scoop config aria2-enabled false`
- 出现 `aria2` 的警告信息：在启用 `aria2` 时，Scoop 默认会显示警告信息。可以使用以下命令关闭警告：`scoop config aria2-warning-enabled false`
- 下载速度未提升：
	- 检查是否被网络限制了多线程连接。
	- 优化 `aria2` 的配置文件，例如增加最大连接数或调整分段大小。
```
split=16
max-concurrent-downloads=10
min-split-size=1M
```
- 检查 Scoop 当前是否启用了 `aria2`：`scoop config`
	- 输出中如果看到 `aria2-enabled: true`，说明 `aria2` 已启用。
- 完全禁用 `aria2`：`scoop config aria2-enabled false`
	- Scoop 会切换回默认的下载方式。

![[Pasted image 20250326093004.png]]


## 配置Scoop
- `scoop config`
