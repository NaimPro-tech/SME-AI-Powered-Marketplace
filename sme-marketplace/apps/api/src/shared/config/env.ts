import dotenv from 'dotenv';
dotenv.config();

export const config = {
  PORT:          process.env.PORT || 4000,
  DATABASE_URL:  process.env.DATABASE_URL!,
  JWT_SECRET:    process.env.JWT_SECRET!,
  JWT_EXPIRES:   process.env.JWT_EXPIRES_IN || '7d',
  WEB_URL:       process.env.WEB_URL || 'http://localhost:3000',
  CLOUDINARY: {
    cloud_name: process.env.CLOUDINARY_CLOUD_NAME!,
    api_key:    process.env.CLOUDINARY_API_KEY!,
    api_secret: process.env.CLOUDINARY_API_SECRET!,
  }
};
