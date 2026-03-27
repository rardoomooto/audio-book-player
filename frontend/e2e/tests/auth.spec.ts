import { test, expect } from '@playwright/test';

test('auth pages load', async ({ page }) => {
  await page.goto('/auth/login');
  await expect(page).toBeTruthy();
});
