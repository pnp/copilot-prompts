import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test("filters, sorts, and restores shareable catalog state", async ({ page }) => {
  await page.goto("./");

  await page.locator("#search").fill("weekly");
  await page.locator("#type").selectOption("skills");
  await page.locator("#sort").selectOption("title");

  await expect(page).toHaveURL(/q=weekly.*type=skills.*sort=title/);
  await expect(page.locator(".component-card:visible")).not.toHaveCount(0);
  await page.reload();
  await expect(page.locator("#search")).toHaveValue("weekly");
  await expect(page.locator("#type")).toHaveValue("skills");

  await page.getByRole("button", { name: "Clear filters" }).click();
  await expect(page).toHaveURL(/\/copilot-prompts\/$/);
  await expect(page.locator("#search")).toBeFocused();
});

test("opens a sample from the catalog", async ({ page }) => {
  await page.goto("./");
  const firstSample = page.locator(".component-card").first();
  const title = await firstSample.getByRole("heading").innerText();

  await firstSample.getByRole("link", { name: /View details/ }).click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(title);
  await expect(page.getByRole("link", { name: "Download sample" })).toBeVisible();
  await expect(page.locator("[data-visitor-stats]")).toHaveAttribute(
    "src",
    /copilot-prompts\/samples\/(?:prompts|agent-instructions|skills)\//,
  );
});

test("tracks key gallery pages with page-specific images", async ({ page }) => {
  for (const path of ["./", "getting-started/", "contributors/", "contributing/"]) {
    await page.goto(path);
    await expect(page.locator("[data-visitor-stats]")).toHaveAttribute("src", /m365-visitor-stats\.azurewebsites\.net\/copilot-prompts/);
  }
});

test("presents the contributor Credly badge", async ({ page }) => {
  await page.goto("contributors/");
  const badge = page.getByRole("img", { name: /Prompt Pro .* contributor badge/ });
  await expect(badge).toBeVisible();
  await expect(badge).toHaveAttribute("src", /\/generated\/brand\/contributor-badge\.png$/);
  await expect(page.getByRole("heading", { name: "Earn the Prompt Pro Credly badge" })).toBeVisible();
  const avatarSources = await page.locator(".contributor-card img").evaluateAll((images) =>
    images.map((image) => image.getAttribute("src") ?? ""),
  );
  expect(avatarSources.every((source) =>
    source.startsWith("https://avatars.githubusercontent.com/") ||
    /^https:\/\/github\.com\/[^/]+\.png(?:\?size=144)?$/.test(source),
  )).toBe(true);
  await expect(page.getByRole("link", { name: /Credly badges work/ })).toHaveAttribute(
    "href",
    "https://aka.ms/community/recognition",
  );
});

test("persists the selected theme", async ({ page }) => {
  await page.goto("./");
  await page.getByRole("switch", { name: /Switch to .* mode/ }).click();
  const theme = await page.locator("html").getAttribute("data-theme");

  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", theme ?? "dark");
});

test("has no serious accessibility violations", async ({ page }) => {
  await page.goto("./");
  const samplePath = await page.locator(".component-card__footer a").first().getAttribute("href");
  expect(samplePath).not.toBeNull();
  for (const path of ["./", "getting-started/", "contributors/", "contributing/", samplePath!]) {
    await page.goto(path);
    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(results.violations.filter((violation) => ["serious", "critical"].includes(violation.impact ?? ""))).toEqual([]);
  }
});

test("does not overflow the viewport", async ({ page }) => {
  await page.goto("./");
  const dimensions = await page.evaluate(() => ({
    clientWidth: document.documentElement.clientWidth,
    scrollWidth: document.documentElement.scrollWidth,
  }));

  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth);
});

test("renders local brand and sample previews", async ({ page }) => {
  await page.goto("./");
  await expect(page.locator(".brand img")).toHaveJSProperty("complete", true);
  await expect(page.locator(".brand img")).not.toHaveJSProperty("naturalWidth", 0);

  const previews = page.locator(".component-card__media img");
  await previews.first().waitFor({ state: "visible" });
  await expect(previews.first()).not.toHaveJSProperty("naturalWidth", 0);
  await expect(previews.first()).toHaveAttribute("src", /\/copilot-prompts\/generated\/previews\//);
});
