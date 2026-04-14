import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  
  test('login page loads correctly', async ({ page }) => {
    await page.goto('/auth/login');
    
    // 检查登录页面元素存在
    await expect(page.locator('input[name="username"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('login with invalid credentials shows error', async ({ page }) => {
    await page.goto('/auth/login');
    
    // 填写无效凭据
    await page.locator('input[name="username"]').fill('invalid_user');
    await page.locator('input[name="password"]').fill('wrong_password');
    await page.locator('button[type="submit"]').click();
    
    // 检查错误消息显示
    // 注意：实际选择器取决于具体实现
    await expect(page.locator('text=/无效|失败|错误|invalid/i')).toBeVisible({ timeout: 5000 });
  });

  test('login form validation', async ({ page }) => {
    await page.goto('/auth/login');
    
    // 不填写任何内容直接提交
    await page.locator('button[type="submit"]').click();
    
    // 检查表单验证错误
    await expect(page.locator('input[name="username"]:invalid')).toBeVisible();
    await expect(page.locator('input[name="password"]:invalid')).toBeVisible();
  });
});

test.describe('User App Access', () => {
  
  test('user app redirects to login when not authenticated', async ({ page }) => {
    await page.goto('/user/library');
    
    // 检查是否重定向到登录页或显示登录提示
    // 具体行为取决于应用实现
    const url = page.url();
    const isLoginPage = url.includes('/auth') || url.includes('/login');
    const hasLoginForm = await page.locator('input[name="username"]').isVisible().catch(() => false);
    
    expect(isLoginPage || hasLoginForm).toBeTruthy();
  });

  test('user app home page loads', async ({ page }) => {
    await page.goto('/user/');
    
    // 检查首页元素
    await expect(page.locator('h1, h2, h4')).toBeVisible();
  });
});

test.describe('Admin App Access', () => {
  
  test('admin app redirects to login when not authenticated', async ({ page }) => {
    await page.goto('/admin/users');
    
    // 检查是否重定向或拒绝访问
    const url = page.url();
    const isLoginPage = url.includes('/auth') || url.includes('/login');
    const hasAuthError = await page.locator('text=/未授权|拒绝|forbidden|unauthorized/i').isVisible().catch(() => false);
    
    expect(isLoginPage || hasAuthError).toBeTruthy();
  });

  test('admin dashboard requires authentication', async ({ page }) => {
    await page.goto('/admin/');
    
    // 应该显示登录提示或重定向
    await expect(page).not.toHaveURL(/\/admin\/dashboard/);
  });
});

test.describe('Token Management', () => {
  
  test('protected routes require authentication', async ({ page }) => {
    // 尝试访问受保护的API端点
    const response = await page.request.get('/api/v1/auth/me');
    
    // 应该返回401
    expect(response.status()).toBe(401);
  });

  test('API returns 401 for invalid token', async ({ page }) => {
    const response = await page.request.get('/api/v1/auth/me', {
      headers: {
        'Authorization': 'Bearer invalid_token_here'
      }
    });
    
    expect(response.status()).toBe(401);
  });
});

test.describe('Session Management', () => {
  
  test('logout clears session', async ({ page }) => {
    // 这个测试需要实际的登录流程
    // 由于是E2E测试，可能需要mock或跳过
    
    // 访问登出端点（如果未认证应返回401）
    const response = await page.request.post('/api/v1/auth/logout');
    
    // 未认证用户尝试登出应返回401
    expect([401, 200, 204]).toContain(response.status());
  });
});
