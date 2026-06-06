import { prisma } from '@sme/database';
import { AppError } from '../../shared/middleware/errorHandler';

export const orderService = {
  async place(buyerId: string, data: { items: { productId: string; quantity: number }[]; deliveryAddress: string; paymentMethod: string }) {
    // Calculate totals
    const products = await prisma.product.findMany({
      where: { id: { in: data.items.map(i => i.productId) } }
    });

    let subtotal = 0;
    const orderItems = data.items.map(item => {
      const product = products.find(p => p.id === item.productId);
      if (!product) throw new AppError(`Product not found: ${item.productId}`, 404);
      if (product.stock < item.quantity) throw new AppError(`Insufficient stock: ${product.name}`, 400);
      const unitPrice = Number(product.discountPrice || product.price);
      const totalPrice = unitPrice * item.quantity;
      subtotal += totalPrice;
      return { productId: item.productId, quantity: item.quantity, unitPrice, totalPrice };
    });

    const deliveryCharge = 60; // Fixed BDT 60 for MVP
    const total = subtotal + deliveryCharge;
    const orderNumber = `ORD-${Date.now()}`;

    const order = await prisma.order.create({
      data: {
        buyerId,
        orderNumber,
        deliveryAddress: data.deliveryAddress,
        paymentMethod: data.paymentMethod as any,
        subtotal,
        deliveryCharge,
        total,
        items: { create: orderItems }
      },
      include: { items: { include: { product: true } } }
    });

    return order;
  },

  async getMyOrders(buyerId: string) {
    return prisma.order.findMany({
      where: { buyerId },
      include: { items: { include: { product: { select: { name: true, images: true } } } } },
      orderBy: { createdAt: 'desc' }
    });
  },

  async getDetail(id: string, userId: string) {
    const order = await prisma.order.findUnique({
      where: { id },
      include: { items: { include: { product: true } }, payment: true }
    });
    if (!order) throw new AppError('Order not found', 404);
    if (order.buyerId !== userId) throw new AppError('Forbidden', 403);
    return order;
  },

  async updateStatus(id: string, status: string) {
    return prisma.order.update({ where: { id }, data: { status: status as any } });
  }
};
