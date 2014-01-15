create table info
(
id int(6) auto_increment not null primary key,
weixin_id char(50) not null,
xiezhua_id char(50) not null,
sendfrom char(100) default "微信",
sendreturn bool default 1,
timeline bool default 0
)CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
