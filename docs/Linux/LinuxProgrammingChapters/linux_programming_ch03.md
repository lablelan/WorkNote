## 01系统调用-库函数
| Name | Descriptions |
| - | -: |
| open | 打开文件或设备 |
| read | 从打开的文件或设备里读数据 |
| write | 向文件或设备写数据 |
| close | 关闭文件或设备 |
| ioctl | 把控制信息传递给设备驱动程序 |

1.write系统调用
```c++
#include <stdio.h>
#include <stdlib.h>

/* size_t write(int fildes, const void *buf, size_t nbytes);
* @fildes 文件描述符
* @buf    写入的buf
* @nbytes 写入字节数
* @return 实际写入字节数，失败返回-1
*/

int main()
{
    if ((write(1, "Here is some data\n", 18)) != 18)
    {
        write(2, "A write error has occurred on file descriptor 1\n", 46);
    }

    exit(0);
}
```
2.read系统调用
```c++
#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>

/*
* size_t read(int fildes, void *buf, size_t nbytes);
* @fildes 文件描述符
* @buf 读取缓冲buf
* @nbytes 从文件读取的字节数
* @return 返回实际读取的字节数，失败返回-1
*/

int main(int argc, char *argv[])
{
    char buffer[128];
    int nread;

    nread = read(0, buffer, 128);
    if (nread == -1)
    {
        write(2, "A read error has occurred\n", 26);
    }

    if ((write(1, buffer, nread)) != nread)
    {
        write(2, "A write error has occurred\n", 27);
    }

    printf("argc:%d, argv[0]:%s, argv[1]:%s", argc, argv[0], argv[1]);

    exit(0);
}
```
3.open系统调用
```c++
#include<stdio.h>
#include<stdlib.h>

#include<fcntl.h>
#include<sys/types.h>
#include<sys/stat.h>

/*
* int open(const char *path, int oflags);
* @path 文件路径
* @oflags 指定打开文件采用的行为(只读/只写/读写)|(末尾追加/丢弃已有内容)
* @return 返回一个新的文件描述符,返回-1设置全局变量errno来指明失败原因
*
* int open(const char *path, int oflags, mode_t mode);
* @path 文件路径
* @oflags 指定打开文件采用的行为(只读/只写/读写)|(末尾追加/对齐已有内容/按参数mode访问模式创建文件/阻>止同时创建同一个文件)
* @mode 当oflags带有O_CREAT创建标志时，指定创建文件的权限及所属（与umask有关）
* @return 返回一个新的文件描述符，返回-1设置全局变量errno来指明失败原因
*/

int main()
{
    int err = open("myfile", O_CREAT|O_EXCL, S_IRUSR|S_IXOTH);

    printf("%d", err);

    exit(0);
}
```
4.close系统调用
```c++
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>

/*
* int close(int fildes);
* @fildes 文件描述符
* @return 释放文件描述符成返回0，否则返回-1
*/

int main()
{
   int fd = open("myfile", O_RDONLY);

   printf("fd:%d\n", fd);

   int close_err = close(fd);
   printf("close_err:%d\n", close_err);

   exit(0);
}
```
5.ioctl系统调用
```c++
#include <stdio.h>

#include <unistd.h>

/*
* int ioctl(int fildes, int cmd, ...);
* @fildes 文件描述符
* @cmd 文件描述符引用对象执行的操作
* @... 执行操作的不同的可选补充参数
* @return 返回操作是否成功
*/

int main()
{
    // linux系统上将键盘的LED等打开
    ioctl(tty_fd, KDSETLED, LED_NUM|LED_CAP|LED_SCR);

    exit(0);
}
```

## 02系统调用-复制文件例子
准备：1MB大小的file.in文件

demo01 copy_sys.c
```c++
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>

/*
* 一个一个字符地读写，1MB的文件需要系统调用2097152次
*/

int main()
{
    char c;
    int in = -1, out = -1;

    in = open("file.in", O_RDONLY);
    out = open("file.out", O_WRONLY|O_CREAT, S_IRUSR|S_IWUSR);
    while(read(in, &c, 1) == 1)
    {
        write(out, &c, 1);
    }

    exit(0);
}
```
demo02 copy_sys_block.c
```c++
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>

/*
* 以1024字节为一块地读写，1MB的文件只需2048次系统调用
*/

int main()
{
    char block[1024] = { 0 };
    int in = -1, out = -1;
    int nread = 0;

    in = open("file.in", O_RDONLY);
    out = open("file.out", O_WRONLY|O_CREAT, S_IRUSR|S_IWUSR);
    while((nread = read(in, block, sizeof(block))) > 0)
    {
        write(out, block, nread);
    }

    exit(0);
}
```
效率对比:
```javascript
rm -rf file.out
TIMEFORMAT="" time ./copy_sys
TIMEFORMAT="" time ./copy_sys_block
```

