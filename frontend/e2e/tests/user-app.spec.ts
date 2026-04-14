import { test, expect } from '@playwright/test';

test('user app loads home', async ({ page }) => {
  await page.goto('/user');
  await expect(page).toBeTruthy();
});
