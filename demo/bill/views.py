from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *


# Create your views here.
def main(request):
    return render(request, "main.html")

def login_page(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username= username).exists():
            messages.error(request, 'Invaild Username')
            return redirect('/login_page/')
        user=authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invaild Password')
            return redirect('/login_page/')
        
        else:
            login(request,user)
            return redirect('/home/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == "POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        cpass=request.POST.get('cpass')
        
        if(password!=cpass):
            messages.info(request, 'Password Doesnt Match')
            return redirect('/register/')
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'Username Already Exist')
            return redirect('/register/')
        user=User.objects.create(
            username=username
        )
        user.set_password(password)
        user.save()
        user_copy=users_copy.objects.create(name=name, phone=phone, email=email, username=username )
        user_copy.save()
        return redirect('/registersuccess/')
    return render(request, 'register.html')

@login_required(login_url="/login_page/")
def deleteallusers(request):
    s=seller.objects.all()
    s.delete()
    b=buyer.objects.all()
    b.delete()
    i=item.objects.all()
    i.delete()
    e=employee.objects.all()
    e.delete()
    bil=invoice.objects.all()
    bil.delete()
    user=users_copy.objects.all()
    user.delete()
    user=User.objects.all()
    user.delete()
    return redirect('/logout_page/')

def registersuccess(request):
    return render(request, "registersuccess.html")


@login_required(login_url="/login_page/")
def home(request):
    seller_count=len(seller.objects.all())
    buyer_count=len(buyer.objects.all())
    item_count=len(item.objects.all())
    employee_count=len(employee.objects.all())
    return render(request, "home.html", { 'seller_count': seller_count, 'buyer_count':buyer_count, 'item_count':item_count, 'employee_count':employee_count } )


@login_required(login_url="/login_page/")
def view(request):
    invoices=invoice.objects.all()
    if len(invoices)==0:
        messages.info(request, 'No invoice Found')
        return render(request, "view.html")
    return render(request, "view.html", {'invoices':invoices})




@login_required(login_url="/login_page/")
def entry(request):
    return render(request, "entry.html")


@login_required(login_url="/login_page/")
def manage_entry_payment(request):
    entry_payment_obj=entry_payment.objects.all()
    if len(entry_payment_obj)==0:
        messages.info(request, 'No Entries Found')
        return render(request, "manage_entry_payment.html")
    return render(request, "manage_entry_payment", {'payment':entry_payment_obj})


@login_required(login_url="/login_page/")
def delete_entry_payment(request, payment_id):
    payment_obj= get_object_or_404(entry_payment, id=payment_id)
    if request.method == 'POST':
        payment_obj.delete()
        return redirect('manage_entry_payment')
    return render(request, 'manage_entry_payment.html', {'payment': entry_payment})


@login_required(login_url="/login_page/")
def add_entry_payment(request):
    if request.method == "POST":
        person_type = request.POST.get('person_type') 
        name_id = request.POST.get('name')
        name = person_type.objects.get(id=name_id)

        transaction_type=request.POST.get('transaction_type')
        date = request.POST.get('date')
        amount = int(request.POST.get('amount'))
        mode = request.POST.get('mode')
        note = request.POST.get('note')

        last_transaction = entry_payment.objects.order_by('-transaction_no').first()
        if last_transaction:
            transaction_no = last_transaction.transaction_no + 1
        else:
            transaction_no = 1  

        new_transaction = entry_payment(
            person=name,
            transaction_type=transaction_type,
            date=date,
            amount=amount,
            mode=mode,
            note=note,
            transaction_no=transaction_no
        )

        new_transaction.save()
        

    else:
        sellers = seller.objects.all()
        buyers = buyer.objects.all()
        employees = employee.objects.all()
        return render(request, 'add_entry_payment.html', {'sellers': sellers, 'buyers': buyers, 'employees': employees})



@login_required(login_url="/login_page/")
def manage_entry_stock(request):
    entry_stock_obj=entry_stock.objects.all()
    if len(entry_stock_obj)==0:
        messages.info(request, 'No Entries Found')
        return render(request, "manage_entry_stock.html")
    return render(request, "manage_entry_stock", {'stock':entry_stock_obj})


