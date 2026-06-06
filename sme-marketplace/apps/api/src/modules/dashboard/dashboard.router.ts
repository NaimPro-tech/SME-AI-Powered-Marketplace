import { Router } from 'express';
import { authGuard, roleGuard } from '../../shared/middleware/authGuard';
import { getSellerStats } from './dashboard.controller';

export const dashboardRouter = Router();

dashboardRouter.get('/seller', authGuard, roleGuard('SELLER'), getSellerStats);
