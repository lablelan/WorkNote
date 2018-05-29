## 查找字符串
```javascript
# 用/查找str字符串
/str
# 用？查找str字符串
?str
```

## 设置查找是否区分大小写
```javascript
# 不区分大小写
:set ic
# 区分大小写
:set noic
```

## 替换
```javascript
# 替换当前行第一个str1为str2
:s/str1/str2
# 替换当前行所有str1为str2
:s/str1/str2/g
# 替换当前文本中所有str1为str2
:%s/str1/str2/g
```