@login_required(login_url="/login_page/")
def delete_entry_stock(request, stock_id):
    stock_obj= get_object_or_404(entry_stock, id=stock_id)
    if request.method == 'POST':
        stock_obj.delete()
        return redirect('manage_entry_stock')
    return render(request, 'manage_entry_stock.html', {'stock': entry_stock})


@login_required(login_url="/login_page/")
def add_entry_stock(request):
    if request.method == "POST":
        person_type = request.POST.get('person_type') 
        name_id = request.POST.get('name')
        name = person_type.objects.get(id=name_id)

        transaction_type=request.POST.get('transaction_type')
        date = request.POST.get('date')
        amount = int(request.POST.get('amount'))
        mode = request.POST.get('mode')
        note = request.POST.get('note')

        last_transaction = entry_stock.objects.order_by('-transaction_no').first()
        if last_transaction:
            transaction_no = last_transaction.transaction_no + 1
        else:
            transaction_no = 1  

        new_transaction = entry_stock(
            person=name,
            transaction_type=transaction_type,
            date=date,
            amount=amount,
            mode=mode,
            note=note,
            transaction_no=transaction_no
        )

        new_transaction.save()
        return render(request, 'manage_entry_stock.html')
        

    else:
        sellers = seller.objects.all()
        buyers = buyer.objects.all()
        employees = employee.objects.all()
        return render(request, 'add_entry_stock.html', {'sellers': sellers, 'buyers': buyers, 'employees': employees})


@login_required(login_url="/login_page/")
def entry_stock(request):
    return render(request, "entry_stock.html")









# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * B U Y E R - - - - S T A R T  * * * * * * * * * * * * * * * * * * * * * * * * * *  *

@login_required(login_url="/login_page/")
def manage_buyer(request):
    buyers=buyer.objects.all()
    if len(buyers)==0:
        messages.info(request, 'No Buyer Found')
        return render(request, "manage_buyer.html")
    return render(request, "manage_buyer.html", {'buyers':buyers})

@login_required(login_url="/login_page/")
def delete_buyer(request, buyer_id):
    buyer_obj= get_object_or_404(buyer, id=buyer_id)
    if request.method == 'POST':
        buyer_obj.delete()
        return redirect('manage_buyer')
    return render(request, 'manage_buyer.html', {'buyer': buyer})

