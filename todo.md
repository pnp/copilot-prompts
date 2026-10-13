# Copilot Prompts Gallery: Quality Audit and Delivery Plan

Audit date: 2026-09-02

Status: structural normalization completed on 2026-09-03; initial static gallery implemented and locally reviewed on 2026-10-13.

## Gallery implementation update (2026-10-13)

- [x] Synchronized the local checkout and VesaJuvonen fork with `pnp/copilot-prompts`.
- [x] Revalidated and normalized all 159 sample folders.
- [x] Added a deterministic Astro build that validates metadata and generates 159 detail pages, a searchable catalog, a sitemap, and public catalog JSON.
- [x] Added type, product, and contributor filters plus responsive cards and sanitized README detail pages.
- [x] Added a GitHub Pages build and deployment workflow for `/copilot-prompts/`.
- [x] Completed strict Astro diagnostics, static generation, dependency audit, and manual desktop/mobile browser review.

Remaining deployment steps:

1. Enable GitHub Pages with GitHub Actions as the source.
2. Verify the first live deployment, generated catalog, and outbound actions.
3. Add automated browser, accessibility, and outbound-link regression checks after launch.

## 0. Normalization update (2026-09-03)

Completed across all 153 sample folders:

- [x] Renamed every sample documentation file to exactly `README.md`.
- [x] Ensured every sample has one canonical `assets/sample.json` with the required publishing field names.
- [x] Moved the misplaced metadata for `m365-7-day-sent-review-and-remind-action` into `assets/sample.json`.
- [x] Added metadata for `m365-change-impacts` and `m365-copilot-as-a-professional-executive-assistant`.
- [x] Normalized sample IDs to `copilotprompts-prompt-{slug}`, `copilotprompts-agent-{slug}`, or `copilotprompts-skill-{slug}`.
- [x] Ensured each README ends with exactly one matching, taxonomy-aware visitor tracker under `https://m365-visitor-stats.azurewebsites.net/copilot-prompts/`.
- [x] Added gallery and README preview references for every sample.
- [x] Referenced the shared `images/ilovecopilot.png` fallback for the 27 samples without contributed images; no fallback binaries were copied into sample folders.
- [x] Added `scripts/normalize-samples.ps1` to check and repair these conventions for future contributions.

Validation completed:

- `./scripts/normalize-samples.ps1` is idempotent and validates all 153 folders.
- All 153 metadata files parse as one-item arrays and pass required publishing-content checks.
- All 153 taxonomy IDs are unique and match their README tracker.
- Every sample has exactly one canonical README and `assets/sample.json`.

### Website readiness snapshot

Current assessment: **content ingestion ready; website implementation and deployment not started**.

| Area | Status | Current evidence | What is still missing |
| --- | --- | --- | --- |
| Sample discovery and identity | Ready | 153 folders validate; all IDs are unique and type-aware | Keep the normalizer as a CI gate |
| README and metadata paths | Ready | Every sample has `README.md` and canonical `assets/sample.json` | Verify paths on Ubuntu in CI |
| Preview availability | Ready | 126 samples map to a local contributed image; 27 intentionally use the shared fallback; no primary preview is external | Require a sample-local static PNG for future contributions |
| Visitor tracking | Ready | Every sample has one `/copilot-prompts/` tracker matching its metadata ID | Add this invariant to CI |
| Required metadata content | Ready | All required scalar values, descriptions, products, authors, and image thumbnails pass the fresh audit | Add these checks to the repository-owned schema and CI |
| Metadata schema | Blocked | The PowerShell normalizer checks the current structural contract | Add a versioned JSON Schema and schema tests |
| Product/facet taxonomy | Deferred | Metadata contains 20 product labels; 142 samples have no facet entries | Do not normalize for the initial website; revisit only if advanced host/application/scenario filters are needed |
| Catalog generator | Not started | No `site/`, package manifest, or generation script exists | Implement deterministic scanning, validation, Markdown rendering, and image handling |
| Gallery interface | Not started | No frontend exists | Build catalog, filters, cards, detail pages, contributors, and guidance pages |
| Automated quality | Blocked | Existing workflow only calls `pnp/pnp-sample-validation@main` | Add local validation, unit, browser, accessibility, link, and image checks |
| GitHub Pages deployment | Not started | No Pages workflow or deployable artifact exists | Add build/deploy workflows and post-deployment verification |

### Launch blockers

The sample data is ready for website generation. The following repository and delivery work remains before the gallery is production-ready:

1. **Contract:** confirm the brand-asset decision and add canonical README/metadata templates for future contributions.
2. **Schema and CI:** add `.github/schemas/sample.schema.json`, run repository-owned validation on Ubuntu, add the normalizer in check mode to pull requests, and pin third-party actions to immutable commits.
3. **Static site:** create the Astro project and generate all 153 type/slug detail routes, the catalog, sitemap, and public catalog JSON.
4. **Experience:** implement search, type/contributor filters, sorting, sample cards, sanitized README detail pages, contributor pages, and source/download actions.
5. **Quality gates:** add unit, Playwright, accessibility, responsive layout, internal link, outbound action, and image-decoding tests.
6. **Deployment:** configure GitHub Pages for `/copilot-prompts`, deploy the tested artifact, and verify the live commit and catalog hash.

