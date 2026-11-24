# 第 5 节：我自己整理出的 Java 编程基础

> 当时的情况是这样的，我觉得自己的的 Java 编程基础还不够，我就从头到尾梳理了一遍。
>
> 可以参考下，本身就是这种样子的，更有参考价值。自己梳理的时候定位就更加准确。

## 01|着要点自己查缺补漏

### **目标**

<callout emoji="✍️">
1. **解决实际问题的能力。**
2. **算法和数据结构的灵活运用能力。**
3. **Java 软件开发基础**、**计算机算法**及**数据结构**。

   - **Java 软件开发基础：**包含使用 Java **编写程序的能力**。
</callout>

### 思维策略

<callout emoji="✍️">
**核心（抽象化表述）：道 + 术 => 道术结合 => 天下无敌**
具体说明：
- **道：**`一步步来，遵循规律`。我可以的，我的脑袋是国奖的脑袋。
- **术：**`解决问题的能力，向上提升的关键`——**（学习）复盘 → 思考（理解，吸收） → 输出 （验证）→复盘（闭环）**。
- **比喻说明：**就像人一样，人的运作成长需要：吃进去东西，吃的时候要爵一爵，然后消化吸收，然后拉出来。
</callout>

### 1.1 Java编程基础

#### 1、进制转换

<callout emoji="🙋">
**问：**对于蓝桥杯软件开发规则中提到的软件，是否可以用其中的计算器功能？如果可以，是否可以用程序员模式？
</callout>

#### 2、数据类型

- 整数类型：byte（1）、short（2）、int（4，默认）、long（8）
- 浮点型：float（4）、double（8，默认）
- 字符型：char（2）
- 布尔型：boolean（1）

**类型自动转换，类型强制转换（**目标类型 目标变量名 = (目标类型)待转变量或数值**）。**

**注意：**

- byte、short、char 之间不会转换，这个是规则。
- 在表达式中，**byte**、**short**、**char** 是**直接转换成 int** 类型参与运算的。
- 转换的目标不能超过目标类型的范围。
- 强制转换会导致数据溢出（就是数据突然变大的情况），可以利用，切除小数部分：

  <callout emoji="💫">
  - **正数向下取整**：3.999 → 3
  - **负数也向零取整**：-2.9 → -2，不是 -3
  - 不会四舍五入，不会进位，**纯暴力截断**
  - 但是想要**真正安全、规范地截断小数**，使用 Math.floor/ Math.ceil/ Math.round，而不是强转。
  </callout>

**Math类提供的常见方法**

<sheet sheet-id="Lc46LP" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

**1）向零截断（和强转效果一样，但更规范）**

**要点：**正数向下，负数向上，统一靠近 0

**代码：**

```Java
double num = -3.9;
long res = (long) num;
// 等价于更规范的：
long res2 = (long) Math.floor(num); // 正数才等价
```

**说明：**浮点强转本质就是 **向零取整**，但可读性差，不推荐。

---

**2）真正向下取整（数学意义上的截断，最常用）**

**要点：**无论正负，都往更小的方向取整

**代码：**

```Java
double a = 3.9;
long res1 = (long) Math.floor(a); // 3

double b = -3.1;
long res2 = (long) Math.floor(b); // -4
```

**说明：**

- 3.9 → 3
- -3.1 → -4（数学上更小）蓝桥杯处理 “整除、取整、分段” 几乎都用这个。

---

**3）向上取整（天花板）**

**要点：**往更大的方向取整

**代码：**

```Java
double a = 3.1;
long res1 = (long) Math.ceil(a); // 4

double b = -3.9;
long res2 = (long) Math.ceil(b); // -3
```

---

**4）四舍五入（最常用！）**

**要点：**最符合日常计算，必须会

**代码：**

```Java
double a = 3.5;
long res1 = Math.round(a); // 4

double b = 3.4;
long res2 = Math.round(b); // 3
```

**说明：**

- Math.round () 返回 **long**，不会溢出

---

<callout emoji="💫">
**问题解答：**`Math.random() 与 new Random()` 的核心区别
要点：**Math.random() 是静态方法，内部只用 1 个全局 Random 实例；new Random() 是自己新建独立随机数生成器。本质就是用 Random 实现的。**
</callout>

**代码：**

```Java
// 方式1
double d1 = Math.random();

// 方式2
Random random = new Random();
double d2 = random.nextDouble();
```

**说明：**

1. **Math.random()**

   - 简便，一行生成 `[0,1)` 随机小数
   - 多线程下可能竞争，性能略差
   - 只能生成 double，不能指定种子、不能生成 int/long/boolean（**问题：如何设定种子，什么意思？长什么样？见下方解答**）
2. **new Random()**

   - 可生成 int、long、float、double、boolean
   - 可设置种子（固定种子=固定随机序列）
   - 可多次复用对象，性能更好
   - 蓝桥杯**更推荐用这个**

---

要点：**需要随机整数、控制序列、频繁使用时，必须用 new Random()**

代码：

```Java
Random r = new Random();
// [0,99]
int num = r.nextInt(100);
```

**说明：**Math.random() 转整数要自己计算，容易写错；**Random 直接 nextInt(n) 更安全**。

<callout emoji="💫">
解答：**如何设定种子，什么意思？长什么样？**
</callout>

**要点：**固定种子后，每次运行输出的随机数序列完全相同

**代码：**

```Java
import java.util.Random;

public class TestSeed {
    public static void main(String[] args) {
        // 固定种子为 100
        Random random = new Random(100);

        System.out.println(random.nextInt(100));
        System.out.println(random.nextInt(100));
        System.out.println(random.nextInt(100));
    }
}
```

**说明：**无论运行多少次，输出的三个数字永远不变，这就是固定种子=固定随机序列。

#### 3、运算符

**1）基本运算符（+、-、\*、/、% ）、+字符串做拼接。**

---

**取余运算 % 核心要点**

---

- 取余结果的符号**只与被除数一致**，与除数无关。
- 定义：`a % b` 的结果绝对值一定小于 `|b|`。

  - 案例：`i % 5` 结果永远在 `[-4,4]` 之间，常用于环形下标。
- 除数不能为 0，否则抛出算术异常。

---

**高频使用场景（多案例+详细解释）**

**1）判断奇偶**

代码：

```Java
boolean isEven = 10 % 2 == 0;
```

解释：对 2 取余为 0 是偶数，为 1 是奇数。

**2）循环下标 / 环形数组**

代码：

```Java
for (int i = 0; i < 10; i++) {
    int idx = i % 3;
    System.out.println(idx); // 输出：0 1 2 0 1 2 0 1 2 0
}
```

解释：`i % n` 会让下标在 `0 ~ n-1` 之间循环，实现环形遍历。

**3）取数字最后一位**

代码：

```Java
int num = 5678;
int last = num % 10; // 结果 8
```

解释：对 10 取余得到个位数字。

**4）取最后两位数字**

代码：

```Java
int num = 5678;
int lastTwo = num % 100; // 结果 78
```

解释：对 100 取余得到最后两位。

**5）判断是否能整除**

代码：

```Java
boolean divisible = 100 % 5 == 0; // true
```

解释：余数为 0 表示可以整除。

**6）限制数值范围**

代码：

```Java
int score = 105;
int real = score % 100; // 5
```

解释：把任意数字限制在 `0~99` 范围内。

**7）周期性切换状态**

代码：

```Java
for (int i = 0; i < 6; i++) {
    String color = i % 2 == 0 ? "red" : "blue";
}
```

解释：奇偶交替，实现隔行变色、开关切换。

---

**循环下标 / 环形数组具体应用场景**

---

**1. 循环报数（约瑟夫环简化版）**

要点：利用 `i%3` 循环 0、1、2 模拟 1、2、3 报数

代码：

```Java
public class Main {
    public static void main(String[] args) {
        // 模拟10个人循环报数，报到3的淘汰
        for (int i = 1; i <= 10; i++) {
            // 0、1、2 循环，对应报数1、2、3
            int call = i % 3;
            if (call == 0) {
                System.out.println(i + "号被淘汰");
            }
        }
    }
}
```

说明：蓝桥杯常考围成一圈报数淘汰，核心就是取余循环。

---

**2. 计算星期（日期周期题）**

要点：利用 `天数%7` 循环星期，固定周期必考

