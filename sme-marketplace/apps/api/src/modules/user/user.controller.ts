import { Response, NextFunction } from 'express';
import { AuthRequest } from '../../shared/middleware/authGuard';
import { prisma } from '@sme/database';

export const getProfile = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const user = await prisma.user.findUnique({
      where: { id: req.user!.id },
      select: { id: true, name: true, email: true, role: true, phone: true, avatar: true,
                sellerProfile: true, buyerProfile: true }
    });
    res.json({ success: true, data: user });
  } catch (e) { next(e); }
};

export const updateProfile = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const user = await prisma.user.update({
      where: { id: req.user!.id },
      data: req.body,
      select: { id: true, name: true, email: true, phone: true, avatar: true }
    });
    res.json({ success: true, data: user });
  } catch (e) { next(e); }
};

export const createSellerProfile = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const slug = req.body.shopName.toLowerCase().replace(/ /g, '-') + '-' + Date.now();
    const profile = await prisma.sellerProfile.create({
      data: { userId: req.user!.id, shopSlug: slug, ...req.body }
    });
    res.status(201).json({ success: true, data: profile });
  } catch (e) { next(e); }
};
