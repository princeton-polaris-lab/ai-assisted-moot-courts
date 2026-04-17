METRICS_METADATA = {
   "VALENCE": {
       "prompt": "How competitive/cooperative is the justice's remark in the current turn?",
       "instructions": """Your classification should choose from a likert scale ranging from 'Competitive' to 'Cooperative':
       - "Competitive": The remark expresses clear justice displeasure with the advocate's last statement in the oral argument context.
           - e.g. "No, no, no, that wasn't the question."
       - "Slightly Competitive": The remark challenges the content of the advocate's last statement in the oral argument context.
           - e.g. "Under what statutory authority was Section 3 passed?"
       - "Neutral": The remark is orthogonal to any of the advocate's arguments. The remark may be purely procedural.
           - e.g. "Yes, thank you, Mr. Chief Justice."
       - "Slightly Cooperative": The remark intends to allow the advocate to expand upon one of his/her existing arguments.
           - e.g. "Okay. All right. So what was your argument?"
       - "Cooperative": The remark suggests justice agreement or support (often through restatement) with the advocate's last statement in the oral argument context.
           - e.g. "But you're not suggesting that. You're actually saying... and it actually says..." """,
       "buckets": "(Competitive, Slightly Competitive, Neutral, Slightly Cooperative, Cooperative)",
       "metric_type": "distributional"
   },
   # examples shortened and taken from https://github.com/HazyResearch/legalbench/blob/main/tasks/oral_argument_question_purpose/claude_prompt.txt
   "LEGALBENCH": {
       "prompt": "Which LegalBench category does the justice's remark, made in the current turn, fall into?",
       "instructions": """Your classification should choose from the following LegalBench categories:
       - 'Background': Seeks factual or procedural information missing or unclear in the briefs.
           - e.g. "I'm curious how other states have dealt with this conundrum besides Colorado and how you -- which ones of those you think we should take account of."
       - 'Clarification': Aims to clarify the advocate's position or the scope of the rule being proposed.
           - e.g. "Is that -- do you understand that to be part of the stipulations or not?"
       - 'Implications': Explores the limits of a proposed rule or its potential implications for future cases.
           - e.g. "Do they have to -- can you compel that speech? Do they have to publish it?"
       - 'Support': Offers implicit or explicit support for the advocate's position.
           - e.g. "Ms. Hansford, I think everyone might be underselling Steele here. I mean, it's true what Justice Alito says about this first sentence sets up the question in an odd way. But the actual holding and heart of the opinion is on page 286..."
       - 'Criticism': Challenges or criticizes the advocate's position.
           - e.g. "Even though the site doesn't say anything about that? It doesn't say, wow, gay marriage is a wonderful thing. It doesn't say -- it doesn't even say...."
       - 'Communicate': Serves as a means for the judge to communicate with other judges on the court, rather than directly with the advocate.
           - e.g. "Last question. This might be what Justice Kagan was asking, but it might be something different..."
       - 'Humor': Introduces humor to ease tension during the proceedings.
           - e.g. "I mean, it does seem a little bit like due process Lochnerism for corporations here, doesn't it?"
       - 'Unclear': The remark is unclear or irrelevant to the arguments presented.
           - e.g. "So I --" """,
       "buckets": "(Background, Clarification, Implications, Support, Criticism, Communicate, Humor, Unclear)",
       "metric_type": "distributional"
   },
   "METACOG":  {
       "prompt": "Which MetaCog category does the justice's remark, made in the current turn, fall into?",
       "instructions": """Your classification should choose from the following MetaCog categories:
       - 'statutory_interpretation': Related to the interpretation and application of statutes
           - e.g. "That is a very narrow way to interpret 'authorized'."
       - 'precedent_and_doctrine': Related to the examination and application of precedents and doctrines.
           - e.g. "How is what we held in Chevron inconsistent with Justice Barrett's hypothetical?"
       - 'case_facts_and_context': Related to the examination of case facts and context.
           - e.g. "Do we know that there were other photos that met the criteria that I mentioned?"
       - 'judicial_role_and_review': Related to the examination of the judicial role and review.
           - e.g. "Would you dispute the proposition that if the discrepancy were true, that the inference drawn by the Fifth Circuit would be a legitimate inference?"
       - 'argumentation_and_clarification': Related to the examination of argumentation and clarification.
           - e.g. Did -- did I understand you in response to a question from Justice Thomas to say that Chevron doesn't apply to constitutional questions?"
       - 'constitutional_issues': Related to the examination of constitutional issues.
           - e.g. "And the constitutionality of this statute is what's at issue?"
       - 'procedural_matters': Related to the examination of procedural matters.
           - e.g. "This Court granted certiorari because you told us there was a 5-to-2 split. And, in fact, there is no split."
       - 'unclear_or_irrelevant': The remark is unclear or irrelevant to the arguments presented.
           - e.g. "I'm sorry. What --" """,
       "buckets": "(statutory_interpretation, precedent_and_doctrine, case_facts_and_context, judicial_role_and_review, argumentation_and_clarification, constitutional_issues, procedural_matters, unclear_or_irrelevant)",
       "metric_type": "distributional"
   },
   "STETSON":  {
       "prompt": "Which Stetson category does the justice's remark, made in the current turn, fall into?",
       "instructions": """Your classification should choose from the following Stetson categories:
       - 'elicit_information': A judge may ask about the facts in the evidence or record, or about authorities, parties, or background.
           - "Before we get to the constitutional problems, what's the statutory authority to appoint the Board?"
       - 'authority_applicability_legal_reach': A judge may ask about how precedent applies to a client's facts or how far legal principles extend. A judge might also ask how authorities are similar to or distinguishable from the case at hand.
           - "Our prior precedents were talking about dangerous, it was a little confusing to all of a sudden find "responsible" being the operative term. If we take your interpretation, what's the bright-line?"
       - 'hypothetical': A judge may ask hypothetical questions to see just how far a legal position will reasonably reach. These can be phrased as examples.
           - e.g. "Can I give you a hypothetical? He does a fundraiser for his mosque. He has no idea that the mosque is under suspicion... Can you put him back on the No Fly list under this declaration?
       - 'opposing_counsel_args': A judge may ask questions about the opposing counsel's argument. These questions will be designed to probe the weaknesses of the current advocate's argument,
           - e.g. "Your friends on the other side will say that there does exist an incompatibility. What would you say to that?"
       - 'policy': A judge may ask policy questions to know how their decisions will impact society.
           - e.g. "How do you sort out those competing policy arguments?"
       - 'seek_concessions': A judge may ask the current advocate to concede a point because judges like to narrow the legal and factual questions in the case and to determine just how far the consequences of a decision will reach.
           - e.g. "Congress amended the statute clearly to expand liability. Do you -- do you concede that?"
       - 'softball': A judge may ask softball questions -- friendly questions designed to help the current advocate -- because they agree with the current advocate and want to help the advocate make his/her point to their fellow judges.
           - e.g. "That's the point, isn't it?"
       - 'irrelevant': : A judge may make a remark that is not relevant to the case at hand.
           - e.g. "Thank you."
       - 'unclear': The remark is unclear.
           - e.g. "Why --"
       - 'other': A judge's remark that does not fall into any of the categories listed above.
           - e.g. "Well, I think that normally connotes something different." """,
       "buckets": "(elicit_information, authority_applicability_legal_reach, hypothetical, opposing_counsel_args, policy, softball, irrelevant, unclear, other)",
       "metric_type": "distributional"
   },
   "ARGUMENT_CONSISTENCY_AND_CORRECTNESS": {
       "prompt": "Does the justice's remark in the current turn call out the advocate's last statement in the oral argument context for inconsistent argumentation?",
       "instructions": """Choose your response from the follow categories:
       - 'Yes': The justice remark calls out inconsistent argumentation IN THE ADVOCATE'S LAST REMARK ONLY.
       - 'No': The justice remark does not call out inconsistent argumentation IN THE ADVOCATE'S LAST REMARK ONLY.
       **IMPORTANT**: YOUR CLASSIFICATION IS WHETHER OR NOT THE JUSTICE CALLS OUR INCONSISTENT ARGUMENTATION IN THE ADVOCATE'S LAST REMARK ONLY.
       """,
       "buckets": "(Yes, No)",
       "metric_type": "distributional"
   },
   "SWITCHING_SIDES_TEST": {
       "prompt": "Does the justice's remark in the current turn call the advocate's last remark out for going against their argument in the context?",
       "instructions": """Choose your response from the follow categories:
       - 'Yes': The justice remark calls an advocate for going against their argument IN THE ADVOCATE'S LAST REMARK ONLY.
       - 'No': The justice remark does not call out an advocate for going against their argument IN THE ADVOCATE'S LAST REMARK ONLY.
       """,
       "buckets": "(Yes, No)",
       "metric_type": "distributional"
   },
   "LOGICAL_FALLACY_BINARY": {
       "prompt": "If we give you a specific logical fallacy, does the justice's remark in the current turn call out that specific logical fallacy in the advocate's last remark?",
       "instructions": """If the justice's remark calls out the specific logical fallacy we pass you, return 'Yes'. 
        Otherwise, if we give you 'No Fallacy' or the justice's remark does not call out the SPECIFIC logical fallacy we pass you, return 'No.'
       """,
       "buckets": "(Yes, No)",
       "metric_type": "binary_classification"
   },
   "LOGICAL_FALLACY": {
       "prompt": "Does the justice's remark in the current turn call out a logical fallacy in the advocate's last remark?",
       "instructions": """If the justice's remark does not call out a logical fallacy in the advocate's last remark, return 'None'. 
        Otherwise, choose what fallacy is caught from ONLY the following categories:
        - 'Legal Factual Inaccuracy'
        - 'General Factual Inaccuracy'
        - 'Sufficient vs. Necessary'
        - 'Correlation vs. Causation'
        - 'Sampling Flaw'
        - 'Numbers Flaw'
        - 'Exclusivity Flaw'
        - 'Comparison Fallacy'
        - 'Temporal Flaw' 
        - 'Misstating the Justice's Last Question'
        - 'Ignoring the Justice's Last Question"
       """,
       "buckets": "(None, Legal Factual Inaccuracy, General Factual Inaccuracy, Sufficient vs. Necessary, Correlation vs. Causation, Sampling Flaw" \
       "Numbers Flaw, Exclusivity Flaw, Comparison Fallacy, Temporal Flaw, Misstating the Justice's Last Question, Ignoring the Justice's Last Question)",
       "metric_type": "distributional"
   },
   "VIOLATE_DECORUM": {
       "prompt": "Does the justice's remark in the current turn suggest that the advocate was being cheeky, snarky, rude, or otherwise inappropriate in their last remark in the oral argument context?",
       "instructions": """Choose your response from the follow categories:
       - 'Yes': The justice response suggests that the justice did not like how an advocate framed a response and found it inappropriate.
       - 'No': The justice response does not make any mention of how an advocate framed their last response.
       """,
       "buckets": "(Yes, No)",
       "metric_type": "distributional"
   },
   "MOST_COMPETITIVE_RESPONSE": {
       "prompt": "Does the justice's remark suggest justice unhappiness with the advocate?",
       "instructions": """Choose your response from the follow categories:
       - 'Yes': The remark suggests that the justice is unhappy with the advocate.
       - 'No': The justice suggests that the justice is perfectly fine with the advocate.
       """,
       "buckets": "(Yes, No)",
       "metric_type": "distributional"
   },
   "RESPONSE_SUGGESTING_MISUNDERSTANDING": {
       "prompt": "Does the justice's remark in the current turn suggest that the advocate has misunderstood or misstepped with their last answer in the oral argument context?",
       "instructions": """Choose your response from the follow categories:
       - 'Yes': The justice response suggests that the advocate has misunderstood, misrepresented, or misstepped with their last response.
       - 'No': The justice response does not suggest that the advocate has misunderstood, misrepresented, or misstepped with their last response.
       """,
       "buckets": "(Yes, No)",
       "metric_type": "distributional"
   },
   "SYCOPHANCY": {
       "prompt": "Does the justice's remark display sycophantic behavior?",
       "instructions": """Choose your response from the follow categories:
       - 'Yes': The justice remark displays overly supportive behavior inappropriate for a Supreme Court oral argument context.
       - 'No': The justice remark displays behavior appropriate for a Supreme Court oral argument context.
       """,
       "buckets": "(Yes, No)",
       "metric_type": "distributional"
   },
   "CONSISTENCY_WITH_STATUTORY_INTERPRETATION": {
       "prompt": "Is the justice's remark consistent with what's known of the justice's approach to statutory interpretation?",
       "instructions": """Choose your response from the follow categories:
       - 'Yes': The remark is consistent or mostly consistent with what's known of the justice's approach to statutory interpretation.
       - 'No': The remark is inconsistent or mostly inconsistent with what's known of the justice's approach to statutory interpretation.
       - 'NA': The remark seems to be orthogonal to ANY approaches to statutory interpretation.""",
       "buckets": "(Yes, No, NA)",
       "metric_type": "distributional"
   },
   "CONSISTENCY_WITH_POLITICAL_IDEOLOGY": {
       "prompt": "Is the justice's remark consistent with the justice's known political ideology?",
       "instructions": """Choose your response from the following categories:
       - 'Yes': The remark is consistent or mostly consistent with the justice's known political ideology.
       - 'No': The remark is inconsistent or mostly inconsistent with the justice’s known to political ideology.
       - 'NA': The remark seems to be orthogonal to ANY political ideologies.""",
       "buckets": "(Yes, No, NA)",
       "metric_type": "distributional"
   },
   "RUBRIC_SIMILARITY": {
       "prompt": "How similar are remark and remark1 to each other in the current turn?",
       "instructions": """We define similarity on four axes: topic, diction, specificity, and illocutionary act type. Choose your response from the following categories:
       - '1': So long as remark and the remark2 have different topics, we score 1, regardless of the other three categories.
       - '2': If only the topic is the same between remark and remark2, we score 2.
       - '3': If the topic and one of the other categories (one of diction, specificity, or illocutionary act type) is the same between remark and remark2, we score 3.
       - '4': If the topic and two of the other categories (two of diction, specificity, or illocutionary act type) are the same between remark and remark2, we score 4.
       - '5': If all categories between the generated and the actual question are the same, we score 5.""",
       "buckets": "(1, 2, 3, 4, 5)",
       "metric_type": "comparative"
   },
   "ISSUE_COVERAGE_BROAD": {
       "prompt": "Does the justice's question address the topic of the issue at hand?",
       "instructions": """Choose your response from the following categories:
       - 'Yes': The current_judge_turn brings up/is topically related to issue.
       - 'No': The current_judge_turn is unrelated to issue.""",
       "buckets": "(Yes, No)",
       "metric_type": "comparative"
   },
   "ISSUE_COVERAGE_MED": {
       "prompt": "Does the justice's question address the the issue at hand?",
       "instructions": """Choose your response from the following categories:
       - 'Yes': The current_judge_turn addresses what's brought up in issue head on.
       - 'No': The current_judge_turn doesn't DIRECTLY address what's brought up in the issue.""",
       "buckets": "(Yes, No)",
       "metric_type": "comparative"
   },
   "ISSUE_COVERAGE_SPECIFIC": {
       "prompt": "Does the justice's question address all aspects of the issue at hand?",
       "instructions": """Choose your response from the following categories:
       - 'Yes': The current_judge_turn addresses ALL points the issue raises.
       - 'No': The current_judge_turn does not address SOME of the points the issue raises.""",
       "buckets": "(Yes, No)",
       "metric_type": "comparative"
   }
}