# SME Smart Marketplace

বাংলাদেশের ক্ষুদ্র উদ্যোক্তাদের জন্য AI-powered Digital Marketplace

## Architecture: Modular Monolith

```
sme-marketplace/
├── apps/
│   ├── api/          → Express.js Backend (Port 4000)
│   └── web/          → Next.js Frontend (Port 3000)
└── packages/
    ├── database/     → Prisma + PostgreSQL
    ├── shared/       → Types, Constants, Validators
    └── ui/           → Shared React Components
```

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Setup environment
cp .env.example .env
# .env ফাইলে DATABASE_URL ও JWT_SECRET দাও

# 3. Database setup
npm run db:migrate

# 4. Start development
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | নতুন অ্যাকাউন্ট |
| POST | /api/v1/auth/login | লগইন |
| GET | /api/v1/products | সব পণ্য দেখো |
| POST | /api/v1/products | পণ্য যোগ করো (Seller) |
| POST | /api/v1/orders | অর্ডার দাও (Buyer) |
| GET | /api/v1/dashboard/seller | Seller Dashboard |

## Roadmap

- [x] Phase 1: Core Marketplace (MVP)
- [ ] Phase 2: Analytics Dashboard
- [ ] Phase 3: AI/ML Layer (Sales Prediction)
- [ ] Phase 4: Mobile App
