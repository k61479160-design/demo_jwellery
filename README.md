# Raivat - Jewelry E-Commerce Platform

## 📋 Project Overview
**Raivat (Raivat Stones)** is a sophisticated **Django-based jewelry e-commerce platform** specializing in stone and jewelry sales. This enterprise-level application features advanced user authentication, payment integration, email notifications, and comprehensive product management.

## 🛠️ Technology Stack
- **Backend Framework**: Django (Python)
- **Database**: SQLite3 (Development) / PostgreSQL-ready
- **Payment Gateway**: Razorpay Integration
- **Email Service**: Gmail SMTP
- **Static Files**: WhiteNoise with compression
- **Security**: Advanced middleware and encryption
- **Data Management**: CSV data import/export

## ✨ Key Features

### 1. **Advanced Authentication System**
- Email-based OTP verification
- Password reset via OTP
- Session management with 24-hour expiry
- Custom authentication enforcement middleware
- Secure login/logout functionality

### 2. **E-Commerce Functionality**
- Product catalog with categories
- Shopping cart
- Order management
- Payment processing with Razorpay
- Invoice generation
- Order tracking

### 3. **Location-Based Services**
- Country, state, and city database
- Location-based shipping
- Geographic data management (13.2M+ cities data)

### 4. **Payment Integration**
- Razorpay payment gateway integration
- Secure payment processing
- Order confirmation
- Payment verification
- Transaction history

### 5. **Email Communication System**
- Automated OTP emails
- Password reset notifications
- Order confirmations
- Custom email templates
- Priority email handling

### 6. **Security Features**
- HSTS (HTTP Strict Transport Security)
- XSS filtering
- CSRF protection
- Content type nosniff
- Frame options protection
- Secure session cookies
- Custom security context processors

## 📁 Project Structure
```
Raivat-main/
├── Raivat/                # Project configuration
│   ├── settings.py       # Django settings with security configs
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── jewelry/             # Main application
│   ├── models.py       # Database models
│   ├── views.py        # Business logic
│   ├── middleware.py   # Custom middleware
│   └── static/         # Static assets
├── media/               # Product images
├── staticfiles/         # Collected static files
├── venv/                # Virtual environment
├── db.sqlite3          # SQLite database (274KB)
├── cities.csv          # Cities database (13.2MB)
├── countries.csv       # Countries database (97KB)
├── states.csv          # States database (364KB)
├── country_state_city_full.json  # Complete location data (3.2MB)
├── data.py             # Data import scripts
├── full_backup.json    # Database backup
├── requirements.txt    # Python dependencies
└── manage.py           # Django management script
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Navigate to project directory**
   ```bash
   cd Raivat-main/Raivat-main
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables setup**
   Create a `.env` file with:
   ```
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=127.0.0.1,localhost
   DEBUG=True
   
   # Database (optional, defaults to SQLite)
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   
   # Razorpay Credentials
   RAZORPAY_KEY_ID=your-razorpay-key-id
   RAZORPAY_KEY_SECRET=your-razorpay-secret
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Import location data (optional)**
   ```bash
   python data.py
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Website: http://127.0.0.1:8000
    - Admin: http://127.0.0.1:8000/admin

## � Output Screenshots

Explore the visual interface of the Raivat platform:

| | |
|---|---|
| ![Screen 1](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/1.png) | ![Screen 2](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/2.png) |
| ![Screen 3](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/3.png) | ![Screen 4](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/4.png) |
| ![Screen 5](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/5.png) | ![Screen 6](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/6.png) |
| ![Screen 7](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/7.png) | ![Screen 8](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/8.png) |
| ![Screen 9](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/9.png) | ![Screen 10](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/10.png) |
| ![Screen 11](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/11.png) | ![Screen 12](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/12.png) |
| ![Screen 13](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/13.png) | ![Screen 14](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/14.png) |
| ![Screen 15](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/15.png) | ![Screen 16](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/16.png) |
| ![Screen 17](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/17.png) | ![Screen 18](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/18.png) |
| ![Screen 19](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/19.png) | ![Screen 20](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/20.png) |
| ![Screen 21](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/21.png) | ![Screen 22](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/22.png) |
| ![Screen 23](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/23.png) | ![Screen 24](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/24.png) |
| ![Screen 25](https://raw.githubusercontent.com/Henilshingala/Output-images/master/raivat/25.png) | |

---
*Reference for Output Images:* [Henilshingala/Output-images](https://github.com/Henilshingala/Output-images/tree/master/raivat)

## �📦 Dependencies (requirements.txt)

```txt
Django==4.x or higher
python-dotenv
razorpay
Pillow (for image handling)
whitenoise (for static files)
```

## 🔐 Security Configuration

### Email Security
- **Email Host**: smtp.gmail.com
- **Port**: 587 (TLS)
- **Email**: info.raivatstones@gmail.com
- Custom email headers for tracking and spam prevention

### Payment Security
- Razorpay live credentials configured
- Secure payment webhook handling
- Transaction verification

### Session Security
- 24-hour session expiry
- HTTP-only cookies
- SameSite='Lax' protection
- Session save on every request

### SSL/HTTPS Settings
- HSTS: 1-year max-age
- Subdomain inclusion
- HSTS preload ready
- Browser XSS filter enabled

## 💳 Payment Integration

### Razorpay Setup
The application uses Razorpay for payment processing:
- **Key ID**: Configured in settings
- **Key Secret**: Stored securely
- **Payment modes**: Cards, UPI, Wallets, Net Banking
- **Currency**: INR

### Payment Flow
1. Customer adds items to cart
2. Proceeds to checkout
3. Razorpay payment gateway opens
4. Payment processed
5. Order confirmed via email
6. Order tracked in admin panel

## 📧 Email System

### Email Configuration
- **Backend**: Django SMTP
- **Provider**: Gmail
- **Features**:
  - OTP for registration/password reset
  - Order confirmations
  - Password reset emails
  - Custom templates

### Email Features
- 10-minute OTP expiry
- High-priority email headers
- Auto-response suppression
- Unsubscribe support
- Abuse reporting mechanism

## 🗄️ Database Features

### Location Data
Comprehensive location database:
- **Countries**: 97KB data, worldwide
- **States**: 364KB data, all regions
- **Cities**: 13.2MB data, 100,000+ cities

### Models Include
- User authentication
- Product catalog
- Categories
- Orders and order items
- Shopping cart
- Customer profiles
- OTP tokens
- Payment transactions

## 📊 Features in Detail

### Customer Features
- User registration with email verification
- OTP-based authentication
- Product browsing and search
- Shopping cart management
- Secure checkout
- Order history
- Profile management
- Password reset

### Admin Features
- Product management (CRUD operations)
- Category management
- Order processing
- Customer management
- Payment tracking
- Inventory management
- Sales analytics

### Middleware Components
1. **Authentication Enforcement**: Ensures proper authentication flow
2. **Security Middleware**: Django security features
3. **Session Middleware**: User session handling
4. **CSRF Middleware**: Cross-site request forgery protection
5. **WhiteNoise Middleware**: Static file serving

## 🎨 Static Files Management

### WhiteNoise Configuration
- Compressed manifest static files storage
- Automatic compression (gzip, Brotli)
- Far-future caching headers
- Production-ready static serving

### Static Files Location
- Development: `jewelry/static/`
- Production: `staticfiles/`
- Media: `media/`

## 🔧 Configuration Details

### File Upload Settings
- Max upload size: 250MB per file
- Max memory size: 250MB
- File permissions: 0o644 (read-write for owner)

### Cache Settings
- Local memory cache
- Quick data retrieval
- Session caching

### Logging
- Console and file logging
- Log file: `django.log`
- INFO level logging
- Error tracking

## 🌐 Deployment Considerations

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS` with domain
- [ ] Change `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Update to PostgreSQL/MySQL
- [ ] Configure proper email credentials
- [ ] Set up SSL certificates
- [ ] Configure production Razorpay keys
- [ ] Set up proper backup system
- [ ] Configure CDN for static files

### Allowed Hosts (Production)
Currently configured for:
- `127.0.0.1`
- `localhost`
- `raivatstones.com`
- `www.raivatstones.com`

## 📈 Data Management

### CSV Import
Scripts available for importing:
- Country data
- State data
- City data
- Product catalogs

### Data Backup
- JSON backup file included
- Database migrations tracked
- Media files backed up separately

## 🎯 Use Cases

Perfect for:
- Jewelry e-commerce businesses
- Stone and gem retailers
- Precious metal dealers
- Custom jewelry designers
- B2C jewelry sales
- Location-specific jewelry delivery

## 🚨 Important Notes

### Security Warnings
- ⚠️ Change default email password in production
- ⚠️ Update Razorpay credentials
- ⚠️ Set strong SECRET_KEY
- ⚠️ Enable SECURE_SSL_REDIRECT in production
- ⚠️ Remove hard-coded credentials before public deployment

### Email Configuration
The current email password is exposed in settings.py. **MUST CHANGE** before production:
```python
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
```

## 📞 Contact Information
- **Email**: info.raivatstones@gmail.com
- **Domain**: raivatstones.com
- **Organization**: Raivat Stone

## 🔄 Development Workflow
1. Activate virtual environment
2. Make code changes
3. Run migrations if needed
4. Test locally
5. Collect static files
6. Deploy to production

## 💡 Additional Features

### Context Processors
- Security context for templates
- Global variables available in all templates

### Custom Commands
- Data import utilities
- Backup scripts
- Database management

---

**Business**: Jewelry & Stones E-Commerce
**Framework**: Django with advanced features
**Payment**: Razorpay Integration
**Status**: Production-ready with configuration updates needed

**⚠️ Security Notice**: Review and update all credentials, secret keys, and security settings before production deployment!