代码：

```Java
public class Main {
    public static void main(String[] args) {
        // 假设今天星期一(1)，求100天后星期几
        int today = 1;
        int later = 100;
        // 计算最终星期
        int week = (today + later) % 7;
        // 修正0为周日
        week = week == 0 ? 7 : week;
        System.out.println("100天后是星期" + week);
    }
}
```

说明：日期、周期类填空题，都会用到取余循环。

---

**3. 环形数组遍历（轮流赋值）**

要点：数组下标循环使用，高频模拟题考法

代码：

```Java
public class Main {
    public static void main(String[] args) {
        int[] arr = new int[5];
        // 给数组循环赋值 1、2、3
        for (int i = 0; i < 10; i++) {
            // 循环生成 0、1、2 下标
            int idx = i % 3;
            arr[idx]++;
        }
    }
}
```

说明：题目出现轮流、循环分配、环形遍历，直接用 `i%长度`。

---

**4. 周期数列求第N项**

要点：重复数列直接取余求对应位置

代码：

```Java
public class Main {
    public static void main(String[] args) {
        // 数列规律：0、1、2、0、1、2... 求第1000项
        int n = 1000;
        // 周期3，直接取余
        int res = (n - 1) % 3;
        System.out.println("第1000项是：" + res);
    }
}
```

说明：纯规律填空题，直接一行取余出答案。

---

**+ 号特殊使用**

---

**1）字符串 + 任意类型 → 字符串拼接**

代码：

```Java
String a = "Hello" + "Java";
String b = "年龄：" + 20;
String c = 10 + 20 + "岁";
String d = "成绩：" + 90.5;
```

说明：任意类型与字符串用 `+` 连接，结果都是字符串，运算从左到右执行。

**2）char 参与 + 运算 → 自动转为 int（ASCII 码相加）**

代码：

```Java
int num = 'a' + 1;
char ch = (char) ('a' + 3);
int sum = '1' + '2';
```

说明：`char` 在加法中会先转成对应 ASCII 数值再计算，而非字符拼接。

---

**/ 和 % 的使用**

---

**案例：**

> 将123的个位、十位、百位，拆下来打印输出。
>
> 公式总结：
>
> - 个位：数值 % 10
> - 十位：数值 / 10 % 10
> - 百位：数值 / 10 / 10 % 10
> - 千位：数值 / 10 / 10 /10 % 10
> - ……

**规律：**

第 n 位（从 0 开始）：先除以 10ⁿ，再对 10 取余

或者说：连续除 n 次 10，然后 % 10

**灵活变换：**

1、提取多位数

```Java
// 提取最后两位（十位数和个位数）
int lastTwo = 1234 % 100;        // = 34
// 提取最后三位
int lastThree = 1234 % 1000;     // = 234
```

2、去掉后面几位

```Java
// 去掉最后两位（得到 12，即百位及以上）
int removeLastTwo = 1234 / 100;  // = 12

// 去掉最后三位
int removeLastThree = 1234 / 1000;  // = 1
```

3、去掉中间的某一位

```Java
// 提取百位（第2位，从0开始）
// 方法：先去掉后面的，再取个位
int hundred = (1234 / 100) % 10;   // 1234/100=12, 12%10=2 ✓

// 通用公式：提取第 k 位（从右往左，0开始）
// digit = (n / (int)Math.pow(10, k)) % 10;
```

4、循环提取某一位（常用！）

```Java
int n = 1234;
while (n > 0) {
    int digit = n % 10;    // 取当前个位
    System.out.println(digit);  // 输出: 4, 3, 2, 1
    n = n / 10;            // 去掉个位，继续
}
```

**问题解决：**取最高位 = 数字 ÷ 10 的 **（这个数字的位数 − 1）** 次方。

**2）自增自减运算符**

---

**自增自减运算符 `++` / `--`**

---

**场景1：for 循环遍历数组 / 字符串（必考）**

要点：循环中逐个访问元素，`i++` 移动下标

代码：

```Java
String s = "abcde";
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    // 处理字符：统计、判断、转换等
}
```

蓝桥杯用途：

- 字符串遍历
- 数组查找最大/最小值
- 统计数字出现次数
- 前缀和、差分遍历

---

**场景2：统计满足条件的个数（计数题）**

要点：满足条件就 `cnt++`，用来计数

代码：

```Java
int cnt = 0;
for (int i = 1; i <= 100; i++) {
    if (i % 2 == 0) {
        cnt++; // 统计1~100偶数个数
    }
}
```

蓝桥杯用途：

- 统计质数个数
- 统计满足某条件的数字个数
- 统计合法字符串数量
- 填空题、结果计算高频用法

---

**场景3：数组下标步进（模拟题专用）**

要点：一边用下标，一边往后走，`idx++`

代码：

```Java
int[] a = {10, 20, 30, 40};
int idx = 0;
int sum = 0;

// 取一个加一个，直到取完
while (idx < a.length) {
    sum += a[idx++];
}
```

蓝桥杯用途：

- 排队、出队、入队模拟
- 约瑟夫环
- 双指针
- 滑动窗口
- 栈/队列操作

---

**场景4：重置/回退下标（`--` 真正高频用法）**

要点：发现不满足条件，**回退一步**，`idx--`

代码：

```Java
int idx = 5;
// 不符合条件，退回到上一个位置
if (!check(a[idx])) {
    idx--;
}
```

蓝桥杯用途：

- 回溯
- 回文判断
- 括号匹配
- 模拟“撤销一步”
- 双指针从两端往中间走

---

**场景5：标记访问过的位置（`vis[i]++`）**

要点：用数组计数，记录出现次数

代码：

```Java
int[] cnt = new int[10];
for (int i = 0; i < s.length(); i++) {
    int num = s.charAt(i) - '0';
    cnt[num]++; // 统计每个数字出现几次
}
```

蓝桥杯用途：

- 数字统计
- 重复数字判断
- 频率统计
- 全排列、组合问题

---

**场景6：while 循环步进（代替 for）**

要点：不知道循环多少次时用 `i++`

代码：

```Java
int x = 100;
int step = 0;
while (x > 0) {
    x /= 2;
    step++;
}
```

蓝桥杯用途：

- 分解数字
- 求位数
- 模拟过程题
- 二分、倍增问题

---

**3）扩展赋值运算符**

**基本赋值运算符**

就是“=”号，从右边往左边看。

如：

```Java
int a = 10; // 先看“=”号右边，先将数据10赋值给变量a存储。
```

---

**扩展赋值运算符**

<sheet sheet-id="cEfy6h" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

**注意：**扩展的赋值运算符隐含了强制类型转换。**（注意格式）**

---

**4）关系运算符**

**5）逻辑运算符**

**逻辑运算符一览表**

把多个条件放在一起算，最后返回布尔类型的值：true、false。

<sheet sheet-id="JfsWJZ" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

`注意：`在java中，“&”，“|” 无论左边是false还是true，右边都要执行。

---

**短路与 短路或一览表**

<sheet sheet-id="hY6uQL" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

`注意：`相比单&和单|来说，性能更好，实际开发中效率更高。

---

**亦或运算**

---

**核心性质（必须记）**

1. 0 ^ x = x
2. x ^ x = 0
3. a ^ b ^ c = a ^ (b ^ c)
4. 自反性：a ^ b ^ b = a

---

**1. 交换两个变量（不用临时变量）**

要点：利用 `a^a=0` 实现交换

题目：看到 “交换两个 int 变量，不准用第三个临时变量”。

代码：

```Java
int a = 3;
int b = 5;
a = a ^ b;
b = a ^ b;
a = a ^ b;
```

蓝桥杯场景：省空间、代码简洁题。

---

**2. 找“只出现一次”的数字（高频真题）**

要点：相同数抵消为0，最后剩下唯一数

题目：数组中只有一个数出现1次，其他都出现2次，找它。

代码：

```Java
int[] arr = {1,2,3,2,1};
int res = 0;
for(int num : arr){
    res ^= num;
}
// res = 3
```

蓝桥杯必考：**找不同数、找丢失数**。

---

**3. 判断两个数符号是否相反**

要点：异或后最高位为1（负数）则符号不同

代码：

```Java
boolean isOpposite = (a ^ b) < 0;
```

场景：快速判断正负，避免分支。