@login_required(login_url="/login_page/")
def add_buyer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        gst = request.POST.get('gst')
        phone = request.POST.get('phone')
        add = request.POST.get('add', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email', '')
        bal = request.POST.get('bal', 0)

        new_buyer = buyer(
            name=name,
            gst=gst,
            phone=phone,
            add=add,
            city=city,
            state=state,
            email=email,
            bal=bal
        )
        new_buyer.save()
        return redirect('/manage_buyer/')

    return render(request, 'add_buyer.html')
    
# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * B U Y E R - - - - E N D  * * * * * * * * * * * * * * * * * * * * * * * * * *  *

# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * S E L L E R - - - - S T A R T * * * * * * * * * * * * * * * * * * * * * * * * * *  *

@login_required(login_url="/login_page/")
def manage_seller(request):
    sellers=seller.objects.all()
    if len(sellers)==0:
        messages.info(request, 'No Seller Found')
        return render(request, "manage_seller.html")
    return render(request, "manage_seller.html", {'sellers':sellers})

@login_required(login_url="/login_page/")
def delete_seller(request, seller_id):
    seller_obj= get_object_or_404(seller, id=seller_id)
    if request.method == 'POST':
        seller_obj.delete()
        return redirect('manage_seller')
    return render(request, 'manage_seller.html', {'seller': seller})

@login_required(login_url="/login_page/")
def add_seller(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        gst = request.POST.get('gst')
        phone = request.POST.get('phone')
        add = request.POST.get('add', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email', '')
        bal = request.POST.get('bal', 0)
        bank_name = request.POST.get('bank_name')
        bank_ac_no = request.POST.get('bank_ac_no')
        bank_branch = request.POST.get('bank_branch')
        bank_ifsc = request.POST.get('bank_ifsc')

        new_seller = seller(
            name=name,
            gst=gst,
            phone=phone,
            add=add,
            city=city,
            state=state,
            email=email,
            bal=bal,
            bank_name=bank_name,
            bank_ac_no=bank_ac_no,
            bank_branch=bank_branch,
            bank_ifsc=bank_ifsc
        )
        new_seller.save()
        return redirect('/manage_seller/')

    return render(request, 'add_seller.html')
    
# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * S E L L E R - - - - E N D  * * * * * * * * * * * * * * * * * * * * * * * * * *  *

# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * E M P L O Y E E - - - - S T A R T * * * * * * * * * * * * * * * * * * * * * * * * * *  *


@login_required(login_url="/login_page/")
def manage_employee(request):
    employees=employee.objects.all()
    if len(employees)==0:
        messages.info(request, 'No employee Found')
        return render(request, "manage_employee.html")
    return render(request, "manage_employee.html", {'employees':employees})

@login_required(login_url="/login_page/")
def delete_employee(request, employee_id):
    employee_obj= get_object_or_404(employee, id=employee_id)
    if request.method == 'POST':
        employee_obj.delete()
        return redirect('manage_employee')
    return render(request, 'manage_employee.html', {'employee': employee})


@login_required(login_url="/login_page/")
def add_employee(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        add = request.POST.get('add')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email')
        bal = request.POST.get('bal')
        aadhaar = request.POST.get('aadhaar')
        
        
        last_employee = employee.objects.all().order_by('empid').last()
        if last_employee:
            empid = int(last_employee.empid) + 1  # Ensure empid is an integer before incrementing
        else:
            empid = 1  # Start with 1 if no employees exist
        
        employee_object = employee(
            name=name,
            empid=empid,
            phone=phone,
            add=add,
            city=city,
            state=state,
            email=email,
            bal=bal,
            aadhaar=aadhaar
        )

        employee_object.save()
        return redirect("/manage_employee/")
    else:
        return render(request, "add_employee.html")
    
# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * E M P L O Y E E - - - - E N D  * * * * * * * * * * * * * * * * * * * * * * * * * *  *


# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * I T E M   - - - - S T A R T  * * * * * * * * * * * * * * * * * * * * * * * * * * *


@login_required(login_url="/login_page/")
def manage_item(request):
    items=item.objects.all()
    if len(items)==0:
        messages.info(request, 'No item Found')
        return render(request, "manage_item.html")
    return render(request, "manage_item.html", {'items':items})


@login_required(login_url="/login_page/")
def delete_item(request, item_id):
    item_obj= get_object_or_404(item, id=item_id)
    if request.method == 'POST':
        item_obj.delete()
        return redirect('manage_item')
    return render(request, 'manage_item.html', {'item': item})


@login_required(login_url="/login_page/")
def add_item(request):
    if request.method == "POST":
        hsn=request.POST.get('hsn')
        name=request.POST.get('name')
        sgst=Decimal(request.POST.get('sgst'))
        cgst=Decimal(request.POST.get('cgst'))
        stock=int(request.POST.get('stock'))
        item_object = item(
            hsn=hsn,
            name=name,
            sgst=sgst,
            cgst=cgst,
            stock=stock
        )

        item_object.save()
        return redirect("/manage_item/")
    else:
        return render(request, "add_item.html")



# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * I T E M   - - - -E N D   * * * * * * * * * * * * * * * * * * * * * * * * * *  *
# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * I N V O I C E    - - - -S T A R T    * * * * * * * * * * * * * * * * * * * * * * * * * *  *
@login_required(login_url="/login_page/")
def manage_invoice(request):
    invoices=invoice.objects.all()
    if len(invoices)==0:
        messages.info(request, 'No invoice Found')
        return render(request, "manage_invoice.html")
    return render(request, "manage_invoice.html", {'invoices':invoices})

@login_required(login_url="/login_page/")
def delete_invoice(request, invoice_id):
    invoice_obj = get_object_or_404(invoice, id=invoice_id)

    if request.method == 'POST':
        
        invoice_obj.invoice_to.bal -= invoice_obj.grand_total
        invoice_obj.invoice_to.save()

        
        for billed_item in invoice_obj.invoice_items.all():
            item = billed_item.item_details
            item.stock += billed_item.quantity
            item.save()


        invoice_obj.delete()
        
        return redirect('manage_invoice')
    
    return render(request, 'manage_invoice.html', {'invoice': invoice_obj})


@login_required(login_url="/login_page/")
def print_invoice(request, invoice_id):
    bill= invoice.objects.get(id=invoice_id)
    return render(request, 'view.html', {'bill': bill, 'x' : range(1,20-bill.no_of_items)})



from decimal import Decimal
from datetime import datetime

@login_required(login_url="/login_page/")
def add_invoice(request):
    if request.method == "POST":
        invoice_from_id = request.POST.get('invoice_from')
        invoice_to_id = request.POST.get('invoice_to')
        date = request.POST.get('date')
        eway = request.POST.get('eway')
        transport = request.POST.get('transport')
        vehicle_no = request.POST.get('vehicle_no')
        no_of_items = int(request.POST.get('no_of_items'))
        other_charges = Decimal(request.POST.get('other_charges', '0.00'))
        discount = Decimal(request.POST.get('discount', '0.00'))

        invoice_from = seller.objects.get(id=invoice_from_id)
        invoice_to = buyer.objects.get(id=invoice_to_id)
        
        invoice_from.bill_count += 1
        invoice_from.save()

        invoice_no = invoice_from.bill_count
        taxable_amt = Decimal('0.00')
        avg_sgst = Decimal('0.00')
        avg_cgst = Decimal('0.00')

        invoice_items_arr = []
        for i in range(1, no_of_items + 1):
            item_details_id = request.POST.get('item' + str(i))
            item_details = item.objects.get(id=item_details_id)
            quantity = int(request.POST.get('quantity' + str(i)))
            rate = Decimal(request.POST.get('rate' + str(i)))
            unit = request.POST.get('unit' + str(i))
            amount = quantity * rate
            taxable_amt += amount
            avg_sgst += item_details.sgst
            avg_cgst += item_details.cgst

            billedItem_object = billedItem(
                item_details=item_details,
                quantity=quantity,
                rate=rate,
                unit=unit,
                amount=amount
            )

            item_details.stock-=quantity
            item_details.save()


            billedItem_object.save()
            invoice_items_arr.append(billedItem_object)
        taxable_amt+=other_charges-discount
        avg_sgst = avg_sgst / no_of_items
        avg_cgst = avg_cgst / no_of_items
        sgst_amt = (taxable_amt * avg_sgst) / Decimal('100.00')
        cgst_amt = (taxable_amt * avg_cgst) / Decimal('100.00')
        tgst_amt = sgst_amt + cgst_amt
        grand_total = taxable_amt + tgst_amt

        date_obj = datetime.strptime(date, '%Y-%m-%d').date()

        invoice_obj = invoice(
            invoice_from=invoice_from,
            invoice_no=invoice_no,
            date=date_obj,
            eway=eway,
            transport=transport,
            vehicle_no=vehicle_no,
            invoice_to=invoice_to,
            no_of_items=no_of_items,
            other_charges=other_charges,
            discount=discount,
            taxable_amt=taxable_amt,
            sgst_amt=sgst_amt,
            cgst_amt=cgst_amt,
            tgst_amt=tgst_amt,
            grand_total=grand_total,
            grand_total_words=amount_to_words(grand_total)
        )

        invoice_to.bal+=grand_total
        invoice_to.save()

        invoice_obj.save()
        invoice_obj.invoice_items.set(invoice_items_arr)

        return redirect("/manage_invoice/")
    else:
        sellers = seller.objects.all()
        buyers = buyer.objects.all()
        items = item.objects.all()
        return render(request, 'add_invoice.html', {'sellers': sellers, 'buyers': buyers, 'items': items})

    

# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * I N V O I C E - - - - E N D   * * * * * * * * * * * * * * * * * * * * * * * * * *  *


from num2words import num2words

def amount_to_words(amount):
    amount_words = num2words(amount, lang='en_IN', to='currency', currency='INR').replace(",", "")
    amount_words = amount_words.capitalize()
    amount_words += " only"
    return amount_words
