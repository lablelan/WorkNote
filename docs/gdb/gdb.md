## 调试core
```javascript
gbd process_name core_file_name
gdb -c core_file_name process_name
```

## 断点
| Name | Descriptions |
| - | -: |
| b | 断点 |
| c | 执行 |
| p | 打印 |
| q | 取消 |

使用gdb.txt断点打印后马上退出gdb不影响外服玩家操作。
gdb.txt:
```javascript
b 文件名:行数
c
p 变量
(其他操作)
q

# 例如
b mastercollect.cpp:121
c
p m_role->GetCommonDataParam()->master_collect_flags
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
