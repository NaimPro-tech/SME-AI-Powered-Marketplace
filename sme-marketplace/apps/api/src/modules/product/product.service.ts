import { prisma } from '@sme/database';
import { AppError } from '../../shared/middleware/errorHandler';

export const productService = {
  async getAll(query: { category?: string; search?: string; page?: number; limit?: number }) {
    const page  = query.page  || 1;
    const limit = query.limit || 12;
    const skip  = (page - 1) * limit;

    const where: any = { status: 'ACTIVE' };
    if (query.category) where.category = { slug: query.category };
    if (query.search)   where.name = { contains: query.search, mode: 'insensitive' };

    const [products, total] = await Promise.all([
      prisma.product.findMany({
        where, skip, take: limit,
        include: { seller: { select: { shopName: true, shopSlug: true } }, category: true },
        orderBy: { createdAt: 'desc' }
      }),
      prisma.product.count({ where })
    ]);

    return { products, total, page, totalPages: Math.ceil(total / limit) };
  },

  async getById(id: string) {
    const product = await prisma.product.findUnique({
      where: { id },
      include: {
        seller: { select: { shopName: true, shopSlug: true, rating: true } },
        category: true,
        reviews: { include: { user: { select: { name: true, avatar: true } } }, take: 10 }
      }
    });
    if (!product) throw new AppError('Product not found', 404);
    return product;
  },

  async create(sellerId: string, data: any) {
    return prisma.product.create({
      data: { ...data, sellerId, slug: data.name.toLowerCase().replace(/ /g, '-') + '-' + Date.now() }
    });
  },

  async update(id: string, sellerId: string, data: any) {
    const product = await prisma.product.findFirst({ where: { id, sellerId } });
    if (!product) throw new AppError('Product not found or unauthorized', 404);
    return prisma.product.update({ where: { id }, data });
  },

  async delete(id: string, sellerId: string) {
    const product = await prisma.product.findFirst({ where: { id, sellerId } });
    if (!product) throw new AppError('Product not found or unauthorized', 404);
    await prisma.product.delete({ where: { id } });
  }
};
