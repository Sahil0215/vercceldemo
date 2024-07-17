from django.shortcuts import render,redirect,get_object_or_404
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
    ban=bank.objects.all()
    ban.delete()
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
def manage(request):
    return render(request, "manage.html")

@login_required(login_url="/login_page/")
def generate(request):
    if request.method == "POST":
        date = request.POST.get('date')
        invoice_from_id = request.POST.get('invoice_from')
        invoice_to_id = request.POST.get('invoice_to')
        no_of_items = request.POST.get('no_of_items')
        rate_of_each_item = request.POST.get('rate_of_each_item')
        qty_of_each_item = request.POST.get('qty_of_each_item')
        eway = request.POST.get('eway')
        vehicle_no = request.POST.get('vehicle_no')
        grand_total = request.POST.get('grand_total')

        try:
            # Fetch the seller and buyer objects
            invoice_from = get_object_or_404(seller, id=invoice_from_id)
            invoice_to = get_object_or_404(buyer, id=invoice_to_id)

            # Generate the invoice number
            invoice_no = invoice_from.invoice_count + 1

            # Create the invoice object
            invoice_object = invoice(
                invoice_no=invoice_no,
                date=date,
                invoice_from=invoice_from,
                invoice_to=invoice_to,
                no_of_items=no_of_items,
                rate_of_each_item=rate_of_each_item,
                qty_of_each_item=qty_of_each_item,
                eway=eway,
                vehicle_no=vehicle_no,
                grand_total=grand_total
            )

            # Save the invoice object
            invoice_object.save()

            # Update the invoice count for the seller
            invoice_from.invoice_count += 1
            invoice_from.save()

            return redirect("/view/")

        except seller.DoesNotExist:
            return render(request, 'generate.html', {
                'error_message': 'Seller does not exist.',
                'sellers': seller.objects.all(),
                'buyers': buyer.objects.all(),
                'items': item.objects.all()
            })
        except buyer.DoesNotExist:
            return render(request, 'generate.html', {
                'error_message': 'Buyer does not exist.',
                'sellers': seller.objects.all(),
                'buyers': buyer.objects.all(),
                'items': item.objects.all()
            })
        except Exception as e:
            return render(request, 'generate.html', {
                'error_message': str(e),
                'sellers': seller.objects.all(),
                'buyers': buyer.objects.all(),
                'items': item.objects.all()
            })

    else:
        sellers = seller.objects.all()
        buyers = buyer.objects.all()
        items = item.objects.all()
        return render(request, 'generate.html', {'sellers': sellers, 'buyers': buyers, 'items': items})


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
def generatesuccess(request):
    return render(request, "generatesuccess.html")









@login_required(login_url="/login_page/")
def manage_invoice(request):
    return render(request, "manage_invoice.html")


