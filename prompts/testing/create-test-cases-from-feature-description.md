{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ---\
title: Create test cases from a feature description\
tags: [testing, qa, developer-tools, test-cases]\
---\
\
## Task\
Given a short feature description, generate a set of structured test cases that cover the happy path, edge cases, and error handling. For each test case include **Title**, **Preconditions**, **Steps**, **Expected Result**, and **Priority**.\
\
## Constraints\
- Produce **10** test cases by default.  \
- Keep each test case concise (3\'966 lines).  \
- Use plain language suitable for QA engineers and developers.  \
- Assume a web application unless the feature description specifies otherwise.  \
- When relevant, include both UI and API checks.\
\
## Format\
- Return output as a numbered list of test cases.  \
- Each test case must follow this mini-template on one line per field:  \
  **Title:** \'85; **Preconditions:** \'85; **Steps:** \'85; **Expected Result:** \'85; **Priority:** (High/Medium/Low)\
\
## Example Input\
> Feature: Users can upload profile pictures up to 5MB; allowed formats: jpg, png; images are auto-resized to 400\'d7400; a thumbnail is generated; user sees a preview and a success message.\
\
## Example Output\
1. **Title:** Upload valid JPG under 5MB; **Preconditions:** User logged in; **Steps:** Navigate to profile \uc0\u8594  Upload a 3MB .jpg \u8594  Save; **Expected Result:** Image uploads, preview shows, image resized to 400\'d7400, success message displayed; **Priority:** High  \
2. **Title:** Reject unsupported format; **Preconditions:** User logged in; **Steps:** Upload a .gif file \uc0\u8594  Save; **Expected Result:** Upload blocked, error message "Unsupported format", no change to profile picture; **Priority:** High  \
3. **Title:** Reject oversized image; **Preconditions:** User logged in; **Steps:** Upload a 7MB .png \uc0\u8594  Save; **Expected Result:** Upload blocked, error message "File exceeds 5MB", no change to profile picture; **Priority:** High  \
4. **Title:** Verify thumbnail generation; **Preconditions:** Valid upload completed; **Steps:** Upload valid image \uc0\u8594  Save \u8594  Inspect thumbnails endpoint/UI; **Expected Result:** Thumbnail exists and dimensions are smaller than 400\'d7400; **Priority:** Medium  \
5. **Title:** Preserve aspect ratio when resizing; **Preconditions:** User logged in; **Steps:** Upload a 2000\'d7500 image \uc0\u8594  Save; **Expected Result:** Image resized to 400\'d7100 (aspect ratio preserved) or centered/cropped per spec; **Priority:** Medium  \
6. **Title:** Network interruption during upload; **Preconditions:** User logged in; **Steps:** Start upload then simulate network drop; **Expected Result:** Upload fails gracefully, retry option shown, no partial image saved; **Priority:** Medium  \
7. **Title:** Upload via mobile browser; **Preconditions:** Mobile user agent; **Steps:** Upload valid .png from mobile \uc0\u8594  Save; **Expected Result:** Upload succeeds, preview displays correctly, image resized; **Priority:** Low  \
8. **Title:** Concurrent uploads from two tabs; **Preconditions:** User logged in in two tabs; **Steps:** Upload different images simultaneously in both tabs; **Expected Result:** Last successful save wins; no data corruption; **Priority:** Low  \
9. **Title:** Invalid image file disguised as jpg; **Preconditions:** User logged in; **Steps:** Upload a renamed .exe with .jpg extension \uc0\u8594  Save; **Expected Result:** Server-side validation rejects file, error message shown; **Priority:** High  \
10. **Title:** Verify audit/log entry on upload; **Preconditions:** Valid upload completed; **Steps:** Upload image \uc0\u8594  Save \u8594  Check audit logs; **Expected Result:** Log entry created with user id, filename, size, timestamp; **Priority:** Medium\
\
## Expected Output\
- **Comprehensive coverage**: Includes happy path, edge cases, and error scenarios.  \
- **Actionable steps**: Each test case has clear steps and verifiable expected results.  \
- **Prioritization**: Each case is labeled High/Medium/Low to guide test planning.  \
- **Concise and consistent format**: Easy to paste into test management tools.\
\
## Rationale\
This prompt helps developers and QA quickly convert feature descriptions into executable test cases, speeding up validation and reducing miscommunication between product, engineering, and QA.}