---

**4. 翻转指定位（二进制操作）**

要点：和1异或取反，和0异或不变

代码：

```Java
// 翻转第3位
x = x ^ (1 << 3);
```

场景：二进制状态题、开关题。

---

5. 简单加密解密

要点：异或两次还原

```Java
int code = num ^ key;   // 加密
int origin = code ^ key;// 解密
```

---

**6）三元运算符**

**介绍**

> `格式：`条件表达式  ? 值1 : 值2;
>
> `执行流程：`首先计算关系表达式的值，如果值为true，返回值1；如果为false，返回值2。

#### 4、输出语句

---

**Java 中 println 和 printf 的区别**

---

**1. 基本功能**

- **println**：打印内容并**自动换行**，无格式控制。
- **printf**：格式化输出，可精确控制小数位数、对齐、进制等。

**2. 语法格式**

```Java
// 打印并换行
System.out.println(内容);

// 格式化打印："格式串", 参数...
System.out.printf(格式字符串, 参数1, 参数2...);
```

**3. 格式控制能力**

- **println**：只能直接输出，无法控制格式。
- **printf**：通过格式符控制整数、浮点数、字符串等输出样式。

**4. 常用格式符与示例（必背）**

```Java
System.out.printf("整数：%d%n", 100);           // 十进制整数
System.out.printf("小数保留2位：%.2f%n", 3.14159); // 浮点数
System.out.printf("字符串：%s%n", "Hello");     // 字符串
System.out.printf("字符：%c%n", 'A');           // 字符
System.out.printf("十六进制：%x%n", 255);       // 转16进制
```

**5. 换行处理**

- **println**：自动换行，无需加 `\n`。
- **printf**：不自动换行，必须手动加 `%n` 或 `\n`。

**6. 返回值与链式调用**

- **println**：返回 `void`，不能链式调用。
- **printf**：返回 `PrintStream`，支持连续调用：

```Java
System.out.printf("年龄：%d%n",25).printf("姓名：%s%n","张三");
```

**7. 蓝桥杯使用场景与案例**

**场景1：普通输出答案 / 调试**

直接打印结果，用 `println` 最简单。

```Java
int ans = 123;
System.out.println(ans);
```

**场景2：题目要求保留 2 位小数（高频）**

求平均值、面积、概率时必须用 `printf`。

```Java
double avg = 78.5678;
System.out.printf("%.2f%n", avg);   // 输出 78.57
```

**场景3：一行输出多个数字、固定格式**

多结果按空格/格式输出，用 `printf` 更整洁。

```Java
int a = 1, b = 2, c = 3;
System.out.printf("%d %d %d%n", a, b, c);
```

#### 5、流程控制语句

**1）顺序结构**

**2）分支结构**

**if 和 switch：**

**if** 有三个分支，分别是单分支、双分支、多分支。

**场景**：条件判断、奇偶、范围筛选、合法判断

```Java
int score = 85;
if (score >= 60) {
    System.out.println("及格");
} else {
    System.out.println("不及格");
}
```

**switch：**

**场景**：固定值匹配（星期、菜单、状态）

```Java
int week = 3;
switch (week) {
    case 1: System.out.println("周一"); break;
    case 2: System.out.println("周二"); break;
    default: System.out.println("其他");
}
```

---

```Java
switch(表达式){
    case 值1:
        执行代码块1;
        break;
    case 值2:
        执行代码块2;
        break;
    ……
    case 值n-1:
        执行代码块n-1;
        break;
    default:
        执行代码块n;
}
```

 ***if、switch的比较，以及各自适合什么业务场景？***

1. 从功能上看if远远强于switch。*为什么？*switch只能做值判断。
2. 当前条件为区间的时候，应该选择使用if分支结构会更好些。
3. 当前条件是与一个个的值进行比较的时候，switch分支更合适，它格式良好，性能较好（因为在做值匹配的时候，if分支是从一个个分支的去判断（**顺序判断**），但是switch不是一个一个的去找（**跳转表**），它可以快速定位到相应的值上去），代码优雅。

***switch使用的几点注意事项***

1. 表达式类型只能是byte、short、int、char，JDK5开始支持枚举，JDK7开始支持String、不支持double、float、（小数不精确，很可能找不到）long（跳转表太大）。
2. case给出的值不允许重复，且只能是字面量，不能是变量。
3. 正常使用switch的时候，不要忘记写break，否则会出现**穿透现象**。

**3）循环结构**

包含for、while、do …… while。

格式

```Java
for(初始化语句; 循环条件; 迭代语句){
    循环体语句(重复执行的代码);
}
```

```Java
初始化语句;
while(循环条件){
    循环体语句(被重复执行的代码);
    迭代语句;
}
// 在控制台输出三次HelloWorld
int i = 0;
while(i < 3){
    System.out.println("HelloWorld");
    i++;
}
```

**1. for 循环（固定次数）**

**场景**：遍历数组/字符串、统计、枚举

```Java
int sum = 0;
for (int i = 1; i <= 100; i++) {
    sum += i;
}
```

**2. while 循环（先判断再执行）**

**场景**：未知次数、条件满足就继续

```Java
int x = 1;
while (x <= 10) {
    System.out.println(x);
    x++;
}
```

**3. do-while 循环（至少执行一次）**

**场景**：菜单选择、输入校验、必须先做一次

```Java
int n;
do {
    n = new Scanner(System.in).nextInt();
} while (n < 0);
```

---

***while循环和for循环有什么区别？什么时候用for？什么时候用while？***

> while和for只是格式不一样，但是执行流程是一样的。
>
> - **功能上是完全一样的，for循环能解决的，while循环也能解决，反之亦然。**
> - **使用规范：知道循环几次：使用for；不知道循环几次：使用while。**

**while循环案例：纸张折叠成珠穆朗玛峰的高度(为什么要做案例啊？)**

```Java
初始化语句;
do{
    循环体语句;
    迭代语句;
} while (循环条件);
// 输出三个HelloWorld
int i = 0;
do{
    System.out.println("HelloWorld");
    i++;
} while (i < 3);
```

**死循环**

```Java
// for循环
for( ; ; ){
    System.out.println("Hello World1!");
}
// while循环，经典写法
// 这里会报错原因是，上面的一个循环是死循环，根本执行不到下面的这个循环
// 所以报错
while(true){
    System.out.println("Hello World2!");
}
//do……while循环
do{
    System.out.println("Hello World3!");
} while (true);
```

**循环的嵌套**

```Java
// 双层for循环嵌套
for(int i = 0; i < 3; i++){
    for(int j = 0; j < 5; j++){
        System.out.println("我爱你");
        }
}
```

---

<callout emoji="💫">
**跳转关键字：break，continue**
- break：跳出并结束当前所在循环的执行。
- continue：用于跳出当前循环的当次执行，直接进入循环的下一次执行。
**`注意事项：`**
- break：只能用于结束所在循环，或者结束所在switch分支的执行。
- continue：只能在循环中使用。
- 这里指的循环是for循环、while循环、do……while循环，不只是for循环。
**`使用场景：`**break比如用在找东西的循环当中，如果找到目标了，也就不要再执行后面的代码或者循环次数了，这个时候就可以使用break关键字跳出循环。具体看练习中。
</callout>

**1. break**

**场景**：跳出循环、结束 switch、找到答案提前退出

```Java
for (int i = 1; i <= 100; i++) {
    if (i == 5) break;
}
```

**2. continue**

**场景**：跳过当前次，直接进入下一轮循环

```Java
for (int i = 1; i <= 10; i++) {
    if (i % 2 == 0) continue;
    System.out.println(i); // 只打印奇数
}
```

---

**随机数Random类**

**场景**：生成随机数、模拟题目、测试数据

```Java
Random r = new Random();
int num = r.nextInt(100);      // [0,99]
int a = r.nextInt(50) + 1;    // [1,50]
boolean b = r.nextBoolean();
```

**案例：拆数字游戏 RandomTest3.java**

这个案例的目的是把以上的知识结合起来，提升编程思维。

随机生成一个1-100之间的数据，提示用户猜测，猜大提示过大，猜小提示过小，直到猜中结束游戏。

**解惑**

程序员写代码习惯从又往左写的原因，程序执行的顺序。

`提示：`

