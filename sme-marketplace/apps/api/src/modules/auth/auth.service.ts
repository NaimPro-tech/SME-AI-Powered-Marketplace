import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { prisma } from '@sme/database';
import { config } from '../../shared/config/env';
import { AppError } from '../../shared/middleware/errorHandler';

export const authService = {
  async register(data: { name: string; email: string; password: string; role: 'BUYER' | 'SELLER' }) {
    const exists = await prisma.user.findUnique({ where: { email: data.email } });
    if (exists) throw new AppError('Email already registered', 409);

    const hashed = await bcrypt.hash(data.password, 12);
    const user = await prisma.user.create({
      data: {
        name:     data.name,
        email:    data.email,
        password: hashed,
        role:     data.role,
      },
      select: { id: true, name: true, email: true, role: true }
    });
    return user;
  },

  async login(email: string, password: string) {
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) throw new AppError('Invalid credentials', 401);

    const valid = await bcrypt.compare(password, user.password);
    if (!valid) throw new AppError('Invalid credentials', 401);

    const token = jwt.sign(
      { id: user.id, role: user.role },
      config.JWT_SECRET,
      { expiresIn: config.JWT_EXPIRES }
    );
    return { token, user: { id: user.id, name: user.name, email: user.email, role: user.role } };
  }
};