Items 1-2 are the pre-site creation milestone. Product normalization and advanced host/application/scenario filtering are explicitly deferred and do not block frontend implementation or launch. Public deployment should require all 153 records to pass the same build used in CI.

The original audit and remediation matrix below are retained as the baseline. Structural items fixed by this update are historical; product taxonomy is deferred, while unresolved content, schema-governance, and gallery-delivery items remain actionable.

## 1. Scope and audit method

This audit covers all immediate sample folders under:

- `samples/prompts/`
- `samples/agent-instructions/`
- `samples/skills/`

The audit intentionally does not judge the writing quality, factual quality, or runtime behavior of a prompt, agent instruction, or `SKILL.md`. It checks whether each contribution can be packaged, validated, and published consistently:

- required folder and core-file structure
- canonical `assets/sample.json` location and JSON shape
- required publishing metadata, identifiers, dates, URLs, products, and authors
- at least one local reference image
- at least one static PNG, as required by `CONTRIBUTING.md`
- a publishable image entry in `thumbnails` with a URL, alt text, and matching local file
- an image reference in the sample README

The repository's current contribution guidance and scaffolding skills were treated as the local contract. The proposed gallery-readiness profile is stricter than the existing external `pnp/pnp-sample-validation@main` workflow because it also verifies local image resolution, date ordering, normalized identifiers, and metadata needed to build deterministic pages.

## 2. Executive summary

| Measure | Baseline | Current | Status |
| --- | ---: | ---: | --- |
| Total samples | 153 | 153 | Stable |
| Prompt samples | 113 | 113 | Stable |
| Agent instruction samples | 31 | 31 | Stable |
| Skill samples | 9 | 9 | Stable |
| Samples passing structural normalization | 23 | 153 | Resolved |
| Samples requiring structural normalization | 130 | 0 | Resolved |
| Canonical `assets/sample.json` files | 150 | 153 | Resolved |
| Missing canonical `assets/sample.json` files | 3 | 0 | Resolved |
| Misplaced `sample.json` files | 1 | 0 | Resolved |

Current structural pass status by type:

| Type | Total | Pass | Needs work |
| --- | ---: | ---: | ---: |
| Prompts | 113 | 113 | 0 |
| Agent instructions | 31 | 31 | 0 |
| Skills | 9 | 9 | 0 |

All samples can now be discovered and loaded through the normalized folder and metadata contract. The fresh rescan found no remaining required metadata, identity, path, date, tracker, author, or preview-integrity defects. Taxonomy facets remain largely unpopulated by design because that work is deferred.

## 3. Quality findings

### 3.1 Systemic issues

| Finding | Baseline | Current | Status | Notes |
| --- | ---: | ---: | --- | --- |
| README filename is not exactly `README.md` | 86 | 0 | Resolved | Case-only renames are recorded in Git for Linux compatibility. |
| README does not reference an image | 43 | 0 | Resolved | READMEs use a contributed image or shared fallback. |
| No image thumbnail | 29 | 0 | Resolved | Every sample has at least one usable gallery preview. |
| No contributed image in the sample | 28 | 27 | Covered | These 27 intentionally use `images/ilovecopilot.png`; replacing it remains a quality improvement. |
| No sample-local static PNG | 46 | 45 | Accepted legacy | Existing local JPEG/GIF/WebP previews remain valid and image-less samples use the shared PNG. New contributions must include a sample-local static PNG. |
| Product taxonomy is inconsistent | 31 | 142 without gallery facets | Deferred | Keep current product labels for the initial website; revisit only if advanced filtering becomes a priority. |
| Metadata `name` mismatch | 14 | 0 | Resolved | All names use the prompt/agent/skill taxonomy. |
| Source `url` mismatch | 6 | 0 | Resolved | All source URLs match the owning folder. |
| Missing or incorrect `downloadUrl` | 6 | 0 | Resolved | All download actions now target the owning folder. |
| Skill product conflicts with current contract | 5 | 4 | Deferred | Keep current Cowork-oriented values unchanged for now. |
| Empty `shortDescription` | 4 | 0 | Resolved | Every card has a short description. |
| Empty `longDescription` | 2 | 0 | Resolved | Both descriptions were populated from their existing README summaries. |
| Update date precedes creation date | 3 | 0 | Resolved | Date ordering is normalized. |
| Canonical `assets/sample.json` is missing | 3 | 0 | Resolved | All 153 files exist in the canonical location. |
| `sample.json` root is not a one-item array | 2 | 0 | Resolved | All 153 roots are one-item arrays. |
| Required `metadata` field is missing | 2 | 0 | Resolved | All records contain the field; facet population remains open. |
| `source` is missing or not `pnp` | 2 | 0 | Resolved | All records use `pnp`. |
| Author entry is incomplete | 1 | 0 | Resolved | Corrected the author property in `agent-instructions/prompt-coach-supreme`. |
| Image thumbnail entry is incomplete | 1 | 0 | Resolved | Added alt text to the supplementary `prompt-coach-supreme` image. |
| Duplicate image thumbnail order | Not tracked | 0 | Resolved | Fresh rescan found and corrected two records with duplicate order `100`. |

