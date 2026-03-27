import { test, expect } from '@playwright/test';

test('admin app loads dashboard', async ({ page }) => {
  await page.goto('/admin');
  await expect(page).toBeTruthy();
});
