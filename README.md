# Django-Smile-Serializer
A Seriailizer for django


一个django的models序列化工具，相比Django REST framework的学习成本将会大大减低，适合各种简单、快捷的需求

支持：

* 修改序列化日期格式（秒或毫秒）
* 序列化部分字段
* 序列化外键数据
* 序列化外键部分字段
* 兼容queryset或单个models数据


Install/安装
-----------
`pip install Django-Smile-Serializer`


Example/例子
-----------

models:
```python
class Tag(models.Model):
  name=models.CharField(u'名称', max_length=200)
  create_time = models.DateTimeField(auto_now_add=True, editable=False)
  

class Uset(models.Model):
  nickname=models.CharField(u'名称', max_length=200)
  phone=models.CharField(u'电话', max_length=11)
  create_time = models.DateTimeField(auto_now_add=True, editable=False)
```

Tag:

|id|name|
|:---|:---|
|1|学生|

User:

|id|name|phone|tag_id|
|:----|:----|:----|:----|
|1|user_1|13000000000|1|
|2|user_2|13000000002|1|


序列化queryset数据：

```python
from SmileSerializer import Serializer
users=User.objects.all()
data=Serializer(users).format()

print data
```

data:
```json
[
  {
    "id":1,
    "name":"user_1",
    "phone":"13000000000",
    "create_time":1504065533
  },
  {
    "id":2,
    "name":"user_2",
    "phone":"13000000002",
    "create_time":1504065533
  }
]
```

序列化单个数据：

```python
from SmileSerializer import Serializer
users=User.objects.get(id=1)
data=Serializer(users).format()

print data
```

data:
```json
{
  "id":1,
  "name":"user_1",
  "phone":"13000000000",
  "create_time":1504065533
}
```


Parameter/参数
-----------

|参数|类型|说明|
|:----|:----|:----|
|include_attr|list|需要序列化的字段|
|exclude_attr|list|不需要序列化字段|
|foreign|bool|是否序列化外键（默认否）|
|datetime_unit|string|序列化日期单位（秒：second、毫秒：millisecond，datetime_format为str时默认为：YYYY-MM-DD hh:mm:ss）|
|datetime_format|string|序列化日期格式（时间戳：timestamp、字符串：str）|
|data_type|string|系列化格式（raw、json）|

