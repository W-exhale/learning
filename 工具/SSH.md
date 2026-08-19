## 算法
- RSA
- ED25519：✅
- ECDSA



## 生成
- `ssh-keygen -t ed25519 -C "你的邮箱"`
	- -t：算法类型
- 之后按 Enter
- 设置密码-->后续每次使用私钥都需要输入密码
- 



## 使用
- 公钥可以放到 github 中使用

- 22 端口改成 443 端口走 https
	- `～/.ssh` 下创建 config 文件
	- 输入
		```
		Host github.com
		    HostName ssh.github.com
		    User git
		    Port 443
		    IdentityFile ~/.ssh/id_ed25519
		```
	- 测试
		- `ssh -T git@github.com`：出现 `Hi W-exhale! You've successfully authenticated, but GitHub does not provide shell access.`
		- `ssh -vT git@github.com`：出现 `Connecting to ssh.github.com port 443`








