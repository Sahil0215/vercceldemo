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
    add = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    gst = models.CharField(max_length=20)
    bal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.name

class seller(models.Model):
    gst = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    add = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50, blank=True, null=True)
    bal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bill_count = models.IntegerField(default=0)
    bank_name = models.CharField(max_length=30)
    bank_ac_no = models.CharField(max_length=25)
    bank_ifsc = models.CharField(max_length=20)
    bank_branch = models.CharField(max_length=20)

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
    bal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    aadhaar = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class item(models.Model):
    name = models.CharField(max_length=20)
    hsn = models.CharField(max_length=7)
    sgst = models.DecimalField(max_digits=5, decimal_places=2)
    cgst = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class billedItem(models.Model):
    item_details = models.ForeignKey(item, on_delete=models.CASCADE, related_name='billed_item', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(max_length=5, blank=True, null=True)
    def __str__(self):
        return f"Billed Item: {self.item_details.name} - Quantity: {self.quantity}"

class invoice(models.Model):
    invoice_from=models.ForeignKey(seller, on_delete=models.CASCADE, blank=True, null=True)
    invoice_no=models.PositiveIntegerField(default=0)
    date=models.DateField(blank=True, null=True)
    eway=models.CharField(max_length=25)
    transport=models.CharField(max_length=20)
    vehicle_no=models.CharField(max_length=15)
    invoice_to=models.ForeignKey(buyer, on_delete=models.CASCADE , blank=True, null=True)
    no_of_items=models.PositiveIntegerField(default=0)
    invoice_items=models.ManyToManyField(billedItem)
    other_charges=models.DecimalField(max_digits=10, decimal_places=2)
    discount=models.DecimalField(max_digits=10, decimal_places=2)
    taxable_amt=models.DecimalField(max_digits=10, decimal_places=2)
    sgst_amt=models.DecimalField(max_digits=10, decimal_places=2)
    cgst_amt=models.DecimalField(max_digits=10, decimal_places=2)
    tgst_amt=models.DecimalField(max_digits=10, decimal_places=2)
    grand_total=models.DecimalField(max_digits=10, decimal_places=2)
    grand_total_words=models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.invoice_no+"==>From-"+self.invoice_from.name+"==To-"+self.invoice_to.name


class entry_payment(models.Model):
    transaction_no=models.IntegerField(default=0)
    name=models.ForeignKey(seller, on_delete=models.CASCADE, blank=True, null=True)
    transaction_type=models.CharField(max_length=15)
    date=models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mode = models.CharField(max_length=15)
    note = models.CharField(max_length=200)

    
