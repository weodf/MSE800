# User Account Management System — Design Document

A simple user account management system that supports user registration, login, profile management, and forgot password functionality.

The system is designed to be maintainable, scalable, and easy to read by separating responsibilities into frontend pages, backend modules, shared helpers, and database tables.

---

## 1. System Architecture

```mermaid
graph TB
    subgraph FE["Frontend"]
        RegisterPage[Register Page]
        LoginPage[Login Page]
        ProfilePage[Profile Page]
        ForgotPage[Forgot Password Page]
        ResetPage[Reset Password Page]
    end

    subgraph BE["Backend Application"]
        AuthModule[Auth Module<br/>Register / Login / Logout]
        UserModule[User Module<br/>Profile Management]
        PasswordModule[Password Reset Module<br/>Forgot / Reset Password]
        Validation[Validation Layer]
        Security[Security Layer<br/>JWT / Session]
    end

    subgraph DB["Database"]
        Users[(Users Table)]
        ResetTokens[(Password Reset Tokens Table)]
    end

    RegisterPage --> AuthModule
    LoginPage --> AuthModule
    ProfilePage --> UserModule
    ForgotPage --> PasswordModule
    ResetPage --> PasswordModule

    AuthModule --> Validation
    UserModule --> Validation
    PasswordModule --> Validation

    AuthModule --> Security
    UserModule --> Security
    PasswordModule --> Security

    AuthModule --> Users
    UserModule --> Users
    PasswordModule --> Users
    PasswordModule --> ResetTokens
```

---

## 2. Module Breakdown

```mermaid
graph LR
    subgraph Auth["Auth Module"]
        A1[Register User]
        A2[Login User]
        A3[Logout User]
        A4[Issue Token or Session]
    end

    subgraph User["User Module"]
        U1[View Profile]
        U2[Update Full Name]
        U3[Update Date of Birth]
        U4[Protect User Data]
    end

    subgraph Password["Password Reset Module"]
        P1[Request Password Reset]
        P2[Generate Reset Token]
        P3[Validate Reset Token]
        P4[Update New Password]
    end

    subgraph Shared["Shared Helpers"]
        S1[Validate Input]
        S2[Hash Password]
        S3[Check Email Format]
        S4[Handle Errors]
        S5[Access Database]
    end

    Auth --> Shared
    User --> Shared
    Password --> Shared
```

---

## 3. Call Graph

```mermaid
graph TD
    main((Application Entry))

    subgraph AuthModule["Auth Module"]
        register((register_user))
        login((login_user))
        logout((logout_user))
    end

    subgraph UserModule["User Module"]
        profile((get_profile))
        updateProfile((update_profile))
    end

    subgraph PasswordModule["Password Reset Module"]
        forgot((forgot_password))
        reset((reset_password))
    end

    subgraph Helpers["Shared Helper Functions"]
        validate((validate_input))
        hash((hash_password))
        compare((compare_password))
        token((generate_reset_token))
        verifyToken((verify_reset_token))
        db[(database_access)]
    end

    main --> register
    main --> login
    main --> logout
    main --> profile
    main --> updateProfile
    main --> forgot
    main --> reset

    register --> validate
    register --> hash
    register --> db

    login --> validate
    login --> compare
    login --> db

    logout --> db

    profile --> db

    updateProfile --> validate
    updateProfile --> db

    forgot --> validate
    forgot --> token
    forgot --> db

    reset --> verifyToken
    reset --> hash
    reset --> db
```

---

## 4. Registration and Login Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as Backend API
    participant DB as Database

    Note over U,DB: User Registration

    U->>FE: Enter full name, date of birth, email, password
    FE->>API: Submit registration request
    API->>API: Validate input
    API->>DB: Check if email already exists

    alt Email already exists
        API-->>FE: Return error message
        FE-->>U: Show registration error
    else Email available
        API->>API: Hash password
        API->>DB: Save new user
        API-->>FE: Registration successful
        FE-->>U: Redirect to login page
    end

    Note over U,DB: User Login

    U->>FE: Enter email and password
    FE->>API: Submit login request
    API->>DB: Find user by email
    API->>API: Compare password with stored hash

    alt Valid credentials
        API-->>FE: Return token or session
        FE-->>U: Redirect to profile page
    else Invalid credentials
        API-->>FE: Return login error
        FE-->>U: Show invalid email or password
    end
