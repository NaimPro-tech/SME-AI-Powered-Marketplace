import { Response, NextFunction } from 'express';
import { AuthRequest } from '../../shared/middleware/authGuard';
import { productService } from './product.service';

export const getProducts = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const data = await productService.getAll(req.query as any);
    res.json({ success: true, data });
  } catch (e) { next(e); }
};

export const getProduct = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const data = await productService.getById(req.params.id);
    res.json({ success: true, data });
  } catch (e) { next(e); }
};

export const createProduct = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const seller = await import('@sme/database').then(m => m.prisma.sellerProfile.findUnique({ where: { userId: req.user!.id } }));
    if (!seller) throw new Error('Seller profile not found');
    const data = await productService.create(seller.id, req.body);
    res.status(201).json({ success: true, data });
  } catch (e) { next(e); }
};

export const updateProduct = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const seller = await import('@sme/database').then(m => m.prisma.sellerProfile.findUnique({ where: { userId: req.user!.id } }));
    const data = await productService.update(req.params.id, seller!.id, req.body);
    res.json({ success: true, data });
  } catch (e) { next(e); }
};

export const deleteProduct = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const seller = await import('@sme/database').then(m => m.prisma.sellerProfile.findUnique({ where: { userId: req.user!.id } }));
    await productService.delete(req.params.id, seller!.id);
    res.json({ success: true, message: 'Product deleted' });
  } catch (e) { next(e); }
};
