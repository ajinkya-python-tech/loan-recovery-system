from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import RecoveryCase



# =========================
# HOME PAGE
# =========================
def home_view(request):

    return render(
        request,
        'home.html'
    )

# =========================
# LOGIN VIEW
# =========================
def login_view(request):

    error = ''

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('add_case')

        else:

            error = 'Invalid username or password'

    return render(request, 'login.html', {
        'error': error
    })


# =========================
# SIGNUP VIEW
# =========================
def signup_view(request):

    error = ''

    if request.method == 'POST':

        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Username already exists
        if User.objects.filter(username=username).exists():

            error = 'Username already exists'

        # Password mismatch
        elif password != confirm_password:

            error = 'Passwords do not match'

        else:

            # Create user
            User.objects.create_user(
                username=username,
                password=password
            )
            User.is_superuser = False
            User.is_staff = False
            
            return redirect('login')

    return render(request, 'signup.html', {
        'error': error
    })


# =========================
# LOGOUT VIEW
# =========================
@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


# =========================
# ADD CASE VIEW
# =========================
@login_required
def add_case(request):

    errors = []

    form_data = {
        'vehicle_number': '',
        'customer_name': '',
        'phone_number': '',
        'customer_amount': '',
        'payment_date': '',
        'agent_name': '',
        'agent_pay': '',
        'recovery_status': '',
        'remarks': '',
    }

    if request.method == 'POST':

        form_data.update({

            'vehicle_number': request.POST.get(
                'vehicle_number', ''
            ).strip(),

            'customer_name': request.POST.get(
                'customer_name', ''
            ).strip(),

            'phone_number': request.POST.get(
                'phone_number', ''
            ).strip(),

            'customer_amount': request.POST.get(
                'customer_amount', ''
            ).strip(),

            'payment_date': request.POST.get(
                'payment_date', ''
            ).strip(),

            'agent_name': request.POST.get(
                'agent_name', ''
            ).strip(),

            'agent_pay': request.POST.get(
                'agent_pay', ''
            ).strip(),

            'recovery_status': request.POST.get(
                'recovery_status', ''
            ).strip(),

            'remarks': request.POST.get(
                'remarks', ''
            ).strip(),
        })

        # =========================
        # CUSTOMER AMOUNT VALIDATION
        # =========================
        if not form_data['customer_amount']:

            errors.append(
                'Customer amount is required.'
            )

        else:

            try:

                form_data['customer_amount'] = Decimal(
                    form_data['customer_amount']
                )

            except (InvalidOperation, ValueError):

                errors.append(
                    'Customer amount must be a valid number.'
                )

        # =========================
        # AGENT PAY VALIDATION
        # =========================
        if not form_data['agent_pay']:

            errors.append(
                'Agent pay is required.'
            )

        else:

            try:

                form_data['agent_pay'] = Decimal(
                    form_data['agent_pay']
                )

            except (InvalidOperation, ValueError):

                errors.append(
                    'Agent pay must be a valid number.'
                )

        # =========================
        # PAYMENT DATE VALIDATION
        # =========================
        if not form_data['payment_date']:

            errors.append(
                'Payment date is required.'
            )

        # =========================
        # SAVE DATA
        # =========================
        if not errors:

            RecoveryCase.objects.create(

                vehicle_number=form_data['vehicle_number'],

                customer_name=form_data['customer_name'],

                phone_number=form_data['phone_number'],

                customer_amount=form_data['customer_amount'],

                payment_date=form_data['payment_date'],

                agent_name=form_data['agent_name'],

                agent_pay=form_data['agent_pay'],

                recovery_status=form_data['recovery_status'],

                remarks=form_data['remarks'],

                created_by=request.user
            )

            return redirect('case_list')

    return render(request, 'add_case.html', {
        'errors': errors,
        'form_data': form_data,
    })


# =========================
# DASHBOARD VIEW
# =========================
@login_required
def dashboard_view(request):

    # Only super admin
    if not request.user.is_superuser:

        return redirect('add_case')

    all_cases = RecoveryCase.objects.all()

    # TOTAL CASES
    total_cases = all_cases.count()

    # TOTAL RECOVERY AMOUNT
    total_customer_amount = all_cases.aggregate(
        total=Sum('customer_amount')
    )['total'] or 0

    # TOTAL AGENT PAY
    total_agent_pay = all_cases.aggregate(
        total=Sum('agent_pay')
    )['total'] or 0

    # RELEASED CASES
    released_cases = all_cases.filter(
        recovery_status='Released'
    ).count()

    # GODOWNED CASES
    godowned_cases = all_cases.filter(
        recovery_status='Godowned'
    ).count()

    # CUSTOMER PAYMENT CASES
    customer_payment_cases = all_cases.filter(
        recovery_status='Customer Payment'
    ).count()

    return render(
        request,
        'dashboard.html',
        {

            'total_cases': total_cases,

            'total_customer_amount':
            total_customer_amount,

            'total_agent_pay':
            total_agent_pay,

            'released_cases':
            released_cases,

            'godowned_cases':
            godowned_cases,

            'customer_payment_cases':
            customer_payment_cases,
        }
    )


# =========================
# CASE LIST VIEW
# =========================
@login_required
def case_list(request):

    # Only super admin can access
    if not request.user.is_superuser:

        return redirect('add_case')

    # Get search filters
    vehicle_number = request.GET.get(
        'vehicle_number',
        ''
    ).strip()

    customer_name = request.GET.get(
        'customer_name',
        ''
    ).strip()

    # Get all cases
    cases = RecoveryCase.objects.all()

    # Filter by Vehicle Number
    if vehicle_number:

        cases = cases.filter(
            vehicle_number__icontains=vehicle_number
        )

    # Filter by Customer Name
    if customer_name:

        cases = cases.filter(
            customer_name__icontains=customer_name
        )

    # Latest first
    cases = cases.order_by('-id')

    return render(
        request,
        'case_list.html',
        {
            'cases': cases,
            'vehicle_number': vehicle_number,
            'customer_name': customer_name,
        }
    )


# =========================
# EDIT CASE VIEW
# =========================
@login_required
def edit_case(request, case_id):

    # Only super admin
    if not request.user.is_superuser:

        return redirect('add_case')

    case = RecoveryCase.objects.get(id=case_id)

    errors = []

    if request.method == 'POST':

        try:

            case.vehicle_number = request.POST.get(
                'vehicle_number'
            )

            case.customer_name = request.POST.get(
                'customer_name'
            )

            case.phone_number = request.POST.get(
                'phone_number'
            )

            case.customer_amount = Decimal(
                request.POST.get('customer_amount')
            )

            case.payment_date = request.POST.get(
                'payment_date'
            )

            case.agent_name = request.POST.get(
                'agent_name'
            )

            case.agent_pay = Decimal(
                request.POST.get('agent_pay')
            )

            case.recovery_status = request.POST.get(
                'recovery_status'
            )

            case.remarks = request.POST.get(
                'remarks'
            )

            case.save()

            return redirect('case_list')

        except Exception as e:

            errors.append(str(e))

    return render(
        request,
        'edit_case.html',
        {
            'case': case,
            'errors': errors
        }
    )


# =========================
# DELETE CASE VIEW
# =========================
@login_required
def delete_case(request, case_id):

    # Only super admin
    if not request.user.is_superuser:

        return redirect('add_case')

    case = RecoveryCase.objects.get(id=case_id)

    case.delete()

    return redirect('case_list')