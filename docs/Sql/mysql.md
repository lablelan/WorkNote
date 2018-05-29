## 创建表
```mysql
CREATE TABLE `role_attr_detail6` (
`role_attr_detail6_id`  bigint(20) NOT NULL AUTO_INCREMENT ,
`role_id`  int(11) NOT NULL DEFAULT 0 ,
PRIMARY KEY (`role_attr_detail6_id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
ROW_FORMAT=Compact
;
INSERT INTO role_attr_detail6(role_attr_detail6_id,role_id) SELECT role_attr_detail5_id,role_id FROM role_attr_detail5;
```

## 修改字段大小
```mysql
ALTER TABLE `role_attr_detail4` MODIFY COLUMN `huashen_data`  varbinary(4096) NOT NULL DEFAULT '' AFTER `image_promotion_data`;
```

## 清除字段数据
```mysql
-- 方法1
update role_attr_detail SET roleactivity_data = '0';
-- 方法2
update role_attr_detail2 SET mount_data = '';
```

## 清空表数据
```mysql
-- 清空全部数据，不写日志，不可恢复，速度极快
truncate table 表名;
-- 清空全部数据，写日志，数据可恢复，速度慢
delete from 表名
```

## 删除表中一列
```mysql
alter table camp drop column king_data;
```

## 字段重命名
```mysql
ALTER TABLE `worldstatus` CHANGE COLUMN `cross_guildbattle_data` `cross_camp_battle_data`  varbinary(1024) NOT NULL DEFAULT '' AFTER `global_cd_data`;
```
