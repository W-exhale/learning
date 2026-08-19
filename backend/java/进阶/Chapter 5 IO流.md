## Part 1 介绍
- I/Ostream：Input/output ，一个过程（流入，流出）

A水库的水通过管道流到B家，对于B来说是input，A来说就是output，而这个管道就是流

- 都是在应用程序的视角来看input还是output
1. 读入
- 例如下图，对于数据源来说就是output，对于program（右边的）来说就是input，中间的就是流
![Pasted image 20241120210825](images/Pasted%20image%2020241120210825.png)
- 比如说我们打开记事本读取东西的时候，对于记事本这个程序来说就是输入（我们也可以将输入理解为获取），获取一个文件也是输入，所以*读文件*的时候是*input*

2. 写入

![Pasted image 20241120211320](images/Pasted%20image%2020241120211320.png)
- 如上图，我们要写入，所以对于数据源而言是input，而对于程序而言是output，而我们都是对程序进行操作，所以写入是output

## Part 2 InputStream和OutputStream
- java中使用I/O流主要就是两个类，但这里两个都是抽象类，所以我们需要使用他们的子类FileInputStream

### Section 1 使用FileInputStream读取文件
- 使用byte进行读取
```java
public void inputFile() throws IOException {  
  
    FileInputStream fileInputStream = new FileInputStream("file/1.txt");  
    int by;//可以不用给0  
    while((by = fileInputStream.read()) != -1){  
        //一个一个读，如果返回-1，说明读到最大了  
        System.out.print((char)by);//强制转换，不转换，就是一次性全部输出  
    }  
    fileInputStream.close();//读完之后要记得关闭内存
}
```

### Section 2 使用FileOutputStream写入文件

```java
public void outputFile() throws IOException{  
    FileOutputStream fileOutputStream = new FileOutputStream("file/2.txt");  
    byte[] bytes = "Exhale!".getBytes();  
    //写入文件  
     for(int x = 0;x < bytes.length;x++){  
         fileOutputStream.write(bytes[x]);  
     }  
     fileOutputStream.close();  
}
```

### Section 3 拷贝
1. 先从一个文件里读取（可以把字节设置大一点）
2. 再写入另一个文件里
```java
public void copyFile() throws IOException {  
  
    FileInputStream fileInputStream = new FileInputStream("C:\\Users\\W_exhale\\Desktop\\picture.png");  
    FileOutputStream fileOutputStream = new FileOutputStream("F:\\练习\\Java\\demo1\\file");  
    //缓冲区  
    byte[] buffer = new byte[1024];  //（字节流，自定义缓冲区）
    int length;  
    while((length = fileInputStream.read(buffer)) != -1){  
        //一个一个读，如果返回-1，说明读到最大了  
        fileOutputStream.write(buffer,0,length);//读length次，1024字节只有1k  
    }  
    fileInputStream.close();  
    fileOutputStream.close();  
}
```
实际上java中是存在该方法的

- 可以使用缓冲字节流，读的更快，上面是一个一个读，这个是一群一群读
```java
public void copyFile() throws IOException {  
    //缓冲区  
    BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream("C:\\Users\\W_exhale\\Desktop\\picture.png"));  
    BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(new FileOutputStream("F:\\练习\\Java\\demo1\\file\\picture.png"));  
  
    int length;  
    while ((length = bufferedInputStream.read()) != -1) {   
        bufferedOutputStream.write(length);  
    }  
    bufferedInputStream.close();  
    bufferedOutputStream.close();  
}
```

-拷贝文件
```java
public void bufferFileBase () throws IOException {  
    //读取写入更快，装饰设计  
    BufferedInputStream bufferedInputStream1 = new BufferedInputStream(new FileInputStream("file/1.txt"));  
    BufferedOutputStream bufferedOutputStream1 = new BufferedOutputStream(new FileOutputStream("C:\\Users\\W_exhale\\Desktop\\2.txt"));  
    int length;  
    while ((length = bufferedInputStream1.read()) != -1) {  
        bufferedOutputStream1.write(length);  
    }  
    bufferedInputStream1.close();  
    bufferedOutputStream1.close();  
}
```

- 实际上java中提供了拷贝文件的方法，在Java.NIO.Files中有个copy....
## Part 3 FileReader 和 FileWriter
- 专门用来处理txt文件（字符）的，处理字符流；字节流可以处理任何文件

属于Reader和Writer

