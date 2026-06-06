import { Router } from 'express';
import { authGuard, roleGuard } from '../../shared/middleware/authGuard';
import { placeOrder, getMyOrders, getOrderDetail, updateOrderStatus } from './order.controller';

export const orderRouter = Router();

orderRouter.post('/',           authGuard, roleGuard('BUYER'),  placeOrder);
orderRouter.get('/my',          authGuard,                      getMyOrders);
orderRouter.get('/:id',         authGuard,                      getOrderDetail);
orderRouter.patch('/:id/status', authGuard, roleGuard('SELLER'), updateOrderStatus);
