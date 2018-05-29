## 发版基本流程
```shell
cd /project_name/workspace/server/src
svn up
sh cbuild release
cd ../
sh publish_release.sh
cd ../publish_release
sh realpublish.sh
cd ../../script
sh list_version.sh
sh create_version.sh
```

## 各种路径
```javascript

工作台路径： 
/mg37_cn/htdocs/workbench/xls2xml

服务端发版版本路径：
/data2/ops/tmp/mg05/cn/server/ver

svn权限文件路径:
50服务器
修改/添加 /data2/repos/hxm1/conf 下的 authz
修改/添加 /data2/repos/hxm1/conf 下的 passwd
51服务器
修改/添加 /data/repos/xxqy/conf 下的 authz
修改/添加 /data/repos/xxqy/conf 下的 passwd

服务端编译生成客户端错误码svn路径：
/mg37_vn/workspace/tool/generrnum/client/

开发服日志路径：
/ug04_cn/temp/log/
```