Resolved canonical metadata files:

- `samples/prompts/m365-7-day-sent-review-and-remind-action/assets/sample.json`
- `samples/prompts/m365-change-impacts/assets/sample.json`
- `samples/prompts/m365-copilot-as-a-professional-executive-assistant/assets/sample.json`

Resolved misplaced file:

- `samples/prompts/m365-7-day-sent-review-and-remind-action/sample/sample.json`

### 3.2 Contract conflicts to resolve before enforcement

- [x] Standardize all sample documentation filenames and scaffolding guidance on `README.md`.
- [x] Establish `images/ilovecopilot.png` as the shared fallback rather than copying it into sample folders.
- [x] Allow supported sample-specific image formats for existing samples, use the shared fallback only when no image exists, and require a local static PNG for new contributions.
- Deferred: define a controlled product taxonomy and store host/application distinctions as metadata facets.
- Deferred: decide whether skills are cross-Copilot contributions and resolve the four Cowork-oriented product conflicts.
- [ ] Add the missing canonical README and `sample.json` templates referenced by contribution guidance.
- [ ] Pin `pnp/pnp-sample-validation` to an immutable commit and add a repository-owned schema/test command.

### 3.3 Issue code legend

The legend and matrix below are retained as the **2026-09-02 baseline audit**, not as the live status tracker. Use sections 2, 3.1, and the delivery phases for current status.

<details>
<summary>Archived baseline issue codes and per-sample remediation matrix</summary>

| Code | Required remediation |
| --- | --- |
| `README_CASE` | Rename `readme.md` or another case variant to exactly `README.md`, using a two-step rename where required on Windows. |
| `IMAGE_MISSING` | Add at least one representative local output/prompt screenshot under lowercase `assets/`. |
| `PNG_MISSING` | Add a static `.png` preview even when GIF/JPEG media already exists. |
| `README_IMAGE` | Reference a local sample image from `README.md`. |
| `ASSETS_MISSING` | Create or rename the folder to lowercase `assets/`. |
| `JSON_MISSING` | Add `assets/sample.json`; move and correct a misplaced file where one exists. |
| `JSON_ROOT` | Wrap the single metadata object in a one-item JSON array. |
| `FIELD_*` | Add the named required field. |
| `EMPTY_*` | Supply a non-empty value for the named field. |
| `NAME` | Set `name` to `copilotprompts-{prompt|agent|skill}-{exact-folder-name}`. |
| `SOURCE` | Set `source` to `pnp`. |
| `URL` | Point `url` to the exact GitHub sample folder. |
| `DOWNLOAD_URL` | Point `downloadUrl` to the partial-download URL for the exact sample folder. |
| `DATE_ORDER` | Make `updateDateTime` equal to or later than `creationDateTime`. |
| `LONG_DESCRIPTION` | Add at least one non-empty long-description paragraph. |
| `PRODUCT_TAXONOMY` | Replace or remap noncanonical product labels after the taxonomy decision. |
| `SKILL_PRODUCT` | Reconcile the skill's product with the final skill-host policy. |
| `AUTHOR` | Supply non-empty `gitHubAccount` and `name` values. |
| `THUMBNAIL` | Add an image thumbnail with type, order, raw URL, and descriptive alt text. |

### 3.4 Per-sample remediation matrix

Each unchecked row failed at least one gallery-readiness check. Samples not listed here passed this structural and publishing audit; that does not certify prompt or instruction content quality.

#### Prompt samples