```

---

## 5. Forgot Password Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as Backend API
    participant DB as Database
    participant Mail as Email Service

    U->>FE: Click "Forgot Password"
    U->>FE: Enter registered email
    FE->>API: Submit forgot password request

    API->>DB: Check if email exists

    alt Email not found
        API-->>FE: Return generic response
        FE-->>U: Show message
    else Email exists
        API->>API: Generate reset token
        API->>DB: Save token and expiry time
        API->>Mail: Send password reset link
        Mail-->>U: Receive reset email
    end

    U->>FE: Open reset link
    U->>FE: Enter new password
    FE->>API: Submit new password and reset token

    API->>DB: Validate reset token and expiry time

    alt Token valid
        API->>API: Hash new password
        API->>DB: Update password
        API->>DB: Mark token as used
        API-->>FE: Password reset successful
        FE-->>U: Redirect to login page
    else Token invalid or expired
        API-->>FE: Return reset error
        FE-->>U: Ask user to request a new reset link
    end
```

---

## 6. Profile Management Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as Backend API
    participant DB as Database

    U->>FE: Open profile page
    FE->>API: Request current user profile
    API->>API: Verify authentication token
    API->>DB: Query user profile
    DB-->>API: Return full name, date of birth, email
    API-->>FE: Return profile data
    FE-->>U: Display profile information

    U->>FE: Edit full name or date of birth
    FE->>API: Submit profile update request
    API->>API: Validate input
    API->>DB: Update user profile
    API-->>FE: Return updated profile
    FE-->>U: Show update success message
```

---

## 7. Data Model

```mermaid
erDiagram
    USERS {
        int id PK
        string full_name
        date date_of_birth
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
    }

    PASSWORD_RESET_TOKENS {
        int id PK
        int user_id FK
        string token
        datetime expires_at
        boolean used
        datetime created_at
    }

    USERS ||--o{ PASSWORD_RESET_TOKENS : has
```

---

## 8. Function Responsibilities

| Layer          | Function               | Responsibility                                                         |
| -------------- | ---------------------- | ---------------------------------------------------------------------- |
| Entry          | `main`                 | Application entry point and route registration                         |
| Auth           | `register_user`        | Register a new user with full name, date of birth, email, and password |
| Auth           | `login_user`           | Verify user credentials and create a login session or token            |
| Auth           | `logout_user`          | Clear user session or remove client-side token                         |
| User           | `get_profile`          | Retrieve the current user's personal information                       |
| User           | `update_profile`       | Update full name and date of birth                                     |
| Password Reset | `forgot_password`      | Generate a password reset token for a registered email                 |
| Password Reset | `reset_password`       | Validate token and update the user's password                          |
| Helper         | `validate_input`       | Validate form fields and prevent invalid data                          |
| Helper         | `hash_password`        | Hash passwords before storing them                                     |
| Helper         | `generate_reset_token` | Create a secure reset token                                            |
| Helper         | `database_access`      | Handle insert, update, and query operations                            |

---

## 9. Design Principles

### Maintainability

The system is divided into clear modules: Auth, User, Password Reset, Shared Helpers, and Database. Each module has a single responsibility, making the code easier to modify and debug.

### Scalability

The password reset logic is separated from the authentication logic. This allows future improvements such as email verification, two-factor authentication, or a separate notification service without changing the whole system structure.

### Readability

The project uses clear naming, simple module boundaries, and a small number of database tables. New developers can understand the system flow by reading the diagrams and function responsibility table.

---

## 10. GitHub Repository Requirement

The project should be uploaded to GitHub with a README file that includes:

* Project description
* Main features
* System architecture diagram
* Module breakdown diagram
* User flow diagrams
* Data model diagram
* Technology stack
* How to run the project
* API endpoint description

```
```
