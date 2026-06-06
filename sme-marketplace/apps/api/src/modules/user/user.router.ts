import { Router } from 'express';
import { authGuard } from '../../shared/middleware/authGuard';
import { getProfile, updateProfile, createSellerProfile } from './user.controller';

export const userRouter = Router();

userRouter.get('/me',            authGuard, getProfile);
userRouter.put('/me',            authGuard, updateProfile);
userRouter.post('/seller-setup', authGuard, createSellerProfile);