- [ ] `prompts/github-adaptivecard-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/github-copilot-fix-code` - `README_CASE`, `NAME`
- [ ] `prompts/github-powerplatform-patchfunction` - `README_CASE`
- [ ] `prompts/github-powershell-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/hr-generate-job-description` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-7-day-inbox-review-action-framework` - `README_CASE`
- [ ] `prompts/m365-7-day-sent-review-and-remind-action` - `README_CASE`, `ASSETS_MISSING`, `IMAGE_MISSING`, `PNG_MISSING`, `JSON_MISSING`
- [ ] `prompts/m365-80s-legends` - `README_CASE`, `DATE_ORDER`
- [ ] `prompts/m365-action-plan-meeting-minutes-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-ai-automation-opportunity-finder` - `README_CASE`
- [ ] `prompts/m365-ai-code-review-feedback` - `README_CASE`
- [ ] `prompts/m365-annual-appraisal-data-generator-prompt` - `README_CASE`, `DATE_ORDER`
- [ ] `prompts/m365-asp-dot-net-core-mvc-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/m365-azure-devops-pipeline-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/m365-change-impacts` - `README_IMAGE`, `JSON_MISSING`
- [ ] `prompts/m365-company-party-planner` - `README_CASE`
- [ ] `prompts/m365-competitor-analysis-report` - `README_CASE`
- [ ] `prompts/m365-compliance-checklist` - `README_CASE`, `README_IMAGE`
- [ ] `prompts/m365-compliance-review-minutes-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-content-based-permission-recommendations` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-copilot-as-a-professional-executive-assistant` - `README_CASE`, `JSON_MISSING`
- [ ] `prompts/m365-copilot-as-an-excel-tutor` - `README_CASE`, `NAME`
- [ ] `prompts/m365-copilot-compare-proposals-on-defined-criteria` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-Copilot-LifeCoach` - `README_CASE`, `DATE_ORDER`
- [ ] `prompts/m365-copilot-software-request-tracker` - `README_CASE`, `NAME`, `URL`
- [ ] `prompts/m365-create-diagram-mermaid-prompt` - `README_CASE`, `PNG_MISSING`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-decision-log-generator-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-define-todays-actions` - `EMPTY_SHORTDESCRIPTION`
- [ ] `prompts/m365-detailed-agenda-for-upcoming-meeting-prompt` - `README_CASE`
- [ ] `prompts/m365-detect-hidden-automation-business` - `EMPTY_SHORTDESCRIPTION`, `LONG_DESCRIPTION`
- [ ] `prompts/m365-email-ranking` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `EMPTY_SHORTDESCRIPTION`, `LONG_DESCRIPTION`, `THUMBNAIL`
- [ ] `prompts/m365-email-sorting` - `README_IMAGE`, `URL`
- [ ] `prompts/m365-external-stakeholder-meeting-minutes-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-extract-unresolved-issues` - `README_CASE`
- [ ] `prompts/m365-find-emails-from-leaders-prompt` - `README_IMAGE`
- [ ] `prompts/m365-fluency-timing-coach-prompt` - `PNG_MISSING`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-generate-known-issue-article-from-support-ticket` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-generate-mermaid-diagram` - `README_CASE`
- [ ] `prompts/m365-generate-pbi-dashboard` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-generate-timesheet` - `README_CASE`, `PNG_MISSING`, `README_IMAGE`
- [ ] `prompts/m365-generate-wordcloud` - `README_CASE`
- [ ] `prompts/m365-generating-teams-meeting-description` - `README_IMAGE`, `NAME`
- [ ] `prompts/m365-geo-locator-prompt` - `README_CASE`, `PNG_MISSING`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-get-technical-interviews-for-past-months` - `README_CASE`, `NAME`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-information-format-pppp-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/m365-last-7-days-recap` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-latest-10-announcements-from-m365-message-center` - `NAME`
- [ ] `prompts/m365-located-unanswered-meeting-prompt` - `README_CASE`
- [ ] `prompts/m365-manage-pending-emails-conversations-prompt` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-meeting-action-items-prompt` - `README_CASE`
- [ ] `prompts/m365-meeting-details-invitee-list` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-meeting-list-invitees-rsvp` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-meeting-minutes-generator` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-multilanguage-quiz` - `README_CASE`, `JSON_ROOT`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-my-name-mentioned-prompt` - `README_CASE`
- [ ] `prompts/m365-office-script-compare-excel-files-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/m365-optimize-my-work-schedule` - `README_CASE`
- [ ] `prompts/m365-outlook-calendar-analytics` - `FIELD_DOWNLOADURL`, `EMPTY_DOWNLOADURL`, `URL`, `DOWNLOAD_URL`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-outlook-thread-summary` - `FIELD_DOWNLOADURL`, `EMPTY_DOWNLOADURL`, `DOWNLOAD_URL`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-planning-kickoff-meeting-minutes-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-post-meeting-summary-prompt` - `README_CASE`
- [ ] `prompts/m365-power-automate-debugger` - `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-prompt-architect` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-promptcoach-cowork-task-and-estimate` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-releasenotes-from-devops-email-markdown` - `README_CASE`, `README_IMAGE`, `NAME`
- [ ] `prompts/m365-researcher-ego-booster` - `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-risk-analysis` - `README_CASE`
- [ ] `prompts/m365-risk-analysis-meeting-minutes-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-sharepoint-content-search` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-sharepoint-SPFx-version-update-prompt` - `README_CASE`
- [ ] `prompts/m365-summarise-chat-group-prompt` - `README_CASE`
- [ ] `prompts/m365-summarise-email` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/m365-summarise-most-recent-discussion-in-well-format-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/m365-team-retrospective-minutes-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-teams-meeting-action-items` - `FIELD_SOURCE`, `FIELD_DOWNLOADURL`, `FIELD_LONGDESCRIPTION`, `SOURCE`, `EMPTY_DOWNLOADURL`, `URL`, `DOWNLOAD_URL`, `LONG_DESCRIPTION`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-teams-sprint-summary` - `FIELD_DOWNLOADURL`, `EMPTY_DOWNLOADURL`, `URL`, `DOWNLOAD_URL`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-tenant-compliance-and-security-summary-report` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `PRODUCT_TAXONOMY`, `THUMBNAIL`
- [ ] `prompts/m365-tic-tac-toe-game-prompt` - `README_CASE`, `PNG_MISSING`, `PRODUCT_TAXONOMY`
- [ ] `prompts/m365-time-finder-meeting-prerequisite-prompt` - `README_CASE`
- [ ] `prompts/m365-top10_bullet_points_in_document` - `README_CASE`
- [ ] `prompts/m365-training-workshop-summary-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `prompts/m365-understanding-mode` - `README_CASE`
- [ ] `prompts/m365-upcoming-meeting-prompt` - `README_IMAGE`
- [ ] `prompts/m365-upcoming-meetings-prompt` - `README_CASE`
- [ ] `prompts/m365-websearch-traveldestination-prompt` - `NAME`
- [ ] `prompts/m365-weekly-highlights-summary` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/m365-work-productivity-and-distractions-check` - `NAME`, `EMPTY_SHORTDESCRIPTION`
- [ ] `prompts/m365-wrapup-day-tomo-planner` - `PNG_MISSING`
- [ ] `prompts/m365-yearly-performance-review-prompt` - `README_CASE`
- [ ] `prompts/ppt-sales-report-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/ppt-welcome-slide-prompt` - `README_CASE`, `PNG_MISSING`
- [ ] `prompts/vscode-daily-usage-summary-prompt` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `NAME`, `THUMBNAIL`
- [ ] `prompts/wellness-influencer-content-creator` - `README_CASE`, `PNG_MISSING`, `PRODUCT_TAXONOMY`
- [ ] `prompts/whiteboard-intranet-ideation-prompt` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/word-sales-proposal-with-file-reference-prompt` - `README_CASE`, `PRODUCT_TAXONOMY`
- [ ] `prompts/word-write-prompt-guidance-best-practices-prompt` - `README_CASE`, `PRODUCT_TAXONOMY`

