## Part 1 命令、环境、包
文本排版（Typesetting Text）
### 序（preamble）
- 序的基本结构
![[Pasted image 20241105192448.png]]

### 块

在`\begin{document}`和`\end{document}`中进行编辑写作

`\begin和\end`的使用就类似于创建了一个环境供其中的文本使用
### 符号使用
- 引号
左引号：\`，\`\`
右引号：'，''

使用%，$，&，#需要使用\\

### 数学公式
数学公式大致同markdown
- 括号：左括号用`\left`，右括号用`\right`
单独一行的数学公式
不用四个$，用如下方式：
```
\begin{equation}
x=\frac{-b \pm \sqrt{b^2-4ac}}{2a}
\end{equation}
```
- 注意：在里面不能有空行，必须每行都有，有空行就会报错。

\$...\$的方式就类似于`\begin{math}...\end{math}`
### 列表
- itemize和enumerate创造列表环境
![[Pasted image 20241105191446.png]]

![[Pasted image 20241105192130.png]]

### 使用amsmath包

我们需要在序（preamble）中导入我们所需要的包
例如：amsmath 来自 American Mathematical Society
`\usepackage{amsmath}`
在amsmath包中可以使用未编号的方程，带\*是这个包里特有的
```
\begin{equation*}
x=\frac{-b \pm \sqrt{b^2-4ac}}{2a}
\end{equation*}
```
bad那条会报错，必须用花括号包起来
![[Pasted image 20241105193341.png]]

这样输出右侧就没有编号
![[Pasted image 20241105193626.png|400]]

还可以用`\operatorname`，会加粗Cov属于运算符，会变成数学专用的符号样式
![[Pasted image 20241105193857.png]]

对齐：
![[屏幕截图 2024-11-05 194137.png]]

### 练习
![[Pasted image 20241105200556.png]]

![[Pasted image 20241105200610.png]]

-注意：正常的N就是手写体，所以不用加\\operatorname，如果要用可以用上面注释中的方式。

## Part 2 结构化文档

### 标题和摘要（abstract）

```latex
\documentclass{article}
\usepackage{amsmath}

\title{Test}
\author{W\_ exhale}
\date{\today}

\begin{document}
\maketitle %comment here...:to actually create the title

\begin{abstract}
Abstract goes here...
\end{abstract}

\end{document}
```

![[Pasted image 20241106202011.png|500]]

### 段落（Section）
```latex
\section{Introduction}
The problem of \ldots

\section{Method}
%使用\section*{Method}可以去数字
We investigate \ldots

\subsection{Sample Preparation}
%同上去数字
\subsection{Data Collection}
\section{Results}
\section{Conclusion}
```
![[Pasted image 20241106202356.png|600]]


### 标签（label）和交叉引用（Cross-References）

```latex
\section{Introduction}
\label{sec:intro}
In Section \ref{Sec:method}

\section{Method}
\label{Sec:method}
We investigate \ldots

\begin{equation}
    \label{eq:euler}
    e^{i\pi}+1=0
\end{equation}

By \eqref{eq:euler},we have \ldots

```

![[Pasted image 20241106203310.png|500]]

- \\eqref位于amsmath包中，\\label用于设置标签，\\ref用于引用标签

## Part 3 图片和表

### 图片
![[Pasted image 20241106210939.png]]

![[Pasted image 20241106210952.png]]

- 上面0.5表示占周围文本的50%，caption表示题注，可以设置一个label，用ref引用

```latex
\documentclass accepts optional arguments, too. Example:
\documentclass[12pt,twocolumn]{article}
```

- 12pt控制字体大小，twocolum两列

###  表 table
- 需要用到tabularx包

lrr表示left，right，right
```latex
\begin{tabular}{lrr}
   Item   & Qty & Unit \$ \\
   Widget &1    & 199.99  \\
   Gadget &2    & 300.99  \\
   Cable  &3    & 19.99   \\
\end{tabular}
```

![[Pasted image 20241106212328.png]]

```latex
\begin{tabular}{|l|r|r|} \hline %l|r|r|中间的|表示竖线
Item & Qty & Unit \$ \\ \hline
Widget & 1 & 199.99 \\
Gadget & 2 & 399.99 \\
Cable & 3 & 19.99 \\ \hline %hline表示横线
\end{tabular}
```

![[Pasted image 20241106212534.png]]


## Part 4 文献引用
需要将文献以‘bibtex’数据库格式放入.bib文件中，大多数文献都可以导出为bibtex格式
- 使用natbib包
Reference *\bibliography* at the end, and specify a *\bibliographystyle*.

![[Pasted image 20241106213923.png]]

还可以用biblatex包，但大部分都在natbib里有

## Part 5 演示文档beamer