- 如果无从下手，没关系，编程思维的养成它需要一个过程，没有技巧。
- 但是很重要的两点是：第一要有用户思维（用户怎么想我们就怎么写代码），第二是先性思维（就是顺腾摸瓜一条线写下来）。

**分析**

> 1. 先随机生成一个1-00之间的随机数。
> 2. 定义一个死循环让用户可以一直猜。
> 3. 在死循环里，每次都提示用户输入一个猜测的数字，猜大提示过大，猜小提示过小，猜中则结束游戏。

```Java
package com.sundae.random;

import java.util.Random;
import java.util.Scanner;

public class RandomTest3 {
    public static void main(String[] args) {
        // 目标：熟悉第三天所学的分支、循环，跳转语句所有知识，并将它们融汇贯通

        // 3. 创建一个扫描器对象，接收用户输入的内容
        Scanner sc = new Scanner(System.in);

        // 1. 先生成一个1-100内的随机数
        Random r = new Random();
        int luckyNumber = r.nextInt(100) + 1;

        // 2. 使用一个死循环，能让用户一直输入（因为不知道用户第几次猜中，所以使用while循环）
        while(true){
            // 4. 提醒用户输入
            System.out.println("你猜的数字是什么？");
            // 5. 真正接收用户输入的地方
            int guessNumber = sc.nextInt();
            // 6. 提示用户猜测，猜大提示过大，猜小提示过小，直到猜中结束游戏。
            if(guessNumber > luckyNumber){
                System.out.println("猜大了！");
            } else if(guessNumber < luckyNumber){
                System.out.println("猜小了！");
            }  else if(guessNumber == luckyNumber){
                System.out.println("猜中了，你去买单吧！");
                break;
            } else {
                System.out.println("你的输入的数字不合规矩");
            }
        }
    }
}
```

---

**蓝桥杯一句话用法**

- 固定次数遍历 → **for**
- 未知次数 → **while**
- 必须执行一次 → **do-while**
- 条件判断 → **if**
- 固定值匹配 → **switch**
- 提前结束 → **break**
- 跳过本轮 → **continue**
- 生成随机数 → **Random**

#### 6、数组

**为何用数组？**

**数组（直接用变量存太笨太老了） + Random + switch → 随机点名。**

**1）静态初始化数组**

格式：

```C++
// 完整格式
数据类型[] 数组名 = new 数据类型[]{元素1, 元素2, 元素3, ……}; // 元素就是数据，数据就是元素
int[] ages = new int[]{13, 23, 24};
double[] scores = new double[]{70.3, 80.4, 93.7, 68.8};

// 简化格式
数据类型[] 数组名 = {元素1, 元素2, 元素3, ……};
int[] ages = {13, 23, 24};
double[] scores = {70.3, 80.4, 93.7, 68.8};
```

<callout emoji="💫">
**`技术进阶小提示`：**即使很简单，即使你都会，我们也要继续去弄，达到刻在脑子里的程度。**因为我们的技术讲的不是知道，而是讲你孰不熟练。** 另外，我们程序员要`学会`以及`习惯`看错误。
**发问：**智能体开发也是讲熟练度，二者是不是一样的？（等着我去尝试）
</callout>

数组访问、数组长度（length）、数组遍历

**2）动态初始化数组**

**(1) 数组的动态初始化**

定义数组时先不存入具体的数值，`只确定数组存储的数据类型和数组的长度。`

**(2) 数组的动态初始化格式**

```Go
// 先初始化
数据类型[] 数组名 = new 数据类型[数组长度];
int[] arr = new int[3];

// 后赋值
arr[0] = 10;
System.out.println(arr[0]);

// 注意：
int[] arr = new int[3]{34, 36, 39}; // 错误的，不能又声明数据，又声明长度，画蛇添足，会报错啊
```

```Go
        // 目标：数组元素求最大值
        // 需求；题目给出了6位美女的颜值的分，请现在根据这些得分求出
        // 颜值最高的美女
        // 1. 先创建一个数组，将这六个颜值得分数据存到容器中去，使用数组
        int[] faceScores = {15, 9000, 10000, 20000, 9500, -5};

        // 3. 在循环外定义一个int类型变量存储初始颜值最高的一位美女
        // 建议初始化第一位美女的颜值最高,然后遍历数组的时候从第二位遍历，也就是从第二位开始比较
        int maxScore = faceScores[0];

        // 2. 遍历数组
        for (int i = 1; i < faceScores.length; i++) {
            // 4. 使用if分支将每位美女的分和上一次的最高分进行对比判断
            int  faceScore = faceScores[i]; // 牛逼地方
            if(faceScore > maxScore) {
                // 5. 如果前默认乱序排序中的后一位比前一位的分数高，就将后一位的列为maxScore
                maxScore = faceScore;
            }
        }

        // 6.输出最高得分及颜值最高的美女
        System.out.println("全场最亮的女得分为：" + maxScore);
```

<callout emoji="💫">
**牛逼思维**
**思维名字叫：**
「**先取**当前元素到临时变量，**再**进行**比较判断**」
**专业叫法：**
**单次取值，复用变量**（高效、清晰、安全）
</callout>

---

**案例：数组反转 Test2.java**

`目标：` 需要掌握数组元素交换的方法。

**需求**

某个数组有5个数据：10, 20, 30, 40,50，请将这个数组中的数据进行反转。

`[10, 20, 30, 40,50]` 反转后 `[50, 40, 30, 20, 10]`

**分析**

> 数组交换操作实际上就是：依次前后交换数据即可实现。

**实现**

```Java
        // 我们使用原地反转的方法
        // 1. 先创建一个数组将这5个数据存到程序中去
        int[] arr = {10, 20, 30, 40,50};

        // 2. 遍历数组，进行反转
        // 这里使用双向交换，相当于一个两个指针控制数据进行交换来实现反转
        for (int i = 0, j = arr.length-1; i < j; i++, j--) {
            // 3. 原地交换数组元素
            // 交换思想：就是定义一个临时变量来存储前一个位置 i 的值，
            // 等到后一个位置 j 的值赋值给前一个位置 i 后，再用临时变量记住的
            // 后一个位置 j 的值赋值给前一个位置 i
            int temp = arr[i]; // 临时变量temp
            arr[i] = arr[j];
            arr[j] = temp;
        }

        // 4. 遍历交换后的数组元素并输出
        for (int i = 0; i < arr.length; i++) {
            System.out
```

**案例：随机排名 Test3.java**

**需求**

某公司开发部5名开发人员，要进行项目进展回报演讲，现在采取随机排名后进行汇报。请先依次录入名员工的工号，然后展示出一组随机的排名顺序。

**分析**

> 只要看到批量数据，我们就要想到容器，但是当前我们学的容器就只有数组，所以就用数组来解决。
>
> 1. 在程序中录入5名员工的工号存储起来 ----> 使用动态初始化数组的方式。
> 2. 依次遍历数组中的每个数据。
> 3. 每遍历一个数据，都用一个随机索引与其进行交换。

**下午练习**

```Go
        // 目标：掌握随机排名案例
        // 需求：某公司开发部5名开发人员，要进行项目进展回报演讲，
        // 现在采取随机排名后进行汇报。请先依次录入名员工的工号，
        // 然后展示出一组随机的排名顺序。

        // 1. 先创建一个动态数组，数组大小为5
        int[] employeeIDs = new int[5];

        // 3. 创建一个Scanner对象接收录入的员工工号
        Scanner sc = new Scanner(System.in);

        // 5.我采用随机索引对应的值与每次访问到的数组索引对应的值进行交换
        // 利用随机索引，结合数组反转思想正好能做到打乱数组实现随机数组排序的目的

        // 6. 创建一个产生随机数的对象
        Random r = new Random();

        // 2. 遍历数组
        for (int i = 0; i < employeeIDs.length; i++) {
            // 4. 接收每次录入的员工工号并将其存储到数组中去
            System.out.println("请录入第" + (i + 1) + "位员工的工号：");
            employeeIDs[i] = sc.nextInt();
        }

        // 7.再次遍历数组，进行打乱数组顺序功能
        for (int i = 0; i < employeeIDs.length; i++) {
            // 8. 并调用方法实现产生随机数以及产生随机数的范围（每次都要变一次随机数数）
            int lukyNum = r.nextInt(5) + 1;
            // 9. 使用交换思想，将顺序访问的数据和随机数字（索引）对应的数据进行交换
            int temp = employeeIDs[i]; // 临时变量temp
            employeeIDs[i] = employeeIDs[lukyNum];
            employeeIDs[lukyNum] = temp;
        }

        // 10. 遍历随机排序后的数组并输出
        for (int i = 0; i < employeeIDs.length; i++) {
            System.out.print("最终进行汇报的顺序为：" + employeeIDs[i] + " "); // 使用空格隔开
        }
```

