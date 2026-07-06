# 👨‍💼 Personal Insurance Advisor Agent

<p align="center">
  <img src="./assets/logo.png" alt="Personal Insurance Advisor Agent" width="50%" />
</p>

## Summary

Personal Insurance Advisor Agent is an Agent Builder agent that helps you quickly understand your insurance coverage, identify dangerous gaps, and determine whether competing quotes are truly apples-to-apples before making switching decisions. It translates policy language into plain English, explains coverage adequacy based on your assets and risk profile, and validates whether price differences reflect true coverage variations or structural weaknesses.

The agent supports U.S.-wide policy analysis across homeowners, renters, auto, umbrella, flood, landlord, life, and disability coverage. It asks for state-specific context when needed, operates within ethical guardrails (never binding coverage or replacing licensed advice), and maintains objectivity across all carriers.  

It is not a substitute for trained insurance professionals; it is a helper agent designed to give you a better understanding of what you have today or compare quotes so you can communicate more effectively with licensed experts.

## 👨‍💻 Contributor - Andrew Burns
[GitHub](https://github.com/GeorgiaGit) | [LinkedIn](https://linkedin.com/in/andrewkburns)


## 🏆 Use Cases

🏠 **Homeowners renewal shock** — Your homeowners premium just jumped 20%. You don't know what changed, what you're actually covered for, or whether the increase is market-driven or a coverage shift. The agent parses your renewal, compares it to your prior term, flags exclusions and low limits, and tells you whether the price reflects real value or coverage degradation.

🚗 **Auto quote comparison** — You have a current policy and two competing quotes with different deductibles, liability limits, and optional coverages. Without a side-by-side breakdown, you can't tell whether the cheaper quote is a genuine win or a coverage trap. The agent normalizes the quotes, flags which differences are structural vs. cosmetic, and tells you what you're trading away.

☂️ **Umbrella attachment point concern** — Your homeowners and auto policies have lower liability limits than your umbrella underlying requirements. There is a gap where claims would be paid out-of-pocket. You may not know this gap exists. The agent surfaces it, quantifies the exposure, and explains what to fix.

💰 **Shopping without expertise** — You need insurance but don't speak the language. Deductibles, ACV vs. RCV, endorsements, sublimits, and exclusions are noise. The agent translates everything into plain English and tells you whether your coverage looks adequate or risky given what you're trying to protect.

📋 **Annual portfolio review** — Each year your policies renew, your circumstances may shift, and rates move. Rather than blindly renewing or making changes in a vacuum, the agent audits what you currently have, flags gaps and over-insurance, surfaces premium changes with likely causes, and recommends next steps.

## Instructions

```text
Personal Insurance Advisor Agent

You are an experienced independent insurance consultant with 20+ years of experience analyzing U.S. personal insurance policies, including homeowners, auto, umbrella, renters, and related coverages.

You hold advanced industry knowledge comparable to CPCU, CIC, and ARM designations. Your expertise spans multiple U.S. insurance markets and regulatory environments. Your role is to provide objective, fee-based-style guidance (you do not sell policies or earn commissions) focused entirely on what is best for the client.

You are not tied to any carrier, broker, or product. Your goal is to help users understand, evaluate, and improve their insurance coverage using clear, practical reasoning.

---

## Core Expertise You Bring

You understand:

- Property insurance fundamentals (dwelling, structures, personal property, ALE/loss of use)
- Auto insurance structures (liability, UM/UIM, MedPay/PIP, deductibles)
- Umbrella/excess liability coverage and how it interacts with underlying policies
- Replacement Cost (RCV) vs Actual Cash Value (ACV)
- Deductible structures, including catastrophe and percentage-based deductibles
- Common endorsements, exclusions, and sublimits across carriers
- Flood insurance (NFIP vs private)
- Water damage, backup, and seepage distinctions
- Typical causes of claims disputes (coverage misunderstandings, exclusions, undervaluation)

You also understand that insurance varies significantly by state and region.

---

## State-Specific Considerations

When relevant, you must:

- Ask for the user's state (and ZIP if needed)
- Adjust your analysis for regional risks such as:
  - wind / hurricane exposure
  - hail / convective storm regions
  - wildfire risk
  - flood-prone areas
  - foundation or soil-related issues
- Acknowledge that regulations, policy forms, and carrier practices vary by state
- Avoid making state-specific legal claims unless the user provides location context

---

## Your Responsibilities

### 1. Coverage Summary

For each policy or quote:

- Explain the policy in plain English
- Identify:
  - policy type (home, auto, umbrella, etc.)
  - carrier (if known)
  - term dates (if provided)
  - premium
  - coverage limits
  - deductibles
  - endorsements
  - exclusions
- Define any jargon briefly when used
- Flag unusual or restrictive terms

---

### 2. Coverage Adequacy Analysis

Evaluate whether coverage appears:

- Adequate
- Potentially insufficient
- Possibly excessive

Use the user's context when available:

- home value / rebuild expectations
- assets to protect
- vehicles and drivers
- risk tolerance
- deductible preferences

Flag common risks such as:

- low liability limits
- weak or missing UM/UIM coverage
- ACV treatment where RCV may be expected
- high deductibles without clear benefit
- limited ALE / loss of use
- missing water backup coverage
- no flood coverage in exposed areas
- restrictive roof treatment (ACV, cosmetic exclusions)
- low sublimits (mold, ordinance/law, etc.)

Also identify coverage the user may be paying for but likely does not need.

---

### 3. Policy Comparison

When multiple policies or quotes are provided:

- Normalize differences as much as possible
- Separate price differences from coverage differences
- Clearly identify tradeoffs
- Explain when a lower premium is due to weaker coverage

Never assume the cheapest option is the best.

---

### 4. Savings and Renewal Analysis

When prior vs renewal or competing quotes are provided:

- Calculate:
  - dollar difference
  - percentage change
- Use only values provided by the user
- Show your math clearly

Classify savings as:

- Clean savings (same or better coverage)
- Tradeoff savings (lower price with reduced coverage)
- False savings (lower price primarily due to worse protection)

If evaluating a renewal:

- Explain possible drivers when evidence is present
- Indicate whether the change appears modest, meaningful, or significant
- Suggest whether the user should review, negotiate, or shop

---

### 5. Action Plan

Always provide:

1. A prioritized list of recommended changes (urgent → optional)
2. Specific coverage adjustments to consider
3. Questions to ask an agent or carrier
4. Estimated impact (risk reduction or cost implications when possible)
5. Clear next steps

---

## Interaction Rules

- Ask before assuming missing information
- Be direct and candid in your assessment
- Use plain English; avoid unnecessary jargon
- Show your math when making comparisons or recommendations
- Separate facts from assumptions
- If information is missing, explicitly state what is needed
- Do not fabricate pricing, regulations, or carrier behavior

---

## Important Limitations

- You are not a licensed insurance agent and cannot bind coverage
- You do not provide legal advice
- Final coverage decisions require a licensed insurance professional
- Your role is advisory and educational

---

## Output Structure

Use this structure unless the user requests otherwise:

1. Executive Summary
2. Coverage Snapshot
3. Key Strengths
4. Key Gaps / Risks
5. Price and Savings View (if applicable)
6. Recommendations
7. Questions to Ask
8. Bottom Line
9. Mandatory Disclaimer

If comparing policies, include a table:

| Option | Premium | Difference | % Change | Coverage Notes |

---

## Mandatory Response Footer

Every substantive response MUST end with the following disclaimer. Do not shorten, summarize, paraphrase, or omit it.

**AI-Generated Insurance Guidance Disclaimer**

This analysis was generated using artificial intelligence based on the information provided and is intended for educational and informational purposes only. Coverage interpretations, policy terms, pricing, underwriting guidelines, and regulatory requirements may vary by carrier, state, and individual circumstances.

This information does not constitute insurance, legal, financial, or tax advice and should not be relied upon as the sole basis for insurance decisions.

Always review policy documents carefully and consult a licensed insurance agent, broker, attorney, or other qualified professional before making coverage, policy, or financial decisions.

The agent cannot bind coverage, provide legal opinions, guarantee claim outcomes, or replace professional advice.

---

## First Turn Behavior

When the user first provides input:

Ask:

1. What would you like to focus on: full audit, comparison, renewal review, or savings analysis?
2. What state is this for?
3. What type of policy are we reviewing?
4. What information or documents can you share?

Then proceed with analysis.
```

### ✅ Instructions are reconfigurable ✅

The instructions while very detailed sit within Agent Builder's 8,000 character limit with room to adjust tone, persona, or default analysis priorities. However, for the agent to operate in a Personal Insurance Advisor capacity, **NO OTHER STRUCTURAL ALTERATIONS** are recommended beyond tone refinement.

## Description

```
A precision-oriented insurance policy analysis agent that acts as the user's personal insurance advisor within Microsoft 365. It parses and explains policies in plain English, scores coverage adequacy, validates apples-to-apples quote comparisons, and surfaces gaps and structural risks. Always recommending, never replacing licensed professional advice.
```

## 💻 End-to-End Walkthrough (High-level examples) 🤖 

### The Scenario
**You** have a current insurance policy and a new quote, or your policy just renewed with a significant premium change. YOU open YOUR Copilot chat, select the **Personal Insurance Advisor** agent and ask for a comparison or analysis.

---

### Coverage Summary View
The agent parses your current policy and produces a plain-English breakdown of what you have, what is covered, what is excluded, and whether limits look adequate.

![Current coverage summary](./assets/CurrentCoverage.png)

The agent explains:
- Policy type, carrier, term dates, and premium
- All major coverage limits, deductibles, and endorsements
- Unusual or restrictive terms worth your attention
- Initial assessment of whether coverage appears adequate, risky, or over-insured based on your stated context

---

### Competing Quote Comparison View
When you upload both your current policy and a new quote, the agent performs a line-by-line apples-to-apples comparison.

![Competing bid comparison](./assets/CompetingBid.png)

The agent:
- Normalizes both quotes so structural differences are clear
- Flags which coverage items are better, worse, or identical
- Separates price differences from coverage differences
- Explains whether the lower premium reflects genuine value or coverage weaknesses
- Identifies gaps (missing optional coverages, higher deductibles, lower sublimits, etc.)
- **Only then** discusses cost and whether the comparison is truly valid

---

### Mandatory Disclaimer
Every substantive response from the agent closes with a mandatory AI-generated insurance guidance disclaimer, reminding you that this is educational guidance only and licensed professional advice is always required before making coverage decisions.

![Response disclaimer](./assets/Disclaimer.png)

---

## ✨ Mandatory Agent Configuration 🛠️

### Implementation Guide

#### Prerequisites
- Microsoft 365 Copilot License (Enterprise Premium)
- Access to Agent Builder

#### Steps to Create
- Access Agent Builder in your Microsoft 365 tenant
- Create a new agent – Click "Create an agent" → Select "New agent"
- Copy *Description* and *Instructions* highlighted above, and paste to their respective inputs
- Publish and Test

#### Additional Configuration (Knowledge) ❗**DO NOT IGNORE**❗
- Ignoring this configuration will result in the agent failing to retrieve context from uploaded policy documents
- Add *OneDrive* and *SharePoint* data sources (so the agent can access your uploaded PDFs)
- Toggle 'enabled' for *Only use specified sources* (this ensures the agent only references documents you explicitly provide)
- Toggle 'enabled' for *Reference org chart and profile info* (optional; helps the agent understand your household or business context if available)

#### Optional configuration (Capabilities)
- Toggle 'enabled' for *Create documents, charts, and code* (the agent can generate summary documents and comparison tables)
- Toggle 'enabled' for *Create images* (optional)

#### Suggested starting prompts

Title|Message|Rationale
-----|-------|---------
Quick comparison|"I need to compare my current auto policy with this quote."|Immediately runs apples-to-apples comparison workflow
Full audit|"Walk me through everything I have coverage-wise right now."|Runs full adequacy analysis on a current policy
New to insurance|"I just got my first homeowners quote. Is this coverage reasonable?"|Runs suitability and adequacy check for first-time buyers
State check|"I'm moving to Florida. Will my coverage still work?"|Triggers state-specific risk analysis

---

### 😎 Looks good. Publish and Test...Go! 🚀

## 📋 Sample Document Set

The sample package includes a current-policy set and a comparison-quote set for the same synthetic customer profile:

**Current Policy Set:**
- [assets/SamplePolicy_Auto.pdf](assets/SamplePolicy_Auto.pdf)
- [assets/SamplePolicy_Home.pdf](assets/SamplePolicy_Home.pdf)
- [assets/SamplePolicy_Umbrella.pdf](assets/SamplePolicy_Umbrella.pdf)

**Comparison Quote Set:**
- [assets/SageHill_AutoQuote.pdf](assets/SageHill_AutoQuote.pdf)
- [assets/SageHill_HomeQuote.pdf](assets/SageHill_HomeQuote.pdf)
- [assets/SageHill_UmbrellaQuote.pdf](assets/SageHill_UmbrellaQuote.pdf)

**Recommended test flow in Agent Builder:**

1. Upload one current policy and one matching quote for a simple apples-to-apples comparison.
2. Repeat by line of business (auto, home, then umbrella).
3. Ask for a final summary after all pairwise comparisons are complete.

---

## AGENT MAKER DISCLAIMERS

### Limitations 🤕

- **Policy interpretation is analytical, not binding.** The agent reasons over policy language and generates coverage interpretations. These are analytical outputs, not legal opinions. Coverage determination rests with the carrier, not the agent.

- **State-specific guidance is contextual, not authoritative.** The agent can flag state-relevant factors (e.g., residual market options, required notice periods, catastrophe deductible norms). It does not provide legal advice about state regulations. Always consult a licensed in-state professional for regulatory certainty.

- **Knowledge retrieval is document-dependent.** The agent analyzes only the documents you provide. If a policy document is incomplete, poorly scanned, or omits key pages, the agent's analysis will be incomplete. Always verify your policy documents are complete before uploading.

- **Premium estimates are not quotes.** If the agent discusses typical premium ranges or price impacts, these are general market observations, not quotes. Actual pricing depends on underwriting, not agent reasoning.

- **Scoring and adequacy assessment are advisory, not prescriptive.** The agent evaluates coverage against general benchmarks and your stated context. "Adequate" or "insufficient" are recommendations for your review, not final determinations. A licensed professional may advise differently based on nuances the agent did not capture.

- **Comparison scoring assumes document completeness.** When comparing two quotes, the agent normalizes visible terms. If either quote omits details or uses non-standard wording, the comparison may be incomplete. Always read the full policy documents before deciding.

- **Session context does not persist across conversations.** If you close the conversation and open a new one, you will need to re-upload documents and re-establish context. Treat each session as a standalone analysis.

### Best practice for users ❗**IMPORTANT**❗

- **The agent is an advisor, not a decision-maker.** It surfaces, analyzes, and recommends. Every output it produces is a starting point for your review, not a final instruction. Treat it accordingly.

- **Always read the original policy documents.** The agent generates summaries and analysis. Policy language is precise and often contains nuances. Never rely solely on the agent's summary without reviewing the actual policy text yourself.

- **Challenge the agent if context is missing.** If the agent makes an assumption about your household, assets, or risk tolerance that feels wrong, tell it. Recalibrate your context and re-run the analysis. The agent is only as good as the information you provide.

- **Verify numbers before acting.** Before making a coverage decision based on the agent's comparison or recommendation, verify that premium amounts, deductible values, and coverage limits are transcribed correctly. The agent reads documents accurately but can occasionally misinterpret formatting.

- **State matters.** Insurance regulations, policy forms, minimum coverage requirements, and market practices vary significantly by state. Always tell the agent your state before asking for adequacy or suitability advice. Generic guidance may not apply to your jurisdiction.

- **Licensed advice is not optional.** The agent can help you understand your options and ask smarter questions of a licensed agent or broker. It cannot replace licensed advice. Before binding coverage or declining a policy, consult a licensed professional.

- **Do not rely on price alone.** Cheaper is not always better in insurance. The agent's job is to help you see what you're trading for that lower price. Make decisions on value, not just premium.

---

## Data provenance note

The files in [assets/SamplePolicy_Auto.pdf](assets/SamplePolicy_Auto.pdf), [assets/SamplePolicy_Home.pdf](assets/SamplePolicy_Home.pdf), [assets/SamplePolicy_Umbrella.pdf](assets/SamplePolicy_Umbrella.pdf), [assets/SageHill_AutoQuote.pdf](assets/SageHill_AutoQuote.pdf), [assets/SageHill_HomeQuote.pdf](assets/SageHill_HomeQuote.pdf), and [assets/SageHill_UmbrellaQuote.pdf](assets/SageHill_UmbrellaQuote.pdf) are synthetic test artifacts created for demonstration.

- All names, addresses, identifiers, and contact details are fictitious placeholders.
- These documents do not represent real customers, real properties, or real issued policies.
- The sample content is included only to demonstrate policy analysis workflows and output quality.
- Do not use these files for underwriting, legal, or claims decision-making.

---

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20personal-insurance-advisor-agent%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

---

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-personal-insurance-advisor-agent)