#### Agent instruction samples

- [ ] `agent-instructions/childrens-book-recommender` - `README_IMAGE`
- [ ] `agent-instructions/communication-assistant` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/conference-session-summarizer` - `README_CASE`
- [ ] `agent-instructions/creator-agent` - `README_CASE`
- [ ] `agent-instructions/customer-comments-agent` - `README_CASE`
- [ ] `agent-instructions/daily-chore-children` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/elevator-pitch-alchemist` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/executive-orchestrator` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/finance-agent` - `FIELD_METADATA`
- [ ] `agent-instructions/learning-path-architect` - `README_CASE`
- [ ] `agent-instructions/m365-dental-care-advisor` - `NAME`, `PRODUCT_TAXONOMY`
- [ ] `agent-instructions/mental-health-first-aider-agent` - `README_CASE`
- [ ] `agent-instructions/peace-keeper-agent` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/prompt-assistance` - `README_CASE`, `README_IMAGE`, `NAME`, `URL`, `DOWNLOAD_URL`
- [ ] `agent-instructions/prompt-coach-supreme` - `JSON_ROOT`, `FIELD_DOWNLOADURL`, `EMPTY_DOWNLOADURL`, `DOWNLOAD_URL`, `PRODUCT_TAXONOMY`, `AUTHOR`, `THUMBNAIL`
- [ ] `agent-instructions/scrum-master-product-owner` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/smart-crop-doctor` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/smart-meal-planner-agent` - `README_IMAGE`
- [ ] `agent-instructions/socratic-tutor` - `README_CASE`, `README_IMAGE`, `NAME`
- [ ] `agent-instructions/soulspace-agent` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/specific-research-agent` - `README_CASE`, `NAME`
- [ ] `agent-instructions/sprint-governance-agent` - `README_IMAGE`, `FIELD_METADATA`
- [ ] `agent-instructions/strategic-mind-agent` - `README_CASE`
- [ ] `agent-instructions/vendor-intake-approval-agent` - `README_CASE`, `README_IMAGE`
- [ ] `agent-instructions/warhol-emoji-factory` - `README_CASE`, `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `agent-instructions/women-in-tech-spotlight` - `README_IMAGE`

#### Skill samples

- [ ] `skills/api-docs-generator` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `skills/code-review-csharp` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `skills/copilot-studio-documenter` - `IMAGE_MISSING`, `PNG_MISSING`, `README_IMAGE`, `THUMBNAIL`
- [ ] `skills/powerapps-canvas-yaml-generator` - `PRODUCT_TAXONOMY`, `SKILL_PRODUCT`
- [ ] `skills/prompt-context-engineer` - `PRODUCT_TAXONOMY`, `SKILL_PRODUCT`
- [ ] `skills/prompt-of-the-week` - `SOURCE`, `PRODUCT_TAXONOMY`, `SKILL_PRODUCT`
- [ ] `skills/self-awareness-review` - `SKILL_PRODUCT`
- [ ] `skills/weekly-pacing` - `PRODUCT_TAXONOMY`, `SKILL_PRODUCT`

</details>

## 4. Sister site analysis

Reference implementation: `https://github.com/pnp/spfx-copilot-components` and `https://pnp.github.io/spfx-copilot-components/`.

### 4.1 Architecture worth reusing

The sister gallery is a static Astro site under `site/` with a repository-aware generation step:

1. A Node script scans sample folders and reads each `assets/sample.json` and `README.md`.
2. AJV validates metadata against a repository-owned JSON Schema.
3. The generator normalizes catalog records, resolves local thumbnail files, checks date order, and sanitizes rendered Markdown.
4. Sharp creates optimized 640 px and 960 px WebP card/detail previews.
5. Astro generates the catalog, one detail page per sample, getting-started, contributor, and contributing pages.
6. A public `catalog.json` is emitted for integrations.
7. Vitest covers catalog normalization; Playwright covers filtering, routing, responsive behavior, and accessibility with Axe.
8. Separate GitHub Actions workflows validate pull requests and deploy the static `site/dist` artifact to GitHub Pages.
9. Deployment verification uses a commit marker and catalog hash so a successful Pages job proves that the expected commit is live.

Important behavior to preserve:

- catalog-first home page with visible sample count
- search without navigation or page reload
- contributor and product filtering
- deterministic sorting by update date and title
- cards with real preview, title, short description, author, version/context metadata, and updated date
- static detail routes with source and download actions
- sanitized README rendering and link rewriting
- additional gallery images on detail pages
- contributor directory and contribution guidance pages
- dark mode, skip link, responsive navigation, canonical/OG metadata, sitemap, and accessibility tests
- no runtime API or database dependency

### 4.2 Changes needed for this repository

> **Deferred for the initial website:** the proposed `copilotHost`, `applications`, and `scenario` taxonomy below is design reference only and is not a launch requirement.

The sister repository has a single sample collection. This repository has three types and possible duplicate slugs, so identity and routing must use both type and slug:

- `/samples/prompts/{slug}/`
- `/samples/agent-instructions/{slug}/`
- `/samples/skills/{slug}/`

The generated record should add:

- `sampleType`: `Prompt`, `Agent instruction`, or `Skill`, derived from the parent folder
- `copilotHost`: normalized host such as `Microsoft 365 Copilot`, `Microsoft Copilot`, or `GitHub Copilot`
- `applications`: optional values such as Outlook, Teams, Word, PowerPoint, Whiteboard, Power Apps, or VS Code
- `scenario`: a controlled category such as Productivity, Meetings, Communications, Development, HR, Learning, Governance, or Creative
- `readmeHtml`: sanitized documentation for the detail page
- `searchText`: title, descriptions, type, host, applications, scenario, and author names

Do not infer long-term taxonomy from folder prefixes or arbitrary product strings at render time. Store controlled values in `sample.json.metadata`, validate them, and normalize only documented legacy aliases during migration.

### 4.3 Branding direction

Working product name: **Copilot Prompt Gallery**.

Positioning: community-built prompts, agent definitions, and reusable skills for the Copilot family.

Visual direction:

- Keep the Microsoft 365 & Power Platform Community family association through the sister site's Copilot PNG, spectrum header treatment, and `side-bg-left.webp` / `side-bg-right.webp` catalog backgrounds.
- Copy reusable assets into this repository instead of hotlinking them. Record original repository path, source commit, license, and intended use in `site/public/images/ASSET-PROVENANCE.md`.
- Confirm that Microsoft/Copilot marks may be reused for this context before publication. Product marks identify the product family; they must not imply Microsoft endorsement of individual community samples.
- Create a distinct prompt-centered identity through typography and composition: compact conversation/prompt syntax motifs, three clearly differentiated type markers, and a catalog headline focused on reusable instructions rather than SPFx components.
- Use a balanced neutral canvas with the family spectrum as an accent. Avoid turning each type into an unrelated mini-brand.
- Use real sample screenshots as the dominant card imagery. Do not use generic generated art as a substitute for missing contribution evidence.

Suggested first viewport:

- brand: Copilot Prompt Gallery
- descriptor: Prompts, agent instructions, and skills
- concise statement: Community patterns for getting more from Microsoft 365 Copilot, Microsoft Copilot, and GitHub Copilot
- live counts for all samples and each contribution type
- immediately visible catalog controls and the first row of samples

## 5. Proposed content and information architecture

### Primary navigation

- Gallery
- Getting started
- Contributors
- Contributing
- GitHub

### Catalog controls

Initial launch scope includes search, type, contributor, and sort controls. Copilot host, application, and scenario filters are deferred with the taxonomy work.

- Search
- Type segmented control: All, Prompts, Agent instructions, Skills
- Contributor filter
- Sort: Recently updated, Newest, Title
- Clear-all control and visible result count

Filters should be represented in the query string so searches can be shared and browser navigation works. Controls must be keyboard accessible and should update results without layout jumps.

### Card content

- local optimized preview image
- sample-type marker
- title
- short description with a consistent line limit
- Copilot host and optional application labels
- contributor name/avatar
- updated date
- entire semantic title/media link plus a clear detail action

### Detail page

- breadcrumb back to the filtered catalog when possible
- title, type, host/application/scenario metadata, author, and dates
- primary real screenshot with optional additional media gallery
- `View source` and `Download sample` actions
- long description
- sanitized README documentation
- references and contributor links
- related samples based on type, host, and scenario as a later enhancement