---

**应用小结**

---

**场景 → 完整可运行代码 → 注释标注 → 什么时候用**

1. **数组遍历（最基础模板）**

**场景**：看一遍所有数据、打印、检查

```Java
public class Main {
    public static void main(String[] args) {
        int[] arr = {10, 20, 30, 40, 50};

        // 模板：标准数组遍历
        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
    }
}
```

**什么时候用**：几乎所有数组题第一步。

---

1. **求最大值（竞赛必考模板）**

**场景**：最高分、最大数、最优解

```Java
public class Main {
    public static void main(String[] args) {
        int[] arr = {15, 8, 23, 9, 100};

        // 模板：求最大值
        int max = arr[0];        // 初始化最大值
        for (int i = 1; i < arr.length; i++) {
            int num = arr[i];    // 先存变量，规范写法
            if (num > max) {
                max = num;
            }
        }
        System.out.println("最大值：" + max);
    }
}
```

---

1. **求数组总和 & 平均值**

**场景**：总分、平均分、总和类题目

```Java
public class Main {
    public static void main(String[] args) {
        int[] arr = {90, 85, 95, 80};

        // 模板：求和
        int sum = 0;
        for (int num : arr) {
            sum += num;
        }
        double avg = sum * 1.0 / arr.length;

        System.out.println("总和：" + sum);
        System.out.printf("平均值：%.2f", avg);
    }
}
```

---

1. **统计数字出现次数（计数数组）**

**场景**：统计多少个男生、多少个A、数字频率

```Java
public class Main {
    public static void main(String[] args) {
        int[] scores = {1, 2, 1, 3, 2, 2, 1};

        // 模板：计数数组
        int[] cnt = new int[4];   // 分数范围 0~3
        for (int num : scores) {
            cnt[num]++;
        }

        System.out.println("1出现次数：" + cnt[1]);
        System.out.println("2出现次数：" + cnt[2]);
    }
}
```

**蓝桥杯高频：统计、查重、找众数**。

---

1. **标记是否访问过（布尔数组）**

**场景**：去重、判断是否用过、回溯、搜索

```Java
public class Main {
    public static void main(String[] args) {
        boolean[] used = new boolean[10];

        used[3] = true;   // 标记3用过
        used[5] = true;   // 标记5用过

        if (!used[2]) {
            System.out.println("2 没用过");
        }
    }
}
```

---

1. **数组翻转 / 回文判断**

**场景**：字符串回文、数字回文、数组翻转

```Java
public class Main {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};

        // 模板：翻转数组
        for (int i = 0; i < arr.length / 2; i++) {
            int j = arr.length - 1 - i;
            // 交换
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
}
```

---

1. **前缀和（快速求区间和**）

**场景**：求第2到第5个数的和、多次区间查询

```Java
public class Main {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        int n = arr.length;

        // 模板：前缀和数组
        int[] pre = new int[n];
        pre[0] = arr[0];
        for (int i = 1; i < n; i++) {
            pre[i] = pre[i - 1] + arr[i];
        }

        // 求 1~3 下标的和
        int sum = pre[3] - pre[0];
    }
}
```

---

1. **排序后处理（蓝桥杯万能神器）**

**场景**：找中位数、去重、最大最小、贪心题目

```Java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] arr = {3, 1, 4, 2, 5};

        // 模板：排序
        Arrays.sort(arr);

        System.out.println("最小值：" + arr[0]);
        System.out.println("最大值：" + arr[arr.length - 1]);
    }
}
```

---

<callout emoji="💫">
**怎么判断什么时候用数组？**
- 要存**多个同类型数据** → 数组
- 要**统计次数** → 计数数组
- 要**最大/最小/总和** → 遍历数组
- 要**快速算区间和** → 前缀和数组
- 要**查重/标记** → 布尔数组
- 要**方便找大小** → 排序数组
</callout>

#### 7、方法

1. ***方法是什么？***

方法是一种用于执行特定任务或操作的代码块，**就是一个功能**，它可以接收数据进行处理，并返回处理后的结果。

**`注意：`** 特定任务或操作是被封装在里面的。

1. **方法的完整定义格式**

```Java
修饰符 返回值类型 方法名(形参列表){
    方法体代码(需要执行的功能代码)
    return 返回值;
}
```

1. **方法如何使用**

方法必须被调用才能执行，`调用格式：方法名称(数据)`。

<callout emoji="💫">
#### 提一嘴，脱颖而出的秘密——熟练
你一定要很熟练，不然等以后到了就业班级或者找工作的时候，**大家学的知识一样，但是有的人能把这个需求做出来，有的做不出来。Ta做出来了，你知道了，去企业的差别就在这儿，你也知道用什么做，但是你就是做不出来，然后你面试你也知道是什么意思，但是你说不出来。**你想想，你面试的时候，假如人家问你，方法是什么？。 。 。 不知道，你面试能成功吗？你就平时学的再牛B也不行知道吧？所以，你们平时听课一定要记脑袋里。即使是听了很多遍，知道了，但是如果别人一问，这个是什么？你就：嗯——嗯——嗯，就是0，听多少遍都是0。
**给自己下个决定：**一定要有强烈的目标，告诉自己我就要脱颖而出，我就是要比别人优秀，我就是要把它做出来，所以我是要不断地提升我的编程能力，技术水平，持续、认真、踏实、大量地去做。
</callout>

---

**方法注意事项：**

```TypeScript
        public static void main(String[] args) {
        // 目标：掌握方法定义时的注意事项
        // 1. 方法在类中的位置放前放后无所谓，但一个方法不能定义在另一个方法里面。
        // 2. 方法的返回值类型写void（无返回申明）时，方法内不能使用return返回数据，
        // 如果方法的返回值类型写了具体类型，方法内部则必须使用return返回对应类型的数据。
        // 3. return语句的下面，不能编写代码，属于无效的代码，执行不到这儿。
        // 4. 方法不调用就不会执行，调用方法时，传给方法的数据，必须严格匹配方法的参数情况。
        // 5. 调用有返回值的方法，有3种方式：1、可以定义变量接收结果2、或者直接输出调用，3、甚至直接调用；
        // 6. 调用无返回值的方法，只有1种方式：1、只能直接调用。
    }
    // 1. 方法在类中的位置放前放后无所谓，但一个方法不能定义在另一个方法里面。
    // 比如f1方法和f2方法就是同一级别，谁在后谁在前都可以
    public static void f1(){
        // 错误
//        public static void f3(){
//        }
    }
    public static void f2(){

    }

    // 2. 方法的返回值类型写void（无返回申明）时，方法内不能使用return返回数据，
    public static void f4(){
        int a = 20;
        // return n ; // 会报错，
    }
    // 如果方法的返回值类型写了具体类型，方法内部则必须使用return返回对应类型的数据。
    public static int f5(){
        int a = 20;
        return a;
    }

    // 3. return语句的下面，不能编写代码，属于无效的代码，执行不到这儿。
    public static int f6(){
        int a = 20;
        return a;
        //System.out.println(a); // 错误
    }

    // 5. 调用有返回值的方法，有3种方式：
    // 1、可以定义变量接收结果2、或者直接输出调用，3、甚至直接调用；
    // 1、可以定义变量接收结果
    // 就是它会有一个返回值，然后你要定义一个变量来接收它的返回值，然后输出这个变量，否则看不到结果
    // 2、或者直接输出调用
    // 就是直接在main方法中这样写：System.out.println(f6();
    // 3、甚至直接调用；
    // 就是直接在main方法里面这样写：f6();
```

---