![Pasted image 20241125113530](images/Pasted%20image%2020241125113530.png)

```java
public void fileReaderTest() throws IOException{  
    FileReader fileReader = new FileReader("file/1.txt");  
    int length;  
    while ((length = fileReader.read()) != -1){  
        System.out.print((char)length);  
    }  
    fileReader.close();  
}  
@Test  
public void fileWriterTest() throws IOException{  
        FileWriter fileWriter = new FileWriter("file/2.txt");  
        fileWriter.write("hello!");  //这里会把2.txt里面的内容清楚重写
        fileWriter.close();  
}
```

- 这里也可以用BufferedReader和BufferedWriter类
```java
  @Test  
public void bufferWriterTest() throws IOException{  
    BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter("file/3.txt"));  
  
    bufferedWriter.write("sjdllsklsk");  
    bufferedWriter.newLine();//这个方法专门提供了一个换行符，推荐使用buffer的方式来对txt进行处理
    bufferedWriter.write("jsjcnsk");  
    bufferedWriter.close();  
}
```

```java
    @Test  
public void bufferReaderTest() throws IOException{  
    BufferedReader bufferedReader = new BufferedReader(new FileReader("file/1.txt"));  
    String str;  
    while((str = bufferedReader.readLine()) != null){//int是返回-1，string是返回null  
        System.out.println(str);  
    }  
}
```

## Part 4 其他流
### Section 1 用字节流操作字符流
让字节流转化为字符流再转回来（操纵文本文件）
- InputStreamReader，
![Pasted image 20241125182102](images/Pasted%20image%2020241125182102.png)

- 对应的还有OutputStreamWriter

### Section 2 DateInputStream
- A data input stream lets an application read primitive Java data types from an underlying input stream in a machine-independent way.

存储成员变量等

### Section 3 ObjectInputSteam and ObjectOutputStream
- 传的是对象，不是byte数组，String之类的
- ObjectOutputStream
	- 过滤流/包装流
		- 负责将 Java 对象转换为字节序列（序列化）。
	- 功能
		- 把 Java 对象（Object）变成二进制流。
	- 操作对象
		- 实现了 `Serializable` 接口的对象、基本数据类型。
	- 注意
		- 必须依赖另一个 `OutputStream`（如输出到文件或内存）。（类似于一个中转站，没有存储功能）
### Section 4 PrintStream and PrintWriter
- 打印流
多线程用的，PipedInputStream

javaweb中会用到，请求的分发会用到多线程，读取请求文件的时候就用这个


### Section 5 FilePermission

### Section 6 ByteArrayInputStream and ByteArrayOutputStream
- 自动创建一个byte类型的缓冲区，先把全部的东西都丢到缓冲区，然后一次性运出去
- ByteArrayOutputStream
	- **内存缓冲区**。它在内存中创建一个字节数组来暂存数据。
	- 功能
		- 把数据写入一个可以自动扩容的 `byte[]`。
### Section 7 CharArrayReader and CharArrayWriter
- 和上面的差不多，只不过存的是char

### Section 8 SequenceInputStream
- 假如创建两个Input流，它可以将两个流进行合并变成一个流，还可以提供多个流进行合并（要用到泛型）

### Section 9 RandomAccessFile
如果要指定读取文件的位置（字节流和字符流都是从头到尾一个一个来读的），可以使用这个方法，但是这个类不属于流（只是放在了io包），但是可以操纵文件，随机的从任何一个地方开始进行读取


## Part 5 apache commons io
可以直接去下载jar包

[org.apache.commons.io.file (Apache Commons IO 2.18.0 API)](https://commons.apache.org/proper/commons-io/apidocs/org/apache/commons/io/file/package-summary.html)
- FileUtils

```java
public void writeTest() throws IOException{  
        File fileB = new File("file/2.txt");  
        if(!fileB.exists()){  
            fileB.createNewFile();  
        }  
  
    FileUtils.writeLines(fileB, new ArrayList(Collections.singleton("jfksdfslfkjddk")), true);  
}
```

- 用到了泛型和arraylist，直接加，比较方便
```java
    public void writeTest() throws IOException{  
            File fileB = new File("file/2.txt");  
            if(!fileB.exists()){  
                fileB.createNewFile();  
            }  
  
            ArrayList<Student> arrayList = new ArrayList<>();  
            arrayList.add(new Student("abc",123));  
            FileUtils.writeLines(fileB, arrayList, true);  
    }  
}
```