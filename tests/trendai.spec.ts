import { test, expect } from '@playwright/test';

test('TrendAI company site loads', async ({ page }) => {
  await page.goto('https://www.trendai.ca/', { waitUntil: 'domcontentloaded' });

  await expect(page).toHaveTitle(/TrendAI/i);
  await expect(
    page.getByText('Revolutionizing the fashion industry with AI analytics').first(),
  ).toBeVisible();
});