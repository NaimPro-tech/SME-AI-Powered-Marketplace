import { Response, NextFunction } from 'express';
import { AuthRequest } from '../../shared/middleware/authGuard';
import { orderService } from './order.service';

export const placeOrder = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const order = await orderService.place(req.user!.id, req.body);
    res.status(201).json({ success: true, data: order });
  } catch (e) { next(e); }
};

export const getMyOrders = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const orders = await orderService.getMyOrders(req.user!.id);
    res.json({ success: true, data: orders });
  } catch (e) { next(e); }
};

export const getOrderDetail = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const order = await orderService.getDetail(req.params.id, req.user!.id);
    res.json({ success: true, data: order });
  } catch (e) { next(e); }
};

export const updateOrderStatus = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const order = await orderService.updateStatus(req.params.id, req.body.status);
    res.json({ success: true, data: order });
  } catch (e) { next(e); }
};
