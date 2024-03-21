# SHOE CART 🚀: Footwear E-commerce! 🌐

Welcome to SHOE CART, where style meets innovation in the world of footwear e-commerce.

## User Experience:

- **Secure OTP Login:** Elevate user security with seamless one-time password verification.
- **Size Variants:** Explore a diverse footwear collection with customizable size options for a personalized fit.
- **Smart Navigation:** Effortlessly find your perfect pair using intuitive search and advanced filtering options.
- **Inquiry Feature:** Engage with us! Have questions or need assistance? Utilize our easy inquiry system for quick responses.
- **Personalized Profiles:** Elevate your shopping journey with profiles tailored to your preferences.
- **Effortless Cart & Checkout:** Smoothly manage your shopping cart and experience a hassle-free checkout process.
- **Flexible Payment Options:** Choose from various payment methods, including Razorpay, wallet, and Cash on Delivery.
- **Automated Invoicing:** Enjoy transparency in transactions with automatic invoice generation.
- **Exclusive Coupons:** Unlock discounts and special offers with promotional coupons.
- **Password Management:** Forgot your password or want to make a change? User-friendly options for seamless account control.

## Admin Empowerment:

- **Intuitive Dashboard:** Comprehensive insights at a glance, empowering quick and informed decision-making.
- **Sales Analytics:** Dive deep into sales performance with detailed analytics and customizable date filters.
- **Downloadable Sales Reports:** Effortlessly download detailed sales reports in Excel format for in-depth analysis.
- **Streamlined Order Management:** Efficiently track and manage orders for a streamlined fulfillment process.
- **Product and User Control:** Enjoy effortless control over products and user accounts for optimal administration.
- **Coupon Mastery:** Fine-tune promotions with comprehensive control over coupon generation and management.
- **Dynamic Banner Changes:** Keep your storefront fresh with the ability to dynamically change banners for strategic promotions.
- **Real-Time User-to-Admin Chat:** Experience instant communication with users through ASGI Daphne WebSocket.

## Cutting-Edge Tech Stack:

- **Django Backend:** Powering our platform with the reliability and scalability of the Django framework.
- **Sleek Frontend Design:** Crafted using HTML, CSS, and Bootstrap for a visually stunning and responsive user interface.
- **Dynamic User Experience:** Implementing Ajax & JQuery for a dynamic and responsive user journey.
- **Reliable Database Management:** Leveraging the efficiency of PostgreSQL for seamless data management.
- **Scalable Deployment with Docker:** Ensuring scalability and ease of deployment using Docker.
- **Secure Hosting on AWS EC2:** Hosted securely and reliably on AWS EC2 for a worry-free experience.
- **Real-Time Chat with Django Channels and ASGI Daphne:** Offering a real-time, interactive experience with our users.



# Get Started:

## Procedure to Run SHOE CART Locally:

### 1. Clone the Repository:

```bash
git clone https://github.com/asifxohd/SHOECART.git
cd SHOECART

# On Windows
python -m venv venv
venv\Scripts\activate

# On Unix or MacOS
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt


Configure Database:
Ensure you have PostgreSQL installed.

Create a new database for SHOE CART.

Update the database configurations in SHOECART/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5. Create .env file:
Create a file named .env in the project root and add the following:

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=d
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
RAZORPAY_API_KEY=
RAZORPAY_API_SECRET_KEY=




