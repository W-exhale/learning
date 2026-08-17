- 可以连接数据库的API
- 含义：一套规范，Java数据库连接（Java Database Connectivity），用来规范客户端程序如何来访问数据库的应用程序接口，提供查询和更新数据库中数据的方法，面向关系型数据库。

- 连接数据库的方式
![[Pasted image 20250122143827.png|400]]
![[Pasted image 20250122144205.png|400]]
之后就是正常的建表操作

- 这是建立的表
![[Pasted image 20250122152711.png]]

```java
public class JDBCDemo01 {  
    public static final String URL = "jdbc:mysql://localhost:3306/student";  
    public static final String USER = "root";  
    public static final String PASSWORD = "tong051114";  
    public static final String DRIVER = "com.mysql.jdbc.Driver";  
  
  
    public static Connection connection;  
    public static Statement statement;  
    public static ResultSet resultSet;  
  
    public static void main(String[] args) throws SQLException {  
        try {  
            //1.加载驱动程序  
            Class.forName(DRIVER);  
            //2.获得数据库连接对象  
            connection = DriverManager.getConnection(URL, USER, PASSWORD);  
            //3.获得数据库操作对象  
            statement = connection.createStatement();  
            //4.进行操作  
            resultSet = statement.executeQuery("select * from info");  
            //将结果集输出  
            while(resultSet.next()){  
                int id = resultSet.getInt(1);  
                String name = resultSet.getString(2);  
                int age = resultSet.getInt(3);  
                System.out.println("id :"+ id + ", name :" + name + ", age: "+ age);  
            }  
  
        } catch (Exception e) {  
            e.printStackTrace();  
        }finally {  
            try {  
            //关闭连接，资源释放，按出栈顺序释放
                resultSet.close();  
                statement.close();  
                connection.close();  
            } catch (SQLException e) {  
                e.printStackTrace();  
            }  
        }  
    }  
}
```
![[Pasted image 20250122152911.png]]

- 但是有一个问题，假如说我们不只需要selectAll函数，还需要selectById函数，那么我们就需要将上面的四个步骤又重复一遍：
```java
//1.加载驱动程序  
Class.forName(DRIVER);  
//2.获得数据库连接对象  
connection = DriverManager.getConnection(URL, USER, PASSWORD);  
//3.获得数据库操作对象  
statement = connection.createStatement();  
//4.进行操作  
resultSet = statement.executeQuery("select * from info");  
```

- 为避免重复，我们可以使用配置文件，util是工具类文件
![[Pasted image 20250122154615.png]]

- 使用properties，要注意db.properties文件中的字符不用双引号

```java
public class JDBCDemo01 {  
    public Connection connection;  
    public Statement statement;  
    @Test  
    public void insertTest(){  
        try {  
            connection = JDBCUtils.getConnection();  
            statement = connection.createStatement();  
            String sql = "DELETE FROM info where id = 5";  
            int res = statement.executeUpdate(sql);  
  
            if(res > 0){  
                System.out.println("delete success!");  
            }  
  
        } catch (Exception e) {  
            e.printStackTrace();  
        }finally {  
            try {  
                JDBCUtils.close(connection,statement);  
            } catch (SQLException e) {  
                e.printStackTrace();  
            }  
        }  
    }  
     @Test  
    public void selectAll(){  
        try {  
            connection = JDBCUtils.getConnection();  
            statement = connection.createStatement();  
  
            String sql = "select * from info";  
  
            resultSet = statement.executeQuery(sql);  
  
            while(resultSet.next()) {  
                int id = resultSet.getInt(1);  
                String name = resultSet.getString(2);  
                int age = resultSet.getInt(3);  
                System.out.println("id :" + id + ", name :" + name + ", age: " + age);  
            }  
            } catch (SQLException e) {  
            e.printStackTrace();  
        }  
        try {  
            JDBCUtils.close(connection, statement,resultSet);        
            } catch (SQLException e) {       
                 e.printStackTrace();        
            }
       }
}
-db.properties
driver = com.mysql.jdbc.Driver  
url = jdbc:mysql://localhost:3306/student?useSSL=false  
user = root  
password = tong051114

-JDBCUtils.java
public class JDBCUtils {  
    private static String driver;  
    private static String url;  
    private static String user;  
    private static String password;  
  
    //通过静态代码块预先执行读取配置项，做预处理  
    static {  
        try (InputStream inputStream = ClassLoader.getSystemResourceAsStream("com/company/demo2/db.properties")) {  
            //JDBCUtils.class.getClassLoader();  
  
  
            Properties properties = new Properties();  
            properties.load(inputStream);  
  
            driver = properties.getProperty("driver");  
            url = properties.getProperty("url");  
            user = properties.getProperty("user");  
            password = properties.getProperty("password");  
  
            Class.forName(driver);  
        } catch (Exception e) {  
            e.printStackTrace();  
        }  
    }  
  
    public static Connection getConnection() throws SQLException {  
        return DriverManager.getConnection(url,user,password);  
    }  
  
    public static void close(Connection connection, Statement statement) throws SQLException {  
        if(statement != null){  
            statement.close();  
            statement = null; //也可以不写  
        }  
        if(connection != null){  
            connection.close();  
        }  
    }  
  
    public static void close(Connection connection, Statement statement, ResultSet resultSet) throws SQLException {  
        if(statement != null){  
            statement.close();  
            statement = null; //也可以不写  
        }  
        if(connection != null){  
            connection.close();  
        }  
        if(resultSet != null){  
            resultSet.close();  
        }  
    }  
  
}
```

- 字符编码问题
（sql语句插入中文）：输入`update info set name = '中文' where id = 4`
![[Pasted image 20250126110513.png]]
-如果要显示中文两个字，需要在db.properties文件里的url加上`?characterEncoding=utf8`，即`url = jdbc:mysql://localhost:3306/student?characterEncoding=utf8`，要注意不要有空格否则会无法识别
- 一开始创建数据库时使用的字符集是utf8mb4，假如说我们改成gbk（windows中文系统是gbk），那JDBC的字符编码设置也要改成gbk。

- 要注意看mysql的字符编码设置，有的是latin1，也不行

实现用户输入字符串，使用preparedStatement防注入？？
```java
public class JDBCUDemo01 {  
  
    public static Connection connection;  
    public static PreparedStatement preparedStatement;  
    public static Scanner scanner = new Scanner(System.in);  
  
  
    public static void main(String[] args){  
        try {  
            connection = JDBCUtils.getConnection();  
  
  
            System.out.println("请先输入姓名，然后输入年龄，用回车隔开：");  
  
            String name = scanner.nextLine();  
            int age = scanner.nextInt();  
  
            String sql = "INSERT INTO info(name,age) values(?,?)";  
  
            preparedStatement = connection.prepareStatement(sql);  
            preparedStatement.setString(1,name);//第一个问号是1  
            preparedStatement.setInt(2, age);//第二个问号  
  
            int res = preparedStatement.executeUpdate();  //假如是查询就用executeQuery
  
            if(res > 0){  
                System.out.println("insert success!");  
            }  
  
        } catch (Exception e) {  
            e.printStackTrace();  
        }finally {  
            try {  
                JDBCUtils.close(connection,preparedStatement);  
                scanner.close();  
            } catch (SQLException e) {  
                e.printStackTrace();  
            }  
  
        }  
    }  
  
}
```
使用查询语句也是一样，可以用问号进行赋值。

