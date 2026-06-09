# ISM-Blogs 📝

A modern, scalable blogging platform built with **FastAPI**, **PostgreSQL**, and **AWS S3**. Write, share, and discover blogs with an intuitive interface and robust backend infrastructure.

🌐 **Live Demo:** [https://ism-blogs.onrender.com](https://ism-blogs.onrender.com)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Key Features Explained](#-key-features-explained)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

---

## ✨ Features

### Core Features
- **User Authentication & Authorization**
  - Secure JWT-based authentication
  - Password hashing with Argon2
  - Email verification and password reset functionality
  - Token-based access control with configurable expiration

- **Blog Management**
  - Create, read, update, and delete blog posts
  - Rich text content support
  - Post timestamps and metadata
  - Pagination for efficient content delivery
  - Like/engagement tracking

- **User Profiles**
  - Customizable user profiles
  - Profile image uploads with optimization
  - User-specific blog management
  - View all posts by a specific user

- **Email Services**
  - Password reset notifications
  - Account verification emails
  - Integrated with Mailtrap for reliable email delivery

- **Image Storage & Optimization**
  - Automatic profile image processing
  - AWS S3 cloud storage
  - Image compression (JPEG format, 85% quality)
  - EXIF data handling and rotation correction
  - 300x300px optimized profile pictures

- **Database & Security**
  - PostgreSQL with async support
  - SQLAlchemy ORM with modern async/await patterns
  - Password hashing and secure token management
  - Database migrations with Alembic

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | ≥0.128.0 | Modern async web framework |
| **Python** | 3.9+ | Programming language |
| **SQLAlchemy** | ≥2.0.45 | ORM for database management |
| **Pydantic** | 2.x | Data validation & settings |
| **Alembic** | ≥1.18.4 | Database migrations |

### Database & Storage
| Technology | Version | Purpose |
|-----------|---------|---------|
| **PostgreSQL** | Latest | Primary relational database |
| **psycopg** | ≥3.3.3 | PostgreSQL async driver |
| **AWS S3** | (boto3) | Cloud image storage |
| **boto3** | ≥1.42.83 | AWS SDK for Python |

### Security & Authentication
| Technology | Version | Purpose |
|-----------|---------|---------|
| **PyJWT** | ≥2.10.1 | JWT token generation & validation |
| **pwdlib[argon2]** | ≥0.3.0 | Password hashing with Argon2 |
| **aiosmtplib** | ≥5.1.0 | Async email sending |

### Frontend
| Technology | Percent | Purpose |
|-----------|---------|---------|
| **HTML** | 50.4% | Page structure |
| **Python (Jinja2)** | 42.6% | Template rendering |
| **CSS** | 4.8% | Styling |
| **JavaScript** | 1.7% | Interactivity |
| **Mako** | 0.5% | Additional templating |

### Image Processing
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Pillow** | ≥12.1.1 | Image processing & optimization |

---

## 🏗️ Architecture

```
ISM-Blogs/
├── models.py           # SQLAlchemy ORM models (User, Post, PasswordResetToken)
├── schemas.py          # Pydantic request/response schemas
├── config.py           # Configuration management with Pydantic Settings
├── database.py         # Async database engine and session management
├── main.py             # FastAPI application and route handlers
├── image_utils.py      # S3 image upload/delete and processing
├── requirements.txt    # Python dependencies
├── routers/
│   ├── users.py       # User authentication and profile routes
│   └── posts.py       # Blog post CRUD routes
├── templates/         # Jinja2 HTML templates
├── static/            # CSS, JavaScript, and static assets
└── .env              # Environment variables (not tracked in git)
```

### Data Flow
```
User Request
    ↓
FastAPI Endpoint
    ↓
Pydantic Validation
    ↓
Database Query (SQLAlchemy)
    ↓
PostgreSQL
    ↓
Response (JSON/HTML)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL database
- AWS S3 bucket (for image storage)
- Mailtrap account (for email testing)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PrathamandX/ISM-Blogs.git
   cd ISM-Blogs
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (see [Configuration](#-configuration) section)
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   fastapi dev main.py
   # Or with uvicorn:
   uvicorn main:app --reload
   ```

   The application will be available at `http://localhost:8000`

---

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/ism_blogs

# JWT Settings
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS S3 Configuration
S3_BUCKET_NAME=your-bucket-name
S3_REGION=ap-southeast-2
S3_ACCESS_KEY_ID=your-aws-access-key
S3_SECRET_ACCESS_KEY=your-aws-secret-key
S3_ENDPOINT_URL=  # Leave empty for AWS, set for MinIO/LocalStack

# Email Configuration (Mailtrap)
MAIL_SERVER=live.smtp.mailtrap.io
MAIL_PORT=587
MAIL_USERNAME=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
MAIL_FROM=noreply@yourdomain.com
MAIL_US_TLS=true

# Application Settings
MAX_UPLOAD_SIZE_BYTES=5242880  # 5MB
POSTS_PER_PAGE=10
RESET_TOKEN_EXPIRE_MINUTES=60
FRONTEND_URL=http://localhost:8000
```

### Configuration Details

**Note:** All sensitive values (SECRET_KEY, AWS credentials, email passwords) are stored as `SecretStr` in Pydantic Settings for enhanced security.

---

## 🔐 Key Features Explained

### 1. **AWS S3 Image Storage**

Profile images are automatically processed and stored in AWS S3:

```python
# From image_utils.py
def process_profile_image(content: bytes) -> tuple[bytes, str]:
    # Open and validate image
    # Apply EXIF rotation correction
    # Resize to 300x300px using LANCZOS resampling
    # Convert RGBA to RGB if needed
    # Compress to JPEG with 85% quality
    # Generate unique UUID filename
    
async def upload_profile_image(file_bytes: bytes, filename: str) -> None:
    # Upload to S3 with proper metadata
    # Path: s3://bucket-name/profile_pics/{filename}
```

**Benefits:**
- Reduces server storage requirements
- Automatic CDN distribution via S3
- Scalable image storage
- Easy backup and disaster recovery

**Generated URL Format:**
```
https://{bucket-name}.s3.{region}.amazonaws.com/profile_pics/{filename}
```

### 2. **PostgreSQL Database**

Robust relational database with three main tables:

**Users Table**
```python
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash (Argon2 hashed)
- image_file (S3 filename reference)
- Relationships: posts, reset_tokens
```

**Posts Table**
```python
- id (Primary Key)
- title (Max 100 chars)
- content (Full text)
- user_id (Foreign Key → Users)
- date_posted (With UTC timezone)
- likes (Engagement counter)
- author (Relationship → User)
```

**PasswordResetToken Table**
```python
- id (Primary Key)
- user_id (Foreign Key → Users)
- token_hash (Unique, 64 chars)
- expires_at (Time-based expiration)
- created_at (Token creation time)
```

**Features:**
- Async query support with SQLAlchemy 2.0+
- Cascade delete for orphaned posts
- Indexed foreign keys for performance
- UTC timezone-aware timestamps
- Data integrity with constraints

### 3. **Mailtrap Email Service**

Secure email delivery for critical user communications:

**Implemented Features:**
- Password reset emails
- Account verification (ready for extension)
- Configured via environment variables
- Async SMTP with aiosmtplib
- Non-blocking email operations

**Configuration:**
```python
# From config.py
MAIL_SERVER = "live.smtp.mailtrap.io"  # Mailtrap inbox
MAIL_PORT = 587  # TLS port
MAIL_USERNAME = env("MAIL_USERNAME")
MAIL_PASSWORD = env("MAIL_PASSWORD")
MAIL_FROM = "noreply@yourdomain.com"
MAIL_US_TLS = True
```

**Usage Example:**
```python
# Send password reset email
await send_password_reset_email(
    user_email="user@example.com",
    reset_token="secure-token",
    frontend_url="https://ism-blogs.onrender.com"
)
```

### 4. **JWT Authentication**

Stateless, scalable authentication system:

**Token Flow:**
1. User logs in with credentials
2. Server validates password with Argon2
3. JWT token generated with user ID and expiration
4. Client stores token and includes in requests
5. Server validates token signature on each request

**Features:**
- HS256 algorithm
- 30-minute default expiration
- Configurable secret key
- Refresh token support (ready for implementation)
- Secure password hashing with Argon2

### 5. **Image Optimization Pipeline**

Automatic processing for user profile images:

1. **Upload:** Receive image file (max 5MB)
2. **Validation:** Check format and EXIF data
3. **Rotation:** Auto-correct based on EXIF orientation
4. **Resize:** Scale to 300x300px
5. **Conversion:** Convert RGBA → RGB if needed
6. **Compression:** JPEG 85% quality
7. **Storage:** Upload to S3 with unique UUID filename
8. **Cleanup:** Delete old image from S3 if updating

**Processing Code:**
```python
# Runs in thread pool to avoid blocking async operations
with Image.open(BytesIO(content)) as original:
    img = ImageOps.exif_transpose(original)  # Fix rotation
    img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)
    # ... JPEG compression and upload