Do not extract and expose a one-click `Copy prompt` feature until prompt/agent bodies have a reliable structured source. README headings and fenced blocks are inconsistent and are not a safe data contract. A future optional `contentFile` or typed metadata field can enable that feature without brittle Markdown scraping.

## 6. Target repository structure

```text
.github/
  schemas/
    sample.schema.json
  workflows/
    validate-gallery.yml
    deploy-gallery.yml
site/
  package.json
  package-lock.json
  astro.config.mjs
  playwright.config.ts
  scripts/
    generate-gallery.mjs
    gallery-model.mjs
    deployment-verification.mjs
  public/
    images/
      copilot.png
      side-bg-left.webp
      side-bg-right.webp
      ASSET-PROVENANCE.md
  src/
    components/
      SampleCard.astro
      CatalogFilters.astro
    generated/
      catalog.json
    layouts/
      BaseLayout.astro
    lib/
      catalog.ts
    pages/
      index.astro
      getting-started.astro
      contributors.astro
      contributing.astro
      samples/[type]/[slug].astro
    styles/
      global.css
  tests/
    unit/
    e2e/
templates/
  README-prompt-template.md
  README-agent-instruction-template.md
  README-skill-template.md
  sample-template.json
```

Generated files and previews must be reproducible and either rebuilt in CI or explicitly ignored; do not hand-edit them.

## 7. Metadata contract proposal

> **Deferred for the initial website:** controlled taxonomy facets may be added later without blocking the baseline catalog.

Keep the established one-item array and existing Solution Gallery fields for compatibility. Add controlled facets through the existing `metadata` array.

Required top-level fields:

- `name`, `source`, `title`, `shortDescription`
- `url`, `downloadUrl`
- non-empty `longDescription`
- `creationDateTime`, `updateDateTime` in `YYYY-MM-DD`, with update not earlier than creation
- non-empty `products`
- `metadata`
- one or more image `thumbnails`
- one or more complete `authors`
- `references`

Required metadata entries for this gallery:

```json
"metadata": [
  { "key": "SAMPLE-TYPE", "value": "Prompt" },
  { "key": "COPILOT-HOST", "value": "Microsoft 365 Copilot" },
  { "key": "SCENARIO", "value": "Meetings" },
  { "key": "APPLICATIONS", "value": "Teams, Outlook" }
]
```

Rules:

- `SAMPLE-TYPE` is derived from the folder during validation and must match the declared value.
- `COPILOT-HOST` uses a controlled allowlist; multiple hosts require an agreed delimiter or an array-capable schema extension.
- `SCENARIO` uses one primary controlled category in phase 1.
- `APPLICATIONS` is optional and must not be overloaded into `products`.
- Every thumbnail image needs unique `order`, a descriptive `alt`, a raw GitHub URL for the owning file, and a matching decodable local image.
- The lowest-order image is the card and social preview.
- New contributions must provide at least one sample-local static PNG. Existing samples may retain another supported local image format, and existing image-less samples use the shared PNG fallback.
- `name`, `url`, and `downloadUrl` are validated against the actual type and folder, not only against regular-expression shapes.
- Author GitHub accounts are compared case-insensitively for contributor aggregation.

## 8. Delivery phases and acceptance gates

### Phase 0: Agree the contract

- [x] Resolve README casing and establish the shared fallback preview policy.
- [x] Accept existing supported image formats while requiring a sample-local static PNG for future contributions.
- Deferred: resolve agent product naming and the Cowork skill policy.
- Deferred: approve the host, application, and scenario taxonomies.
- [ ] Decide whether all legacy samples must pass before first public deployment or whether a dated, visible migration status is acceptable.
- [ ] Confirm legal/brand reuse of the sister site's background and Copilot assets.

Gate: one written schema and contribution contract has no conflicting instructions.

### Phase 1: Add repository-owned validation

- [ ] Add `.github/schemas/sample.schema.json` with conditional rules where practical.
- [ ] Add a Node validator that scans all three sample roots and checks identity, URLs, date order, local files, image decoding/dimensions, thumbnail order, alt text, and README image references.
- [ ] Emit both human-readable errors and a JSON audit artifact.
- [ ] Add unit tests for valid documents, malformed roots, path traversal, encoded filenames, and duplicate slugs across types.
- [ ] Pin third-party actions to immutable commit SHAs.
- [ ] Run validation on pull requests and prevent new debt immediately.

Gate: the validator reproduces this audit and gives contributors exact file-level remediation messages.

### Phase 2: Repair P0 publication blockers

- [x] Add or move the three missing canonical metadata files.
- [x] Fix the two non-array documents.
- [x] Add all missing required metadata fields and non-empty short descriptions.
- [x] Add non-empty long descriptions to `m365-detect-hidden-automation-business` and `m365-email-ranking`.
- [x] Correct source/download URLs and metadata names.
- [x] Add a publishable thumbnail for every sample, using the shared fallback where needed.
- [x] Complete the legacy image thumbnail entry in `agent-instructions/prompt-coach-supreme`.
- [x] Correct the incomplete author metadata in `agent-instructions/prompt-coach-supreme`.
- [x] Resolve duplicate thumbnail order values in `m365-copilot-compare-proposals-on-defined-criteria` and `m365-latest-10-announcements-from-m365-message-center`.

