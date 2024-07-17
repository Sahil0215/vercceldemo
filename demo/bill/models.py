from django.db import models
from django.contrib.auth.models import User

class users_copy(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username + " => " + self.name

class buyer(models.Model):
    name = models.CharField(max_length=50)
    gst = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    add = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    email = models.CharField(max_length=50, blank=True, null=True)
    bal = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class seller(models.Model):
    name = models.CharField(max_length=50)
    gst = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    add = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    email = models.CharField(max_length=50, blank=True, null=True)
    bal = models.IntegerField(default=0)
    bill_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class employee(models.Model):
    name = models.CharField(max_length=50)
    empid = models.CharField(max_length=20, default=0)
    phone = models.CharField(max_length=15)
    add = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    bal = models.IntegerField(default=0)
    aadhaar = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class bank(models.Model):
    s_gst = models.ForeignKey(seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    ac_no = models.CharField(max_length=25)
    branch = models.CharField(max_length=20)
    ifsc = models.CharField(max_length=10)

    def __str__(self):
        return self.name + " => " + str(self.s_gst)

class item(models.Model):
    hsn = models.CharField(max_length=7)
    name = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class billedItem(models.Model):
    item_details = models.ForeignKey(item, on_delete=models.CASCADE, related_name='billed_item', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    rate = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Billed Item: {self.item_details.name} - Quantity: {self.quantity}"

class invoice(models.Model):
    date = models.DateField(blank=True, null=True)
    bill_no = models.PositiveIntegerField(unique=True)
    bill_from = models.ForeignKey(seller, on_delete=models.CASCADE, related_name='bill_from', blank=True, null=True)
    bill_to = models.ForeignKey(buyer, on_delete=models.CASCADE, related_name='bill_to', blank=True, null=True)
    transport=models.CharField(max_length=20, blank = True)
    no_of_items = models.PositiveIntegerField()
    billed_items = models.ManyToManyField(billedItem, related_name='invoices',blank=True, null=True)
    eway = models.CharField(max_length=20)
    vehicle_no = models.CharField(max_length=10)
    discount=models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()

    def __str__(self):
        return f"Bill {self.bill_no} - {self.date}"