```

---

## 📚 API Documentation

### Interactive Docs
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Core Endpoints

#### Authentication
```
POST   /api/users/register        - Create new user account
POST   /api/users/login           - Login and get JWT token
POST   /api/users/forgot-password - Request password reset
POST   /api/users/reset-password  - Reset password with token
```

#### User Management
```
GET    /api/users/me              - Get current user profile
PUT    /api/users/profile         - Update user profile
POST   /api/users/profile-picture - Upload profile image
GET    /api/users/{user_id}       - Get public user profile
```

#### Blog Posts
```
GET    /api/posts                 - List all posts (paginated)
POST   /api/posts                 - Create new post
GET    /api/posts/{post_id}       - Get post details
PUT    /api/posts/{post_id}       - Update post
DELETE /api/posts/{post_id}       - Delete post
GET    /users/{user_id}/posts     - Get user's posts
```

---

## 📁 Project Structure

```
ISM-Blogs/
├── main.py                 # FastAPI app initialization
├── models.py              # SQLAlchemy ORM models
├── schemas.py             # Pydantic validation schemas
├── config.py              # Environment configuration
├── database.py            # Database connection setup
├── image_utils.py         # S3 & image processing utilities
│
├── routers/
│   ├── users.py           # /api/users/* endpoints
│   └── posts.py           # /api/posts/* endpoints
│
├── templates/             # Jinja2 HTML templates
│   ├── home.html
│   ├── post.html
│   ├── base.html
│   └── ...
│
├── static/                # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── profile_pics/      # Default avatar
│
├── alembic/               # Database migration scripts
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
└── README.md             # This file
```

---

## 🌐 Deployment

### Render.com Deployment

The application is live on **Render.com**: [https://ism-blogs.onrender.com](https://ism-blogs.onrender.com)

#### Deployment Steps

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Connect to Render**
   - Go to [https://render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Select `PrathamandX/ISM-Blogs` repo

3. **Configure Environment**
   - Set all `.env` variables in Render dashboard
   - Use Render's PostgreSQL database
   - Set AWS credentials for S3

4. **Build & Deploy**
   - Build command: `pip install -r requirements.txt && alembic upgrade head`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`

#### Production Considerations

- Database URL: Use Render PostgreSQL connection string
- Email: Configure Mailtrap for transactional emails
- S3 Credentials: Add AWS IAM user with S3 permissions
- Frontend URL: Update to production domain
- Secret Key: Generate strong random key for production

---

## 🧪 Testing

### Manual API Testing
```bash
# Register user
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Login
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Create post (with token)
curl -X POST "http://localhost:8000/api/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Post","content":"This is amazing!"}'
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
# Commit with clear messages
git commit -m "Add feature: description"

# Push and create PR
git push origin feature/your-feature
```

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📧 Contact & Support

- **GitHub:** [@PrathamandX](https://github.com/PrathamandX)
- **Live Demo:** [https://ism-blogs.onrender.com](https://ism-blogs.onrender.com)

---

## 🙏 Acknowledgments

- FastAPI for the amazing async web framework
- PostgreSQL for reliable data storage
- AWS S3 for cloud image storage
- Mailtrap for email services
- Render.com for seamless deployment

---

**Happy Blogging! 🚀📝**