Gate: complete. All 153 samples pass required publishing-content checks and can be discovered and parsed without exclusions.

### Phase 3: Normalize assets and documentation

- [x] Rename all case-variant READMEs to `README.md` and record the case-only renames in Git.
- [x] Provide a preview for every sample through a contributed image or the shared repository fallback.
- [x] Map all 126 samples with contributed media to sample-specific primary previews, including the 18 legacy samples without PNG files.
- Optional improvement: replace the shared fallback in the 27 image-less legacy samples when maintainers provide representative screenshots.
- [x] Reference a contributed image or the shared fallback in every README.
- [x] Normalize primary thumbnail URLs to sample-local images or the shared fallback.
- [x] Resolve incomplete legacy thumbnail entries and validate unique order values and alt text.
- [ ] Add canonical README and metadata templates.
- [x] Update all three scaffolding skills to produce taxonomy-aware IDs and `/copilot-prompts/` trackers.
- [x] Update `CONTRIBUTING.md` with README casing, fallback preview, identity, and tracker rules.
- [ ] Update the repository `README.md` with gallery build and local-development instructions after the site exists.

Gate: every sample meets the baseline structure and image requirements on Windows and Linux.

### Phase 4: Build the gallery foundation

- [ ] Scaffold `site/` with Astro, sitemap, Sharp, AJV, marked, sanitize-html, Vitest, Playwright, and Axe.
- [ ] Set Astro `site` to `https://pnp.github.io`, `base` to `/copilot-prompts`, and trailing slashes consistently.
- [ ] Port the sister site's safe link rewriting, Markdown sanitization, image optimization, catalog generation, and deployment marker patterns.
- [ ] Adapt scanning to three roots and composite type/slug routes.
- [ ] Generate private build data and a public `catalog.json` without sanitized README HTML/search internals.

Gate: a deterministic production build creates 153 detail pages, optimized previews, sitemap, catalog JSON, and no broken internal links.

### Phase 5: Build the branded experience

- [ ] Implement the family header/background assets with documented provenance.
- [ ] Implement the distinct Copilot Prompt Gallery identity and type markers.
- [ ] Build catalog search, type/contributor filters, sorting, result count, and empty state.
- Deferred: add host/application/scenario filters after a controlled taxonomy is approved.
- [ ] Build sample cards, type-aware details, media galleries, source/download actions, and README rendering.
- [ ] Build getting-started, contributors, and contributing pages.
- [ ] Add canonical, Open Graph, Twitter card, favicon, sitemap, and structured metadata.
- [ ] Support light/dark themes without sacrificing sample-image legibility.

Gate: the first screen is the usable gallery, works at mobile and desktop widths, and visibly belongs to the same community family without looking like the SPFx catalog renamed.

### Phase 6: Test and deploy

- [ ] Unit-test schema normalization, routing, link rewriting, preview selection, and contributor aggregation.
- [ ] Browser-test search/filter query strings, sorting, detail navigation, back navigation, keyboard operation, mobile navigation, theme persistence, and zero-result recovery.
- [ ] Run Axe checks on catalog, detail, contributors, and contributing pages.
- [ ] Check image decoding and nonblank previews across representative desktop/mobile viewports.
- [ ] Enforce no horizontal overflow, no overlapping controls, and readable long titles.
- [ ] Add Pages validation and deployment workflows with least-privilege permissions, concurrency control, artifacts, environment URL, and post-deploy commit/hash verification.
- [ ] Add a pull-request summary with sample count, page count, excluded count, preview count, and artifact size.

Gate: validation, production build, browser tests, accessibility checks, and post-deployment verification all pass for the same commit.

### Phase 7: Operate and improve

- [ ] Add dependency update automation and a documented Node version.
- [ ] Track gallery schema versions and provide migrations rather than permanent aliases.
- [ ] Publish a machine-readable quality status without exposing contributor-sensitive internals.
- [ ] Measure broken outbound links and stale metadata on a schedule.
- [ ] Consider related samples, favorites, copy-prompt actions, and richer scenario collections only after the baseline catalog is reliable.

Gate: a new compliant sample is validated, indexed, previewed, and deployed without hand-editing site code.

## 9. Recommended sequencing

1. Resolve the screenshot wording and brand decisions in Phase 0; taxonomy and Cowork policy remain deferred.
2. Add the JSON Schema, repository-owned validator tests, and pull-request CI while retaining `scripts/normalize-samples.ps1` as the repair command.
3. Add canonical README and metadata templates that match the schema and updated scaffolders.
4. Scaffold the Astro site and deterministic catalog generator against all 153 normalized samples without requiring taxonomy facets.
5. Build and browser-test the catalog and detail experience, then add the least-privilege Pages deployment workflow.
6. Make schema validity, 153 generated detail pages, zero excluded records, accessibility, and post-deployment verification production launch gates.

This sequencing keeps the gallery generator honest: contribution quality is the source of truth, and the site is a deterministic presentation of that source rather than a second hand-maintained catalog.