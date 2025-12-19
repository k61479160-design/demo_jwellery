import json
import logging
import random
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import razorpay
from .decorators import secure_account_access
from .models import (DiamondProduct, DiscountCode, Product, ProductCategory,
                     UserDiscount, UserProfile, Payment)
from django.core.mail import send_mail


def home(request):
    discount_codes = list(DiscountCode.objects.all())

    if discount_codes:
        selected_code = random.choice(discount_codes)
        code = selected_code.code
        percentage = selected_code.percentage
    else:
        code = "WELCOME"
        percentage = 5

    show_popup = False
    if request.user.is_authenticated:
        if request.session.get("new_user_registered") and not request.session.get(
            "popup_shown"
        ):
            show_popup = True
            request.session["popup_shown"] = True
            request.session["new_user_registered"] = False

            try:
                user_discount = UserDiscount.objects.get(
                    user=request.user, is_used=False
                )
                code = (
                    user_discount.discount_code.code
                    if user_discount.discount_code
                    else "WELCOME"
                )
                percentage = user_discount.percentage
            except UserDiscount.DoesNotExist:
                pass

    context = {
        "code": code,
        "percentage": percentage,
        "show_popup": show_popup,
    }

    return render(request, "jewelry/index.html", context)


def about(request):
    return render(request, "jewelry/about.html")


def about_lab_groun(request):
    return render(request, "jewelry/about-lab-groun.html")


def diamond(request):
    shape_choices = DiamondProduct.SHAPE_CHOICES
    selected_shape = request.GET.get("shape")
    products = DiamondProduct.objects.filter(status="available").order_by('carat')
    if selected_shape:
        products = products.filter(shape=selected_shape)
    context = {
        "products": products,
        "shape_choices": shape_choices,
        "selected_shape": selected_shape,
        "user_is_authenticated": request.user.is_authenticated,
    }
    return render(request, "jewelry/diamond.html", context)


def product(request):
    return render(request, "jewelry/product.html")


def collections(request):
 
    category_filter = request.GET.get("category")

    # Get regular products
    products = Product.objects.filter(status="active")
    
    # Get diamond products
    diamond_products = DiamondProduct.objects.filter(status="available").select_related("category")

    if category_filter:
        # Filter by category name in the new CharField
        products = products.filter(category__icontains=category_filter)
        diamond_products = diamond_products.filter(category__name=category_filter)
        selected_category = ProductCategory.objects.filter(
            name=category_filter, is_active=True
        ).first()
    else:
        selected_category = None

    categories = ProductCategory.objects.filter(is_active=True)

    context = {
        "products": products,
        "diamond_products": diamond_products,
        "categories": categories,
        "selected_category": selected_category,
        "category_filter": category_filter,
        "contact_email": "info.raivatstones@gmail.com",  
        "user_is_authenticated": request.user.is_authenticated,
    }

    return render(request, "jewelry/collections.html", context)


def category_page(request):
 
    categories = ProductCategory.objects.filter(is_active=True).order_by("sort_order", "display_name")
    
    # Calculate product counts manually since we changed the relationship
    for category in categories:
        regular_product_count = Product.objects.filter(
            category__icontains=category.display_name, 
            status="active"
        ).count()
        diamond_product_count = category.diamond_products.filter(status="available").count()
        category.product_count = regular_product_count + diamond_product_count

    context = {
        "categories": categories,
    }

    return render(request, "jewelry/category.html", context)


def testimonials(request):
    return render(request, "jewelry/testimonials.html")


def contact(request):
    form_success = request.GET.get("success") == "1"
    form_error = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = f"Contact Form Submission from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ["info.raivatstones@gmail.com"],
                fail_silently=False,
            )
            return redirect("/contact/?success=1")
        except Exception:
            form_error = True
    return render(
        request,
        "jewelry/contact.html",
        {"form_success": form_success, "form_error": form_error},
    )


def faq(request):
    return render(request, "jewelry/faq.html")


def policies(request):
    return render(request, "jewelry/policies.html")


def terms_and_condition(request):
    return render(request, "jewelry/terms_and_condition.html")


def cart(request):
    return render(request, "jewelry/cart.html")


def checkout(request):
    return render(request, "jewelry/checkout.html")