## 03C标准库-I/O函数
| Name | Descriptions |
| - | -: |
| fopen | 类似底层的opne系统调用。有输入/输出缓冲。返回一个文件流。 |
| fclose | 关闭指定的文件流stream，使所有尚未写出的数据都写出(close隐藏执行了一次flush操作)。 |
| fflush | 把文件流里未写出的数据立即写出。 |
| fseek | 与lseek对应。指定下一次读写操作的指定位置。 |
| fread | 从一个指定文件流读取数据记录，并写到ptr指向的数据缓冲区。 |
| fgetc | 从一个文件流里去除下一个字节并作为一个字符返回。当它达到文件尾或出现错误时，返回EOF。 |
| getc | 与fgetc作用相同，它很可能被实现为一个fgetc的宏。 |
| getchar | 相当于getc(stdin)，它从标准输入里读下一个字符。注意它把字符当做int而不是char，这样就运行文件尾(EOF)标志取值-1。 |
| fgets | 将字符写到参数s指向的的字符串里，直到遇到 换行符/已经输出了指定长度n-1个字符/达到文件尾 时在结尾加上\0。 |
| gets | 与fgets类似，不过它从标准输入读取数据并丢弃遇到的换行符\n。它在接收字符串的尾部加上一个null字节。注意：get对传输字符个数并没有限制，这意味着它可能会移除字节的传输缓冲区。 |
| fwrite | 从一个指定文件流取出数据记录，并写到输出流中。 |
| fputc | 把一个字符写到一个输出文件流中。 |
| putc | 与fputs作用相同，它很可能被实现为一个fputc的宏。 |
| putchar | 相当于putc(c, stdout)，它把单个字符写到标准输出。注意它把字符当做int而不是char，这样就运行文件尾(EOF)标志取值-1。 |
| fputs | 将参数s字符串写入文件流stream中，写入n个字符。 |
| puts |  |
| printf | 把自己的输出送到标准输出。 |
| fprintf | 把自己的输出送到指定文件流 |
| sprintf | 发自己的输出和一个结尾控制阀写到作为参数传递过来的字符串s里。这个s字符串必须足够容纳所有的输出数据。 |

1.fopen、fclose
```c++
#include <stdio.h>
#include <stdlib.h>

/*
* FILE *fopen(const char *filename, const char *mode);
* @filename 打开文件名
* @mode 打开文件方式
* @return 成功返回文件流，失败返回NULL
*/

/*
* int fclose(FILE *stream);
* @stream 指定文件流
* @return 成功返回0，失败返回非0
*/

int main()
{
    FILE *in = NULL;

    in = fopen("file.in", "r");

    if(in != NULL)
    {
        printf("in: %d\n", in);
        int a = fgetc(in);
        printf("%d\n", a);    
    }
    else
    {
        printf("fopen execuet error\n");
    }

    int close_ret = 0;
    printf("in:%d\n", in);
    close_ret = fclose(in);
    printf("close_ret: %d\n", close_ret);

    exit(0);
}
```
2.fgetc、getc
```c++
#include <stdio.h>
#include <stdlib.h>

/*
* int fgetc(FILE *stream);
* @stream 指定文件流
* @return 成功返回读取的字符，失败返回-1
*/

/*
* int getc(FILE *stream);
* @stream 指定文件流
* @return 成功返回读取的字符，失败返回-1
*/

int main()
{
    FILE *in = NULL;

    in = fopen("file.in", "r");

    int c = fgetc(in);
    printf("%c\n", c);
    int b = getc(in);
    printf("%c\n", b);

    int ret = fclose(in);
    printf("%d\n", ret);

    return 0;
}
```
3.fgets
```c++
#include <stdio.h>
#include <stdlib.h>

/*
* char *fgets(char *s, int n, FILE *stream);
* @s 存放读取的字符串
* @n 读取字符串的长度
* @stream 指定文件流
* @return 成功返回s的指针，失败返回NULL
*/

int main()
{
    FILE *in = NULL;

    in = fopen("file.in", "r");
    char s[1024] = { 0 };
    char *tmp = NULL;

    tmp = fgets(s, 1023, in);

    if(tmp != NULL)
    {
        printf("%s\n", s);
        printf("%s\n", tmp);
    }

    int ret = fclose(in);
    printf("close:%d\n", ret);

    exit(0);
}
```

4.fputc、putc
```c++
#include <stdio.h>
#include <stdlib.h>

/*
* int fputc(int c, FILE *stream);
* @c 将要写入的字符
* @stream 指定的文件流
* @return 成功返回0，失败返回EOP
*/

/*
* int putc(int c, FILE *stream);
* @c 将要写入的字符
* @stream 指定的文件流
* @return 成功返回0，失败返回EOF
*/

int main()
{
    FILE *out = NULL;
    out = fopen("file.out", "w");

    if (out != NULL)
    {
        int fp_ret = fputc(64, out);
        printf("fp_ret: %d\n", fp_ret);
        int p_ret = putc(65, out);
        printf("p_ret: %d\n", p_ret);
    }

    int close_ret = fclose(out);
    printf("close_ret:%d", close_ret);

    exit(0);
}
```

5.fflush
```c++
#include <stdio.h>
#include <stdlib.h>

/*
 * int fflush(FILE *stream);
 * @stream 指定文件流
 * @return 成功返回0，失败返回EOF
 */

int main()
{
    FILE *out = NULL;
    out = fopen("file.out", "w");

    if (out != NULL)
    {
        fputc(67, out);
        int ff_ret = fflush(out);
        printf("ff_ret: %d\n", ff_ret);
    }

    while(1)
    {
        printf("cat the file.out\n");
        sleep(1);
    }

    int close_ret = fclose(out);
    printf("close_ret:%d", close_ret);

    exit(0);
}

```