<callout emoji="💫">
**设计方法的技巧：主要关注三方面**
1. ***方法是否需要接收数据进行处理？***
2. ***方法是否需要返回数据？***
3. **方法要处理的业务（编程能力）**
**案例-计算1-n的和**
**`需求：`** 计算1-n的和
**`分析:`**
> 1. 是否需要接收数据进行处理？`需要，需要接收数据n，因此设计形参为int类型，参数名为n，即：int n。`
> 2. 是否需要返回数据？`可要可不要。/需要放回1-n的计算结果，因此声明返回值类型为int。`
</callout>

---

**方法的重载：**

1. ***什么是方法的重载？***

**一个类中**，出现**多个方法的名称相同**，但是它们的**形参列表是不同的**，那么这些方法就被称为**方法重载**了。

1. **方法重载的注意事项**

   1. **一个类中，只要一些方法的名称相同、形参列表不同**，那么它们就是方法重载了，其它的都不管（如：修饰符，返回值类型是否一样都无所谓）。
   2. 形参列表不同指的是：形参的**个数**、**类型**、**顺序**不同，不关心形参的名称。

```TypeScript
    public static void main(String[] args) {
        // 认识什么是方法的重载，以及方法重载的作用
        test();
        test(2);
        test(2, 4);

    }
    public static void test(){
        System.out.println("我一只小猫都没有");
    }
    public static void test(int n){
        System.out.println("我有" + n + "只小猫");
    }
    public static void test(int n, int m){
        System.out.println("我不仅有" + n + "只小猫，我还有" + m +"只小狗");
    }
```

---

<callout emoji="💫">
###  方法重载的应用场景
开发中我们经常**需要为处理一类业务，提供多种解决方案**，**此时采用方法重载来设计是很专业的**。而且，作为程序员就只需要记一个API，就完了，**对程序员也友好**。
</callout>

---

<callout emoji="💫">
**return 关键字**
**return关键字在方法中的单独使用**
- **`return：`** 可以用在无返回值的方法中，作用是**立即跳出并结束当前方法的执行**。
- **作卫语句来拦截**。
</callout>

```Java
    public static void main(String[] args) {
        // 目标：掌握return关键字的使用
        System.out.println("开始。。。");
        divided(20, 0);
        System.out.println("结束。。。");
    }
    public static void divided(int a, int b){
        if(b == 0){
            System.out.println("您的除数不能为0~！");
            return; // 跳出并结束当前方法的执行（阿里巴巴开发指南！）
        }
        int c = a / b;
        System.out.println(c);
    }
```

---

#### 8、API

**String、ArrayList。**

##### **1）String**

<callout emoji="💫">
**如何学习？**
**我们要先学习：**
1. **如何创建对象**
2. **如何封装字符串数据**
3. **如何调用 String 的方法**
**以后任何一个程序出来都是这三件事。**
</callout>

1. **String创建对象封装字符串数据的方式**

**方式一：**Java程序中所有的字符串文字（例如“abc”）为此类的对象。（更为推荐）

```Java
String name = "小黑";
String schoolName = "黑马程序员";
```

**方式二：**调用String类的构造器初始化字符串对象。

<sheet sheet-id="KQuYjc" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

**练习**

```Java
package com.sundae.string;

public class StringDemo1 {
    public static void main(String[] args) {
        // 目标：掌握创建字符串对象，封装字符串数据的方法
        // 方式一：Java程序中所有的字符串文字（例如“abc”）为此类的对象。（更推荐）
        String name = "小黑";
        String schoolName = "黑马程序员";

        // 方式二：调用String类的构造器初始化字符串对象。
        // 1、创建一个空白字符串对象
        String s1 = new String(); // 等同于 s1 = "";
        System.out.println(s1);  // 啥也没有

        // 2、根据传入的字符串内容，来创建字符串对象
        String s2 = new String("西门吹雪"); // 等同于 s2 = "西门吹雪";
        System.out.println(s2); // 西门吹雪

        // 3、根据字符数组的内容，来创建字符串对象（以后可能会用到）
        char[] chars = {'a', 'b', 'c', '中', '国'};
        String s3 = new String(chars);
        System.out.println(s3); // abc中国

        // 4、根据字节数组的内容，来创建字符串对象
        byte[] bytes = {97, 98, 99, 65,66,67};
        String s4 = new String(bytes);
        System.out.println(s4); // abcABC 【解码】
    }
}
```

---

1. **String 的常用方法**

<sheet sheet-id="fz4G8J" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

**练习**

```Java
package com.sundae.string;

public class StringDemo2 {
    public static void main(String[] args) {
        // 目标：快速熟悉String提供的处理字符串的常用方法
        String name = "ab黑马666";

        // 1、获取字符串的长度（字符的个数）
        System.out.println("长度：" + name.length()); // 7

        // 2、提取字符串中某个位置索引的字符
        System.out.println(name.charAt(2)); // 黑

        System.out.println("---------------------");
        // 遍历字符串
        for (int i = 0; i < name.length(); i++) { // name.length().fori
            char c = name.charAt(i);
            System.out.print(c + " ");
        }
        System.out.println("\n----------------------");

        // 3、将字符串转成字符数组，再进行遍历
        char[] chars = name.toCharArray();
        for (int i = 0; i < chars.length; i++) { // chars.fori
            char c = chars[i];
            System.out.print(c + " ");
        }
        System.out.println("\n----------------------");

        // 4、equals：“判断字符串内容”，内容一样就返回true。【重点】
        String s1 = new String("黑马666");
        String s2 = new String("黑马666");
        System.out.println(s1 == s2); // false
        System.out.println(s1.equals(s2)); // ture

        // 5、忽略大小写比较字符串内容（常用于字符串比较）
        String t1 = "a6GFo";
        String t2 = "a6gfo";
        System.out.println(t1.equals(t2)); // false 适合精准匹配
        System.out.println(t1.equalsIgnoreCase(t2)); // true 忽略大小写

        // 6、截取字符串内容（包前不包后的）
        String st = "黑马程序员999";
        String rs = st.substring(0, 2);
        System.out.println(rs); // 黑马

        // 7、从当前索引位置一直截取到字符串的末尾
        String rs2 = st.substring(2);
        System.out.println(rs2); // 程序员999

        // 8、把字符串中的某个内容替换为新内容，并返回新的字符串对象给我们【Jax我太喜欢了】
        String info = "这个游戏简直是个垃圾，sb，去你大爷，还我血汗钱30块，垃圾！";
        // 因为返回的是一个字符串对象，所以我们可以链式编程
        String re3 = info.replace("垃圾", "**").replace("sb", "**");
        System.out.println(re3);

        // 9、判断字符串中是否包含某个关键字
        String st2 = "黑马程序员999";
        System.out.println(st2.contains("黑马")); // true
        System.out.println(st2.contains("999")); // true
        System.out.println(st2.contains("699")); // false

        // 10、判断字符串是否以某个字符串开头
        // startsWith 判断是否以什么内容开头
        System.out.println(st2.startsWith("黑马")); // true
        System.out.println(st2.startsWith("黑马9")); // false

        // endsWith 判断是否以什么内容结尾
        System.out.println(st2.endsWith("黑马程序员")); // false

        // 11、把字符按照某个指定内容分割成多个字符串，
        // 放到一个字符串数组里面返回给我们
        String result = "陈羽凡,王宝强,贾乃亮";
        String[] names = result.split(",");
        for (int i = 0; i < names.length; i++) {
            System.out.println(names[i]);
        }
    }
}
```

---

**案例：使用 String 来开发验证码**

**需求：**

实现随机产生验证码，验证码的每位可能是数字、大写字母、小写字母。

**分析：**

> 1. 设计一个方法，该方法接收一个整型参数，最终要返回对应位数的随机验证码。
> 2. 方法内定义两个字符串变量：一个用来记住要生成的验证码，一个用来记住要用到的全部字符。
>
> ```Java
> String code = "";
> String data ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
> ```
>
> 1. 使用for循环控制生成多少位随机字符，每次得到一个字符范围内的随机索引，根据索引提取该字符，把该字符交给code变量连接起来，循环结束后，在循环外返回code即可。
> 2. 主程序中，调用该方法即可得到随机验证码了。

**练习：**