def order_confirmation(request):
    return render(request, "jewelry/order-confirmation.html")


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip().lower()
            if email == "info.raivatstones@gmail.com":
                return JsonResponse(
                    {
                        "success": False,
                        "message": "This email is reserved for admin use only.",
                    }
                )

            
            try:
                existing_user = User.objects.filter(email__iexact=email).first()
            except Exception:
                existing_user = None

            if existing_user:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "An account with this email address already exists. Please use a different email or try logging in.",
                    }
                )

            
            try:
                existing_username = User.objects.filter(username__iexact=email).first()
            except Exception:
                existing_username = None

            if existing_username:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "An account with this email address already exists. Please use a different email or try logging in.",
                    }
                )

            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=data.get("password"),
                first_name=data.get("firstName", ""),
                last_name=data.get("lastName", ""),
                is_active=True,
            )

            
            UserProfile.objects.create(
                user=user,
                phone_number=data.get("phone", ""),
                birth_date=data.get("birthDate"),
                street_number=data.get("streetNumber", ""),
                street_name=data.get("streetName", ""),
                city=data.get("city", ""),
                state=data.get("state", ""),
                zip_code=data.get("zipCode", ""),
                country=data.get("country", ""),
            )

            
            login(request, user)

            
            discount_codes = list(DiscountCode.objects.all())
            if discount_codes:
                selected_code = random.choice(discount_codes)
                code = selected_code.code
                percentage = selected_code.percentage
            else:
                
                code = "WELCOME"
                percentage = 5

            
            UserDiscount.objects.create(
                user=user,
                discount_code=selected_code if discount_codes else None,
                percentage=percentage,
            )

            
            request.session["new_user_registered"] = True

            return JsonResponse(
                {"success": True, "message": "Registration successful!"}
            )

        except Exception as e:
            logger.error(f"Error in signup: {str(e)}")
            return JsonResponse(
                {"success": False, "message": "Registration failed. Please try again."}
            )

    return render(request, "jewelry/signup.html")


@csrf_exempt
def check_email(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip().lower()

            
            if not email or "@" not in email:
                return JsonResponse(
                    {"exists": False, "message": "Invalid email format"}
                )

            
            try:
                existing_user = User.objects.filter(email__iexact=email).first()
            except Exception:
                existing_user = None

            return JsonResponse(
                {
                    "exists": existing_user is not None,
                    "message": (
                        "Email already exists" if existing_user else "Email available"
                    ),
                }
            )

        except Exception as e:
            logger.error(f"Error checking email: {str(e)}")
            return JsonResponse({"exists": False, "message": "Error checking email"})

    return JsonResponse({"exists": False, "message": "Invalid request method"})


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("loginEmail", "").strip().lower()
            password = data.get("loginPassword")
            
            if email == "info.raivatstones@gmail.com":
                return JsonResponse(
                    {
                        "success": False,
                        "message": "This email is reserved for admin use only.",
                    }
                )

            
            try:
                user = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Invalid email or password"}
                )

            
            authenticated_user = authenticate(
                request, username=email, password=password
            )

            if authenticated_user is not None and authenticated_user.is_active:
                login(request, authenticated_user)
                return JsonResponse({"success": True, "message": "Login successful!"})
            else:
                return JsonResponse(
                    {"success": False, "message": "Invalid email or password"}
                )

        except Exception as e:
            logger.error(f"Error in login_view: {str(e)}")
            return JsonResponse(
                {"success": False, "message": "Login failed. Please try again."}
            )

    return render(request, "jewelry/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")



logger = logging.getLogger(__name__)


@csrf_exempt
def forgot_password_view(request):
    """
    Simple password reset page - only accessible to logged-in users
    """
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    return render(request, "jewelry/forgot-password.html")


@csrf_exempt
def reset_password_view(request):
    """
    Reset password for logged-in users without email verification
    """
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "You must be logged in to reset your password"})
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_password = data.get("password", "").strip()
            confirm_password = data.get("confirm_password", "").strip()

            # Validate input
            if not new_password or not confirm_password:
                return JsonResponse({"success": False, "message": "Please fill in all fields"})

            if new_password != confirm_password:
                return JsonResponse({"success": False, "message": "Passwords do not match"})

            # Validate password strength
            try:
                validate_password(new_password)
            except ValidationError as e:
                return JsonResponse({"success": False, "message": str(e)})

            # Update user password
            try:
                user = request.user
                user.set_password(new_password)
                user.save()
                
                # Log the user out and redirect to login
                logout(request)
                
                logger.info(f"Password reset successful for user {user.username}")
                return JsonResponse({
                    "success": True, 
                    "message": "Password reset successful! Please sign in with your new password."
                })
                
            except Exception as e:
                logger.error(f"Error updating password for user {request.user.username}: {str(e)}")
                return JsonResponse({
                    "success": False, 
                    "message": "An error occurred while updating your password. Please try again."
                })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid request format"})
        except Exception as e:
            logger.error(f"Error in reset_password_view: {str(e)}")
            return JsonResponse({
                "success": False, 
                "message": "An error occurred. Please try again."
            })

    return JsonResponse({"success": False, "message": "Invalid request method"})



@secure_account_access
def account(request):
    
    
    try:
        profile = request.user.profile
    except Exception:
        
        profile = UserProfile.objects.create(user=request.user)

    
    payments = Payment.objects.filter(user=request.user).order_by("-created_at")
    total_payments = payments.count()
    total_amount = sum([p.get_total_payment_amount() for p in payments])

    context = {
        "user": request.user,
        "profile": profile,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,   
        "payments": payments,
        "total_payments": total_payments,
        "total_amount": total_amount,
    }

    return render(request, "jewelry/account.html", context)


def page_not_found(request, exception):
    return render(request, "jewelry/404.html", status=404)


