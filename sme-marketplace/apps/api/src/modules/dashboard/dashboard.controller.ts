import { Response, NextFunction } from 'express';
import { AuthRequest } from '../../shared/middleware/authGuard';
import { prisma } from '@sme/database';

export const getSellerStats = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const seller = await prisma.sellerProfile.findUnique({ where: { userId: req.user!.id } });
    if (!seller) { res.status(404).json({ success: false, message: 'Seller profile not found' }); return; }

    const [totalProducts, totalOrders, recentOrders] = await Promise.all([
      prisma.product.count({ where: { sellerId: seller.id } }),
      prisma.orderItem.count({ where: { product: { sellerId: seller.id } } }),
      prisma.order.findMany({
        where: { items: { some: { product: { sellerId: seller.id } } } },
        take: 5,
        orderBy: { createdAt: 'desc' },
        include: { items: { include: { product: { select: { name: true } } } } }
      })
    ]);

    res.json({ success: true, data: { totalProducts, totalOrders, totalSales: seller.totalSales, recentOrders } });
  } catch (e) { next(e); }
};
