## 整型
- int数值类型
也分有符号和无符号，范围和之前一样

TINYINT，1
SMALLINT，2
MEDIUMINT，3
INT，4
BIGINT，8

在mysql中使用是：
![Pasted image 20241008200054](images/Pasted%20image%2020241008200054.png)

创建之后会有显示一个默认宽度，如下括号中的数字，数字表示的是宽度（设置元组的值可以超过该宽度，但是不可以超过该类型本身的最大值）
![Pasted image 20241008200131](images/Pasted%20image%2020241008200131.png)


## 浮点型
FLOAT：4
DOUBLE：8

-在mysql中使用：

逗号前是整数部分，逗号后是小数部分

![Pasted image 20241008201741](images/Pasted%20image%2020241008201741.png)

-看第三行，小数部分多了会四舍五入，少了会添0
![Pasted image 20241008201833](images/Pasted%20image%2020241008201833.png)

-再来看双精度
![Pasted image 20241008202000](images/Pasted%20image%2020241008202000.png)

会出现丢失精度的情况，所以一般钱的表达一般不会使用double。
double是把小数先转换成二进制数，再转换成小数来显示的，如果第一个转换转换成无限循环小数，那么在转换回来就无法精确表示前面的值，造成精度丢失。
https://blog.csdn.net/weixin_45729934/article/details/121389109

所以一般double只用于科学计算。

## 定点数
钱的金额可以用这个类型。

DECIMAL，没有范围，依靠括号（M,D）里的值，如果M>D，就是M+2，否则D+2（其实就是哪个大看哪个+2）

不会丢失精度，但是小数后面的位数还是按规定的来
![Pasted image 20241008203128](images/Pasted%20image%2020241008203128.png)

定点数的小数和整数是分开存的，所以不会丢失精度。
但是这样占的空间就会增多

## 字符串类型

CHAR，（0-255字符），效率比varchar的更高
VARCHAR，会回收多余的数据（0-65535字符），变长字符串
TINYBLOB
BLOB
TEXT，长文本数据，常用类似于我们写博客的时候，一篇文章
MEDIUMBLOB，
LONGBLOB
LONGTEXT,

## 布尔类型

有true和false两种

![Pasted image 20241008205039](images/Pasted%20image%2020241008205039.png)


## 枚举类型
可以限制填入的内容

![Pasted image 20241008205852](images/Pasted%20image%2020241008205852.png)

在枚举中是以整数的方式来存储的，第一个存的是1，第二个是2...，所以也可以通过整数的方式来设置值

![Pasted image 20241008210133](images/Pasted%20image%2020241008210133.png)

枚举类型的好处：两个字节，速度快，限制数据，以数字的方式访问

## set类型
取多个数据，

假如说需要设置多个爱好，这时候就可以用到set，但是不能设置两个分开来的，会报错。可以设置一个。就相当于是设置多个时的逗号放在单引号里面。

第一个是2的0次方，第二个是2的1次方...
![Pasted image 20241008211712](images/Pasted%20image%2020241008211712.png)

![Pasted image 20241008210950](images/Pasted%20image%2020241008210950.png)

## 时间和日期类型
每一张表都必须有日期和时间类型。
DATE
TIME
YEAR
DATETIME
TIMESTAMP
![Pasted image 20241008211933](images/Pasted%20image%2020241008211933.png)

![Pasted image 20241008212329](images/Pasted%20image%2020241008212329.png)

一般实际应用的时候不是手动输入，会在程序开始的时候自动获取。