```Java
package com.sundae.string;

import java.util.Random;

public class StringTest5 {
    public static void main(String[] args) {
        // 目标：使用String开发验证码
        System.out.println(createCode(4));
        System.out.println(createCode(7));
    }
   public static String createCode(int len){
       Random r = new Random();
       // 1、定义两个字符串变量来记住生成的验证码和要用到的全部字符
       String code = ""; // 记住验证吗
       String data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"; // 全部随机字符

       // 2、使用for循环来控制生成多少位的字符，然后拼接返回就是验证码
       for (int i = 0; i < len; i++) {
           // 3、随机产生索引
            int index = r.nextInt(data.length());
            // 4、根据随机索引提取对应位置处的字符
           char ch = data.charAt(index);
            code += ch;
       }
        return code;
   }
}
```

##### **2）ArrayList**

ArrayList是一个集合。

1. *什****么是集合？***

> - ArrayList 是一个集合。集合是一种容器，用来装数据的，类似于数组。

1. **有数组，为啥还用集合？**

> - 举个例子，假如说我们要开发一个简易版的购物车，问：这个购物车的商品是随时可能变多，还是随时可能变少？肯定随时可能变多，随时可能变少。所以说，万一我一下子想加100个商品，你不能把它固定死吧？

**`因为：`**

- 数组定义完成并启动后，**长度就固定了**。
- 集合它大小可变，开发中用的更多。（**而且集合的功能会更强大一些，集合里面还有很多其他的功能**）

1. **集合种类很多**

按照面向对象的思想，肯定有很多东西来代表集合啊。

<sheet sheet-id="9rIwsU" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

<callout emoji="💫">
***那我们怎么学 ArrayList 呢？***
既然是个容器，那我们Java中肯定提供了方法啊。
1. **会提供创建容器对象的方式**。
> 首先要想清楚，它是用一个对象来代表这个容器，而不是真的有一个容器。
>
> 学会创建一个ArrayList对象来代表一下这个容器。
1. **会提供相应的方法对容器进行操作**。
> 比如：添加数据、删除某个数据、修改某个数据、获取某个数据。
**简单来说，就是：**1、**学习创建对象**，2、**学习增删改查的方法**，3、**再了解一下容器的其他特点**。基本上你的集合就精通了。
</callout>

1. **第一步：创建 ArrayList 对象**

**1）先导包（必须写）**

```Java
import java.util.ArrayList;
```

**2）创建语法**

```Java
// 存整数
ArrayList<Integer> list = new ArrayList<>();

// 存字符串
ArrayList<String> list2 = new ArrayList<>();
```

- `<Integer>`：限定只能存 int 数据（蓝桥杯最常用）
- 空的 list，长度为 0

---

1. **第二步：核心操作 —— 增、删、改、查（8 个方法）**

**① 增（添加数据）**

```Java
list.add(10);     // 往末尾加 10
list.add(20);     // 往末尾加 20
list.add(3, 100); // 在下标 3 的位置插入 100
```

**竞赛用途**：读入数据、存答案、存路径。

---

**② 查（获取数据）**

```Java
int num = list.get(0); // 获取下标 0 的元素
```

- 下标从 0 开始，和数组一样

---

**③ 改（修改数据）**

```Java
list.set(1, 99); // 把下标 1 的元素改成 99
```

---

**④ 删（删除数据）**

```Java
list.remove(2);      // 删除下标 2 的元素
list.remove(Integer.valueOf(10)); // 删除第一个值为 10 的元素
```

---

**⑤ 获取长度**

```Java
int size = list.size();
```

对应数组的 `length`

---

**⑥ 清空**

```Java
list.clear();
```

---

**⑦ 判断是否为空**

```Java
boolean empty = list.isEmpty();
```

---

**⑧ 判断是否包含某个元素**

```Java
boolean has = list.contains(20);
```

---

1. **第三步：遍历 ArrayList**

**方式 1：普通 for（最常用，可控下标）**

```Java
for (int i = 0; i < list.size(); i++) {
    int num = list.get(i);
    System.out.println(num);
}
```

**方式 2：增强 for（只遍历）**

```Java
for (int num : list) {
    System.out.println(num);
}
```

---

1. **ArrayList 特点（竞赛必懂）**

   1. **长度可变**：不用提前定大小，随便 add
   2. **只能存包装类**：int → Integer，double → Double
   3. **下标访问和数组一样快**
   4. **插入删除慢**，但蓝桥杯数据小，随便用
   5. **可以直接排序**

      ```Java
      Arrays.sort(list);
      ```

<callout emoji="💫">
**注意：**
**Arrays.sort (数组)** → 只给 **数组** 用
**Collections.sort(ArrayList)** → 才是给 **ArrayList** 用的
</callout>

---

1. **蓝桥杯真实应用场景**

**场景 1：读取若干个数，存起来，求最大值**

```Java
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<Integer> list = new ArrayList<>();

        list.add(5);
        list.add(9);
        list.add(3);
        list.add(12);

        // 求最大值
        int max = list.get(0);
        for (int i = 1; i < list.size(); i++) {
            if (list.get(i) > max) {
                max = list.get(i);
            }
        }
        System.out.println(max); // 12
    }
}
```

---

**场景 2：存多个答案，最后一起输出**

```Java
ArrayList<Integer> ans = new ArrayList<>();
ans.add(100);
ans.add(200);

for (int x : ans) {
    System.out.println(x);
}
```

---

**场景 3：排序（高频）**

```Java
import java.util.Collections;

Collections.sort(list); // 从小到大排序
```

---

**场景 4：动态添加数据（数组做不到）**

不知道多少数据时，用 ArrayList 最舒服：

```Java
// 读到 0 停止
while (true) {
    int x = sc.nextInt();
    if (x == 0) break;
    list.add(x);
}
```

---

**一句话总结**

1. **创建对象**：`ArrayList<Integer> list = new ArrayList<>();`
2. **增**：`add`
3. **查**：`get`
4. **改**：`set`
5. **删**：`remove`
6. **长度**：`size()`
7. **遍历**：for 循环
8. **竞赛用途**：存动态数据、存答案、排序、贪心、DFS 路径

---

##### **3）StringJoiner**

**String：**

```TypeScript
public class Test{
    public static void main(String[] args){
        String s = "";
        for(int i = 0; i < 1000000; i++){
            // 因为字符串对象是不可变的，因此每次拼接都会新创建一个字符串对象到堆里面。
            // 每次拼接都产生新对象，就指向新对象。
            // 这些是什么对象？都是些垃圾对象。
            // 而且这么多的对象在我们的内存中是很浪费内存的。
            s = s + "abc";
        }
        System.out.println(s);
    }
}
```

这个速度忒慢。

**StringBuilder：**

速度快了，但是代码多。

**StringJoiner：**

它认为 StringBuilder 性能是快了，但是写代码费劲。所以它提出了一个观点：**有没有既高效，又能更方便**的拼接？

> - JDK8 开始有的，跟 StringBuilder 一样，也是用来操作字符串的，也可以看作是一个字符串对象，创建之后里面的字符串内容是可变的。
> - 好处：不仅仅能提高字符串的操作效率，并且在有些场景下使用它操作字符串，代码会更简洁。

**构造器：**

<sheet sheet-id="omoPD9" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

**方法名称：**

<sheet sheet-id="L2WGcF" token="BwM1ssKZ4h2Xg2tw8ZlcrF8RnDb"></sheet>

```Java
public static String printArray(int[] array) {
    // 万一传进来的数组是null怎么办？所以要做卫语句拦截
    if (array == null) return null;
    // 1、创建一个StringJoiner对象
    // 参数一：间隔符号，参数二：开始符号，参数三：结束符号
    StringJoiner sj = new StringJoiner(", ", "[", "]");
    // 2、遍历数组数据
    for (int i = 0; i < array.length; i++) {
        int data = array[i];
        sj.add(Integer.toString(data));
    }
    return sj.toString();
}
```

##### **4）Math（见上面）**

##### **5）BigDecimal**

##### **6）日期时间**

---

###### **一、Java Time API 核心知识点**

1. **LocalDate**：表示**日期（年-月-日）**，不包含时间和时区。常用创建方式：`LocalDate.now()`（当前日期）、`LocalDate.of(2025, 12, 31)`（指定日期）、`LocalDate.parse("2025-12-31")`（解析字符串）。

