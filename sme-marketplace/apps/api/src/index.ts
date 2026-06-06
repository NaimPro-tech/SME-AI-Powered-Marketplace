import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { config } from './shared/config/env';
import { errorHandler } from './shared/middleware/errorHandler';
import { authRouter } from './modules/auth/auth.router';
import { productRouter } from './modules/product/product.router';
import { orderRouter } from './modules/order/order.router';
import { userRouter } from './modules/user/user.router';
import { dashboardRouter } from './modules/dashboard/dashboard.router';

const app = express();

// ── Middleware
app.use(helmet());
app.use(cors({ origin: config.WEB_URL, credentials: true }));
app.use(express.json());

// ── Routes (Modular)
app.use('/api/v1/auth',      authRouter);
app.use('/api/v1/users',     userRouter);
app.use('/api/v1/products',  productRouter);
app.use('/api/v1/orders',    orderRouter);
app.use('/api/v1/dashboard', dashboardRouter);

// ── Health Check
app.get('/health', (_, res) => res.json({ status: 'ok', version: '1.0.0' }));

// ── Global Error Handler
app.use(errorHandler);

app.listen(config.PORT, () => {
  console.log(`🚀 API running on http://localhost:${config.PORT}`);
});

export default app;
