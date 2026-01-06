from typing import Dict, Any
from groq import Groq
from app.config import get_settings


def generate_grant_application(grant_data: Dict[str, Any], org_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate a complete grant application using Groq's Llama 3.1 70B model

    Args:
        grant_data: Dictionary containing grant details (title, description, eligibility, etc.)
        org_data: Dictionary containing organization details (name, mission, budget, etc.)

    Returns:
        Dictionary with generated sections of the application
    """

    # Initialize Groq client
    settings = get_settings()
    client = Groq(api_key=settings.groq_api_key)

    # Extract organization data
    org_name = org_data.get('organization_name', 'Our Organization')
    org_type = org_data.get('organization_type', 'Child Care Center')
    city = org_data.get('city', 'Portland')
    mission = org_data.get('mission_statement', 'To provide quality early childhood education')
    enrollment = org_data.get('current_enrollment', 50)
    budget = org_data.get('operating_budget', 250000)
    staff = org_data.get('staff_count', 8)

    # Extract personalization data
    achievements = org_data.get('key_achievements', '')
    specific_needs = org_data.get('specific_needs', '')
    target_outcomes = org_data.get('target_outcomes', '')
    community_impact = org_data.get('community_impact', '')

    # Extract grant data
    grant_title = grant_data.get('title', 'Grant Program')
    grant_source = grant_data.get('source_name', 'Funding Organization')
    amount_min = grant_data.get('amount_min', 10000)
    amount_max = grant_data.get('amount_max', 50000)
    description = grant_data.get('description', 'Support for early childhood education')
    eligibility = grant_data.get('eligibility_criteria', [])
    priorities = grant_data.get('funding_priorities', [])

    # Create comprehensive context for the AI
    context = f"""
You are an expert grant writer with a proven track record of winning competitive funding. You understand that funders have limited resources and receive many applications - your job is to make THIS application stand out as the clear choice.

GRANT INFORMATION:
- Title: {grant_title}
- Funding Organization: {grant_source}
- Description: {description}
- Funding Range: ${amount_min:,.0f} - ${amount_max:,.0f}
- Eligibility Criteria: {', '.join(eligibility) if eligibility else 'General eligibility'}
- Funding Priorities: {', '.join(priorities) if priorities else 'General priorities'}

ORGANIZATION INFORMATION:
- Name: {org_name}
- Type: {org_type}
- Location: {city}, Oregon
- Mission: {mission}
- Current Enrollment: {enrollment} children
- Annual Budget: ${budget:,.0f}
- Staff Count: {staff} professionals

PERSONALIZATION DETAILS:
- Key Achievements: {achievements}
- Specific Needs/Challenges: {specific_needs}
- Target Outcomes: {target_outcomes}
- Community Impact: {community_impact}

YOUR MISSION: Write an application that makes funders excited to invest in this organization. This application must:

1. DEMONSTRATE EXCEPTIONAL VALUE: Show why this organization delivers outsized impact relative to investment. Highlight proven track record, efficiency, and results.

2. CREATE URGENCY: Illustrate the critical need and what will be lost if this grant isn't awarded. Make the funder feel this is an opportunity they cannot miss.

3. SHOWCASE UNIQUE STRENGTHS: Emphasize what makes this organization different from and better than alternatives. Focus on competitive advantages, innovative approaches, and special expertise.

4. PROVE CREDIBILITY: Use specific data, achievements, and examples that demonstrate capability. Make it clear this organization will deliver on promises.

5. ALIGN PERFECTLY: Connect every aspect of the proposal directly to the funder's priorities and mission. Show you understand what they care about and how this investment advances their goals.

6. PAINT A VIVID PICTURE: Help the funder visualize the specific children, families, and communities who will benefit. Make the impact tangible and emotionally compelling.

7. ELIMINATE DOUBT: Anticipate concerns (sustainability, capacity, outcomes) and proactively address them with confidence and evidence.

8. INSPIRE CONFIDENCE: Use strong, decisive language that conveys competence and readiness. Avoid hedging or uncertainty.

Write in a professional but passionate tone that balances data-driven credibility with heartfelt commitment to mission. Every sentence should advance the case for funding THIS organization.
"""

    sections = {}

    # Define sections to generate
    section_prompts = {
        "executive_summary": "Write a powerful Executive Summary (250-300 words) that immediately establishes why this organization is the ideal recipient for this grant. Open with the most compelling achievement or impact statistic. Create a sense of opportunity and urgency. Make the funder excited about what their investment will accomplish. This must be so strong that even if they read nothing else, they want to fund this proposal.",

        "organizational_background": "Write an Organizational Background section (350-400 words) that positions this organization as exceptionally qualified and proven. Highlight impressive achievements with specific numbers and results. Emphasize unique strengths, innovative approaches, or special expertise that sets this organization apart. Build confidence that this team has the track record, skills, and commitment to deliver outstanding results. Make the funder feel they're investing in excellence.",

        "need_statement": "Write a Statement of Need (350-400 words) that creates genuine urgency while demonstrating deep understanding of the issue. Use compelling data and specific examples that make the need real and pressing. Show what's at stake if this grant isn't funded - the children who won't be served, the families who will struggle, the community opportunity that will be lost. Connect the need directly to what the funder cares about. Make them feel that funding this is not just beneficial but essential.",

        "project_description": "Write a Project Description (450-500 words) that makes the funder confident this investment will work. Be specific and detailed about activities, demonstrating you've thought through implementation. Highlight what makes this approach effective, innovative, or superior to alternatives. Show how activities align perfectly with funder priorities. Include a realistic timeline that proves you're ready to execute immediately. Make them visualize exactly how their money will create change.",

        "expected_outcomes": "Write an Expected Outcomes section (300-350 words) that demonstrates exceptional return on investment. Present ambitious but achievable targets with specific metrics. Show both short-term wins and longer-term impact. Explain how you'll measure and track results, proving accountability. Connect outcomes directly to the funder's mission and goals. Use language that conveys certainty and commitment. Make them see exactly what their investment will buy.",

        "budget_justification": "Write a Budget Justification (300-350 words) that shows every dollar is strategically allocated for maximum impact. Emphasize the value and efficiency of your approach. Show how costs compare favorably to outcomes. Demonstrate fiscal responsibility and smart resource management. If possible, note any cost-sharing, matching funds, or in-kind contributions that multiply the funder's investment. Make them feel their money will be used wisely and will go further here than elsewhere.",

        "sustainability_plan": "Write a Sustainability Plan (300-350 words) that eliminates concerns about long-term viability. Show a realistic, concrete strategy for continuing impact beyond the grant period. Demonstrate organizational stability and growth trajectory. Highlight existing relationships with other funders or partners. Prove this isn't a one-time effort but an investment in building lasting capacity. Make them confident this grant will catalyze sustained change, not just temporary support."
    }

    print("Generating grant application with Groq AI...")

    # Generate each section using Groq
    for section_name, section_prompt in section_prompts.items():
        print(f"  Generating: {section_name}...")

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": context
                    },
                    {
                        "role": "user",
                        "content": section_prompt
                    }
                ],
                model="llama-3.3-70b-versatile",  # Fast and high-quality model
                temperature=0.7,  # Balanced creativity and consistency
                max_tokens=1024,  # Enough for detailed sections
            )

            sections[section_name] = chat_completion.choices[0].message.content.strip()
            print(f"  ✓ {section_name} generated ({len(sections[section_name])} chars)")

        except Exception as e:
            print(f"  ✗ Error generating {section_name}: {str(e)}")
            # Fallback to a simple template if AI fails
            sections[section_name] = f"[This section will be generated with AI. Error: {str(e)}]"

    print("✓ Grant application generation complete!")
    return sections


def refine_section(original_text: str, feedback: str) -> str:
    """
    Refine a specific section based on user feedback using Groq AI

    Args:
        original_text: The original section text
        feedback: User's feedback or instructions for improvement

    Returns:
        Refined section text
    """

    settings = get_settings()
    client = Groq(api_key=settings.groq_api_key)

    prompt = f"""You are an expert grant writer. A user has provided feedback on a section of their grant application.

ORIGINAL TEXT:
{original_text}

USER FEEDBACK:
{feedback}

Please revise the text based on the user's feedback. Maintain the professional tone and quality of grant writing while incorporating their requested changes. Return ONLY the revised text, with no additional commentary."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error refining section: {str(e)}")
        return f"{original_text}\n\n[Note: Unable to refine section. Error: {str(e)}]"


def generate_personalization_suggestion(field_name: str, org_data: Dict[str, Any]) -> str:
    """
    Generate a personalization field suggestion based on organization data

    Args:
        field_name: The personalization field to generate (key_achievements, specific_needs, target_outcomes, community_impact)
        org_data: Dictionary containing basic organization details

    Returns:
        Suggested text for the personalization field
    """

    settings = get_settings()
    client = Groq(api_key=settings.groq_api_key)

    # Extract organization data
    org_name = org_data.get('organization_name', 'the organization')
    org_type = org_data.get('organization_type', 'Child Care Center')
    city = org_data.get('city', 'Portland')
    mission = org_data.get('mission_statement', '')
    enrollment = org_data.get('current_enrollment', '')
    budget = org_data.get('operating_budget', '')
    staff = org_data.get('staff_count', '')

    budget_str = f"${budget:,.0f}" if budget else 'Not specified'

    prompts = {
        "key_achievements": f"""Based on this organization's profile, suggest 2-3 realistic key achievements or success stories that would be impressive to grant funders. Be specific and include metrics where possible.

Organization: {org_name}
Type: {org_type}
Location: {city}, Oregon
Mission: {mission}
Enrollment: {enrollment} children
Budget: {budget_str}
Staff: {staff} professionals

Write ONLY the achievement text (2-3 sentences), with no preamble or labels. Make it compelling and data-driven.""",

        "specific_needs": f"""Based on this organization's profile, suggest specific challenges or gaps that grant funding could address. Focus on realistic needs for a {org_type} in Oregon.

Organization: {org_name}
Type: {org_type}
Location: {city}, Oregon
Mission: {mission}
Enrollment: {enrollment} children
Budget: {budget_str}
Staff: {staff} professionals

Write ONLY the needs text (2-3 sentences), with no preamble or labels. Be specific about what's needed and why.""",

        "target_outcomes": f"""Based on this organization's profile, suggest measurable outcomes that could be achieved with grant funding. Focus on specific, quantifiable goals appropriate for a {org_type}.

Organization: {org_name}
Type: {org_type}
Location: {city}, Oregon
Mission: {mission}
Enrollment: {enrollment} children
Budget: {budget_str}
Staff: {staff} professionals

Write ONLY the outcomes text (2-3 sentences), with no preamble or labels. Include specific numbers and metrics.""",

        "community_impact": f"""Based on this organization's profile, suggest how this organization impacts the local community. Focus on realistic community value for a {org_type} in {city}, Oregon.

Organization: {org_name}
Type: {org_type}
Location: {city}, Oregon
Mission: {mission}
Enrollment: {enrollment} children
Budget: {budget_str}
Staff: {staff} professionals

Write ONLY the community impact text (2-3 sentences), with no preamble or labels. Emphasize community value and relationships."""
    }

    prompt = prompts.get(field_name, "")
    if not prompt:
        return f"Unable to generate suggestion for {field_name}"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,  # Slightly higher for more creative suggestions
            max_tokens=300,
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error generating personalization suggestion: {str(e)}")
        return f"Unable to generate suggestion. Please fill this in manually."