#Manage Page Functions
@login_required(login_url="/login_page/")
def additem(request):
    if request.method=="post":
        hsn=request.POST.get('hsn')
        name=request.POST.get('name')
        tax=request.POST.get('tax')

        item_object=item.object.create(
            hsn=hsn,
            name=name,
            tax=tax,
        )

        item_object.save()


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

        new_seller = seller(
            name=name,
            gst=gst,
            phone=phone,
            add=add,
            city=city,
            state=state,
            email=email,
            bal=bal
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



# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * B  A N K  - - - - S T A R T * * * * * * * * * * * * * * * * * * * * * * * * * *  *

@login_required(login_url="/login_page/")
def addbank(request):
    if request.method == "POST":
        s_gst_id = request.POST.get('s_gst')  # Assuming you're passing the seller ID
        name = request.POST.get('name')
        ac_no = request.POST.get('ac_no')
        branch = request.POST.get('branch')
        ifsc = request.POST.get('ifsc')

        s_gst = seller.objects.get(id=s_gst_id)  # Get the seller object

        bank_object = bank.objects.create(
            s_gst=s_gst,
            name=name,
            ac_no=ac_no,
            branch=branch,
            ifsc=ifsc
        )

        bank_object.save()
        return redirect("/generatesuccess/")
    else:
        return render(request, "manage.html")
    
# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * B  A N K  - - - - E N D  * * * * * * * * * * * * * * * * * * * * * * * * * *  *

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
        tax=request.POST.get('tax')
        item_object = item(
            hsn=hsn,
            name=name,
            tax=tax
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
    invoice_obj= get_object_or_404(invoice, id=invoice_id)
    if request.method == 'POST':
        invoice_obj.delete()
        return redirect('manage_invoice')
    return render(request, 'manage_invoice.html', {'invoice': invoice})


# def add_invoice(request):
#     if request.method == "POST":
#         date = request.POST.get('date')
#         invoice_from_id = request.POST.get('invoice_from')
#         invoice_from = get_object_or_404(seller, id=invoice_from_id)
#         invoice_to_id = request.POST.get('invoice_to')
#         transport=request.POST.get('transport')
#         invoice_to = get_object_or_404(buyer, id=invoice_to_id)
#         no_of_items = request.POST.get('no_of_items')
#         count=1
#         for i in  no_of_items:
#             item_details_id=int(request.POST.get('item_details_'+str(count)))
#             quantity_f=request.POST.get('quantity_'+str(count))
#             rate_f=request.POST.get('rate_'+str(count))
#             count= count+1
#             item_details_f=get_object_or_404(item, id=item_details_id)
#             billed_item_o=billedItem(
#                 item_details=item_details_f,
#                 quantity=quantity_f,
#                 rate=rate_f,
#                 total=int(quantity_f)*int(rate_f)
#             )
#             billed_item_o.save()
#             billed_items=billed_item_o
#         discount= request.POST.get('discount') 
#         eway = request.POST.get('eway')
#         vehicle_no = request.POST.get('vehicle_no')
#         grand_total = request.POST.get('grand_total')


#             # Generate the invoice number
#         invoice_no = invoice_from.invoice_count + 1

#             # Create the invoice object
#         invoice_object = invoice(
#                 invoice_no=invoice_no,
#                 date=date,
#                 invoice_from=invoice_from,
#                 invoice_to=invoice_to,
#                 no_of_items=no_of_items,
#                 billed_items=billed_items,
#                 eway=eway,
#                 transport=transport,
#                 vehicle_no=vehicle_no,
#                 grand_total=grand_total,
#                 discount=discount
#             )

#             # Save the invoice object
#         invoice_object.save()

#             # Update the invoice count for the seller
#         invoice_from.invoice_count += 1
#         invoice_from.save()

#         return redirect('/manage_invoice/')
#     else:
#         sellers = seller.objects.all()
#         buyers = buyer.objects.all()
#         items = item.objects.all()
#         return render(request, 'add_invoice.html', {'sellers': sellers, 'buyers': buyers, 'items': items})

from django.utils import timezone

@login_required(login_url="/login_page/")

def add_invoice(request):
    if request.method == 'POST':
        # Invoice details
        date = request.POST['date']
        bill_no = request.POST['bill_no']
        bill_from_id = request.POST['bill_from']
        bill_to_id = request.POST['bill_to']
        transport = request.POST['transport']
        no_of_items = int(request.POST['no_of_items'])
        eway = request.POST['eway']
        vehicle_no = request.POST['vehicle_no']
        discount = request.POST['discount']
        grand_total = request.POST['grand_total']

        bill_from = seller.objects.get(id=bill_from_id)
        bill_to = buyer.objects.get(id=bill_to_id)

        new_invoice = invoice(
            date=date,
            bill_no=bill_no,
            bill_from=bill_from,
            bill_to=bill_to,
            transport=transport,
            no_of_items=no_of_items,
            eway=eway,
            vehicle_no=vehicle_no,
            discount=discount,
            grand_total=grand_total,
        )
        new_invoice.save()

        for i in range(no_of_items):
            item_id = request.POST[f'item_{i}']
            quantity = int(request.POST[f'quantity_{i}'])
            rate = int(request.POST[f'rate_{i}'])
            total = quantity * rate

            billed_item = billedItem(
                item_details=item.objects.get(id=item_id),
                quantity=quantity,
                rate=rate,
                total=total,
            )
            billed_item.save()
            new_invoice.billed_items.add(billed_item)

        return redirect('invoice_list')  # Redirect to a list of invoices or wherever you need

    else:
        buyers = buyer.objects.all()
        sellers = seller.objects.all()
        items = item.objects.all()
        return render(request, 'create_invoice.html', {'buyers': buyers, 'sellers': sellers, 'items': items})

# * * * * * * * * * * * * *  * * * * * * * * * * * * * * * I N V O I C E - - - - E N D   * * * * * * * * * * * * * * * * * * * * * * * * * *  *


