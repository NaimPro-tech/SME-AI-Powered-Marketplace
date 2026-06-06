import { Router } from 'express';
import { authGuard, roleGuard } from '../../shared/middleware/authGuard';
import {
  getProducts, getProduct,
  createProduct, updateProduct, deleteProduct
} from './product.controller';

export const productRouter = Router();

// Public
productRouter.get('/',    getProducts);
productRouter.get('/:id', getProduct);

// Seller only
productRouter.post('/',      authGuard, roleGuard('SELLER'), createProduct);
productRouter.put('/:id',    authGuard, roleGuard('SELLER'), updateProduct);
productRouter.delete('/:id', authGuard, roleGuard('SELLER'), deleteProduct);