1. **获取日期字段**：**`getYear()`** 获取年份，**`getMonthValue()`** 获取月份（1-12），**`getDayOfMonth()`** 获取日（1-31），**`getDayOfWeek().getValue()`** 获取星期几（**周一=1，周日=7**）。
2. **日期加减**：**`plusDays(n)`**、**`plusMonths(n)`**、**`plusYears(n)`** 向后推 n 天/月/年；**`minusDays(n)`**、**`minusMonths(n)`**、**`minusYears(n)`** 向前推 n 天/月/年。
3. **日期比较**：**`isAfter(其他日期)`** 判断是否在之后，**`isBefore(其他日期)`** 判断是否在之前，**`isEqual(其他日期)`** 判断是否相等。
4. **闰年判断**：**`isLeapYear()`** 方法直接返回是否为闰年。底层规则：**能被 400 整除**，或者**能被 4 整除但不能被 100 整除**。
5. **遍历日期区间**：**标准模板**为 `for (LocalDate d = start; !d.isAfter(end); d = d.plusDays(1))`，循环体内处理每一天。
6. **计算间隔天数**：**`ChronoUnit.DAYS.between(开始日期, 结束日期)`** 返回两个日期之间的天数差。
7. **DateTimeFormatter**：格式化与解析。**`DateTimeFormatter.ofPattern("yyyy-MM-dd")`** 创建格式器，**`日期.format(格式器)`** 转成字符串，**`LocalDate.parse(字符串, 格式器)`** 解析成日期。
8. **TemporalAdjusters**：日期调整器。**`with(TemporalAdjusters.firstDayOfMonth())`** 得到当月第一天，**`with(TemporalAdjusters.lastDayOfMonth())`** 得到当月最后一天。
9. **Period**：日期区间（年/月/日维度）。**`Period.between(开始, 结束)`** 得到 Period 对象，调用 **`getYears()`**、**`getMonths()`**、**`getDays()`** 获取差值。
10. **LocalTime**：表示**时间（时:分:秒.纳秒）**。常用：`LocalTime.now()`、`LocalTime.of(14, 30, 0)`、`getHour()`、`getMinute()`。
11. **LocalDateTime**：表示**日期+时间**。常用：`LocalDateTime.now()`、**`toLocalDate()`** 提取日期部分、**`toLocalTime()`** 提取时间部分。
12. **YearMonth**：表示**某年某月**。常用：`YearMonth.now()`、`YearMonth.of(2025, 2)`、**`lengthOfMonth()`** 获取该月天数。
13. **MonthDay**：表示**月-日（不包含年份）**。常用于判断生日，如 `MonthDay.of(12, 25)` 表示圣诞节。
14. **异常处理**：创建非法日期（如 2 月 30 日）会抛出 **`DateTimeException`**，可以用 try-catch 判断日期是否合法。

---

###### 二、必背代码片段

###### 创建日期

```Java
LocalDate d1 = LocalDate.now();                    // 当前日期
LocalDate d2 = LocalDate.of(2025, 12, 31);        // 指定日期
LocalDate d3 = LocalDate.parse("2025-12-31");     // 解析字符串
```

###### 获取年月日星期

```Java
int year = d.getYear();                // 年份
int month = d.getMonthValue();         // 月份 1-12
int day = d.getDayOfMonth();           // 日
int week = d.getDayOfWeek().getValue(); // 周一=1 周日=7
```

###### 日期加减

```Java
LocalDate tomorrow = d.plusDays(1);
LocalDate nextMonth = d.plusMonths(1);
LocalDate lastYear = d.minusYears(1);
```

###### 比较日期

```Java
if (d1.isAfter(d2)) { ... }
if (d1.isBefore(d2)) { ... }
if (d1.isEqual(d2)) { ... }
```

###### 闰年判断

```Java
boolean leap = d.isLeapYear();  // LocalDate 自带
// 或者自己写：
boolean isLeap = (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
```

###### 遍历日期区间（经典模板）

```Java
LocalDate start = LocalDate.of(2000, 1, 1);
LocalDate end = LocalDate.of(2025, 12, 31);
for (LocalDate d = start; !d.isAfter(end); d = d.plusDays(1)) {
    // 处理每一天
}
```

###### 计算两个日期的间隔天数

```Java
long days = ChronoUnit.DAYS.between(start, end);
```

---

###### 三、场景案例（由易到难）

###### 场景1：判断某年是否是闰年

```Java
LocalDate d = LocalDate.of(2024, 1, 1);
System.out.println(d.isLeapYear());  // true
```

###### 场景2：计算从出生到今天的总天数

```Java
LocalDate birth = LocalDate.of(2000, 1, 1);
LocalDate today = LocalDate.now();
long days = ChronoUnit.DAYS.between(birth, today);
```

###### 场景3：统计 2000-2025 年所有 13 号是星期五的个数

```Java
LocalDate start = LocalDate.of(2000, 1, 1);
LocalDate end = LocalDate.of(2025, 12, 31);
int count = 0;
for (LocalDate d = start; !d.isAfter(end); d = d.plusDays(1)) {
    if (d.getDayOfMonth() == 13 && d.getDayOfWeek().getValue() == 5) {
        count++;
    }
}
System.out.println(count);
```

###### 场景4：输出某个月的最后一天

```Java
LocalDate date = LocalDate.of(2025, 2, 1);
LocalDate lastDay = date.with(TemporalAdjusters.lastDayOfMonth());
System.out.println(lastDay);  // 2025-02-28（闰年就是29）
```

###### 场景5：计算两个日期之间有多少个星期一

```Java
LocalDate start = LocalDate.of(2025, 1, 1);
LocalDate end = LocalDate.of(2025, 12, 31);
int count = 0;
for (LocalDate d = start; !d.isAfter(end); d = d.plusDays(1)) {
    if (d.getDayOfWeek().getValue() == 1) count++;
}
```

###### 场景6：解析用户输入的日期字符串

```Java
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
LocalDate date = LocalDate.parse("2025-12-31", formatter);
```

###### 场景7：判断一个日期是否合法（比如 2 月 29 日只在闰年存在）

```Java
public static boolean isValidDate(int year, int month, int day) {
    try {
        LocalDate.of(year, month, day);
        return true;
    } catch (DateTimeException e) {
        return false;
    }
}
```

---

##### **7）Arrays**

<callout emoji="💫">
### Arrays
Arrays 是用来操作数组的一个工具类。（Java 中似乎有这么一个特点，就是只要是后面带“s”的，一般都是工具类。）
</callout>

1. **Arrays 是什么？**

- 专门用来**操作数组**的工具类
- 提供：**排序、查找、填充、复制、转字符串、比较**等方法。
- 必须导包：`import java.util.Arrays;`

---

1. **核心方法（竞赛只考这 6 个）**

**① 排序（最最常用）**

对数组**升序排序**，找最大最小、中位数、去重都靠它

```Java
int[] arr = {3,1,4,2};
Arrays.sort(arr);  // 排序后：1 2 3 4
```

**蓝桥杯场景**：求最值、贪心、两数之和、去重

---

**② 二分查找（必须先排序）**

在有序数组中找一个数的下标，找不到返回负数

```Java
int index = Arrays.binarySearch(arr, 3);
```

**注意**：必须先用 `Arrays.sort()` 排序

---

**③ 数组填充（初始化）**

把数组所有位置设为同一个值

```Java
int[] a = new int[5];
Arrays.fill(a, 10);  // 全部变成 10
```

**场景**：初始化 dp 数组、标记数组

---

**④ 数组复制**

复制一个新数组，不改变原数组

```Java
int[] newArr = Arrays.copyOf(arr, arr.length);
```

**场景**：保留原数组，需要一个副本操作

---

**⑤ 把数组转成字符串（方便输出**）

直接打印数组，不用写循环

```Java
System.out.println(Arrays.toString(arr));
```

输出格式：`[1, 2, 3, 4]`

---

**⑥ 判断两个数组是否相等**

```Java
boolean same = Arrays.equals(arr1, arr2);
```

**场景**：判断两组数据是否完全一样

---

<callout emoji="💫">
#### 一句话总结
- **排序用 `Arrays.sort(数组)`**
- **打印数组用 `Arrays.toString(数组)`**
- **初始化用 `Arrays.fill`**
- **有序查找用 `Arrays.binarySearch`**
- **复制用 `Arrays.copyOf`**
只要是**数组**的工具操作，全部找 `Arrays` 类。
</callout>
