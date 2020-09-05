from tortoise import models, fields


class User(models.Model):
    id = fields.BigIntField(pk=True, description="discord user id")
    neis_ae = fields.CharField(
        max_length=3, description="neis education office code", null=True
    )
    neis_se = fields.CharField(max_length=7, description="neis school code", null=True)
    school_type = fields.CharField(
        max_length=3, description="user school type", null=True
    )
    iamschool = fields.CharField(
        max_length=5, default="0", description="iamschool school code"
    )
    public = fields.BooleanField(
        default=True, description="whether make data public or not"
    )
    grade = fields.IntField(description="user school grade", null=True)
    class_ = fields.IntField(description="user school class", null=True)

    class Meta:
        table = "users"
        table_description = "Table of user datas"

    def __int__(self):
        return self.id

    def __repr__(self):
        return (
            f"<User"
            f"id={self.id}"
            f"neis_ae={self.neis_ae}"
            f"neis_se={self.neis_se}"
            f"school_type={self.school_type}"
            f"iamschool={self.iamschool}"
            f"public={self.public}"
            f"grade={self.grade}"
            f"class={self.class_}"
            ">"
        )