def maintenance(request):
    return render(request, "jewelry/maintenance.html")


@csrf_exempt
def claim_discount(request):
    
    if request.method == "POST" and request.user.is_authenticated:
        try:

            user_discount = UserDiscount.objects.get(user=request.user, is_used=False)
            user_discount.mark_as_used()

            return JsonResponse(
                {
                    "success": True,
                    "message": f"Discount {user_discount.discount_code.code} ({user_discount.percentage}%) claimed successfully!",
                }
            )
        except UserDiscount.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "No unused discount found for this user."}
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Error claiming discount. Please try again.",
                }
            )

    return JsonResponse({"success": False, "message": "Invalid request."})


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
@csrf_exempt
def payment_page(request):
    return render(
        request,
        "jewelry/payment.html",
        {
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        },
    )


def diamond_size_chart(request):
    return render(request, "jewelry/diamond-size-chart.html")


def round_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/round.html")


def princess_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/princess.html")


@login_required
@csrf_exempt
def create_order(request):
    if request.method == "POST":
        import razorpay
        import json
        from django.http import JsonResponse
        data = json.loads(request.body)
        amount = data.get("amount")
        currency = data.get("currency", "INR")
        if not amount or not currency:
            return JsonResponse({"error": "Amount and currency are required."}, status=400)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            order = client.order.create({
                "amount": int(amount),
                "currency": currency,
                "payment_capture": 1
            })
            return JsonResponse({
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"]
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def verify_payment(request):
    """
    Verify Razorpay payment signature and persist a Payment record.
    Expects JSON body with: razorpay_payment_id, razorpay_order_id, razorpay_signature, amount (in smallest unit), currency.
    Requires authenticated user.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Authentication required."}, status=401)

    try:
        data = json.loads(request.body)
        payment_id = data.get("razorpay_payment_id")
        order_id = data.get("razorpay_order_id")
        signature = data.get("razorpay_signature")
        amount_smallest = data.get("amount")  # e.g., paise
        currency = data.get("currency", "INR")

        if not all([payment_id, order_id, signature]):
            return JsonResponse({"success": False, "message": "Missing required fields."}, status=400)

        # Verify signature
        import hmac
        import hashlib
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{order_id}|{payment_id}".encode(),
            hashlib.sha256,
        ).hexdigest()

        if generated_signature != signature:
            return JsonResponse({"success": False, "message": "Signature verification failed."}, status=400)

        # Fetch payment from Razorpay for authoritative status/amount
        try:
            rp_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            pinfo = rp_client.payment.fetch(payment_id)
            rp_status = pinfo.get("status")  # expected 'captured'
            rp_amount = pinfo.get("amount")  # in smallest unit
            rp_currency = pinfo.get("currency", currency)
        except Exception:
            rp_status = None
            rp_amount = amount_smallest
            rp_currency = currency

        # Normalize amount to major unit with precise Decimal arithmetic
        amount_major = (Decimal(rp_amount or 0) / Decimal(100)).quantize(Decimal('0.01'))

        status = "completed" if rp_status in ("captured", "authorized") else "pending"

        payment_obj, created = Payment.objects.get_or_create(
            user=request.user,
            payment_id=payment_id,
            defaults={
                "email": request.user.email,
                "amount": amount_major,
                "currency": rp_currency,
                "platform": "razorpay",
                "order_id": order_id,
                "razorpay_payment_id": payment_id,
                "status": status,
                "description": "Custom Payment",
            },
        )

        if not created:
            # Update existing record if needed
            payment_obj.amount = amount_major
            payment_obj.currency = rp_currency
            payment_obj.status = status
            payment_obj.save(update_fields=["amount", "currency", "status"]) 

        if status == "completed" and not payment_obj.completed_at:
            payment_obj.completed_at = timezone.now()
            payment_obj.save(update_fields=["completed_at"])

        return JsonResponse({"success": True})

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON."}, status=400)
    except Exception as e:
        logger.exception("Error verifying payment")
        return JsonResponse({"success": False, "message": "Server error."}, status=500)


def asscher_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/asscher.html")

def cusion_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/cusion.html")

def emrald_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/emrald.html")

def heart_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/heart.html")

def marquise_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/marquise.html")

def oval_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/oval.html")

def pear_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/pear.html")

def rec_cusion_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/rec-cusion.html")

def square_radint_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/square-radiant.html")


def radiant_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/radiant.html")

def trillion_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/trillion.html")

def baguette_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/baguette.html")

def hexagon_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/hexagon.html")

def lozenge_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/lozenge.html")

def shield_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/shield.html")

def tapered_baguette_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/tapered-baguette.html")

def briolette_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/briolette.html")

def half_moon_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/half-moon.html")

def square_caution_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/square-caution.html")

def coffin_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/coffin.html")

def bullet_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/bullet.html")

def trapezoid_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/trapezoid.html")

def square_radiant_diamond_size_chart(request):
    return render(request, "jewelry/size-chart/square-radiant.html")
