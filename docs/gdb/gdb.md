## 调试core
```javascript
gbd process_name core_file_name
gdb -c core_file_name process_name
```

## 断点
b 断点

c 执行

p 打印

q 取消

gdb.txt:
```javascript
b 函数名
c
p 变量
(其他操作)
q
```
查看进程id：
```javascript
ps -aux | grep `pwd`             # 注意符号 ` 不是单引号 ’
```
gdb断点：
```javascript
gdb -p 进程id -x gdb.txt
```
