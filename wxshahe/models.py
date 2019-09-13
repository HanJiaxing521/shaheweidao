from django.db import models

# Create your models here.


class User(models.Model):
    # 用户的唯一ID
    user_id = models.TextField(primary_key=True)
    # 用户名
    user_name = models.TextField()
    # 用户头像
    user_image = models.TextField()
    # 用户身份
    user_manager = models.BooleanField(default=False)

    def __str__(self):
        user_id_str = str(self.user_id)
        return user_id_str


class Diet(models.Model):
    # 菜品的唯一ID
    diet_id = models.AutoField(primary_key=True)
    # 菜品名
    diet_name = models.TextField()
    # 菜品图片
    diet_image = models.TextField()
    # 菜品原料
    diet_material = models.TextField()
    # 菜品营养
    diet_nutrient = models.TextField()
    # 菜品位置
    diet_location = models.TextField()
    # cai pin jia ge
    diet_price = models.IntegerField()
    # 菜品点赞数
    diet_praise = models.IntegerField()
    # 大厨ID
    diet_cook_id = models.IntegerField(unique=False)

    def __str__(self):
        return self.diet_name


class Cook(models.Model):
    # 厨师唯一ID
    cook_id = models.AutoField(primary_key=True)
    # 厨师姓名
    cook_name = models.TextField(default=" ")
    # 厨师证件照
    cook_image = models.TextField()
    # 厨师介绍
    cook_brief_content = models.TextField()
    # 点赞数量
    cook_praise = models.IntegerField()

    def __str__(self):
        return self.cook_name


class Log(models.Model):
    # 记录唯一ID
    log_id = models.AutoField(primary_key=True)
    # 用户ID
    log_user_id = models.TextField()
    # 菜品ID
    log_diet_id = models.IntegerField()
    # 是否点赞
    log_diet_praise = models.BooleanField()
    # 评论
    log_diet_evaluation = models.TextField()

    def __str__(self):
        log_str = str(self.log_id)
        return log_str


class Attribution(models.Model):
    # 菜品ID(外键)
    diet_id = models.ForeignKey('Diet', on_delete=models.CASCADE)
    # 属性1
    attribution1 = models.IntegerField()
    # 属性2
    attribution2 = models.IntegerField()
    # 属性3
    attribution3 = models.IntegerField()
    # 属性4
    attribution4 = models.IntegerField()
    # 属性5
    attribution5 = models.IntegerField()
    # 属性6
    attribution6 = models.IntegerField()
    # 属性7
    attribution7 = models.IntegerField()
    # 属性8
    attribution8 = models.IntegerField()
    # 属性9
    attribution9 = models.IntegerField()

    def __str__(self):
        diet_str_id = str(self.diet_id)
        return diet_str_id


class Group(models.Model):
    # 簇心唯一ID
    user_id = models.TextField()
    # 所属类别
    group = models.IntegerField()


class Feedback(models.Model):
    # 意见唯一ID
    que_id = models.AutoField(primary_key=True)
    # 意见类型
    que_class = models.TextField()
    # 提交时间
    que_time = models.TextField()
    # 意见内容
    que_text = models.TextField()
    # 图片
    que_image = models.ImageField()
    # 联系方式
    que_message = models.TextField()
