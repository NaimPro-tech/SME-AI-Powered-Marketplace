import { Request, Response, NextFunction } from 'express';
import { authService } from './auth.service';

export const register = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await authService.register(req.body);
    res.status(201).json({ success: true, data: user });
  } catch (e) { next(e); }
};

export const login = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const result = await authService.login(req.body.email, req.body.password);
    res.json({ success: true, data: result });
  } catch (e) { next(e); }
};

export const refresh = (_req: Request, res: Response) => {
  res.json({ message: 'refresh — coming soon' });
};

export const logout = (_req: Request, res: Response) => {
  res.json({ success: true, message: 'Logged out' });
};
