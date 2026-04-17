import utils.prompt_utils as prompt_utils

CONSOLIDATED_PROFILES = f"""{prompt_utils.JUSTICE_PROFILES['John G. Roberts, Jr.']}
{prompt_utils.JUSTICE_PROFILES['Clarence Thomas']}
{prompt_utils.JUSTICE_PROFILES['Ketanji Brown Jackson']}
{prompt_utils.JUSTICE_PROFILES['Sonia Sotomayor']}
{prompt_utils.JUSTICE_PROFILES['Neil Gorsuch']}
{prompt_utils.JUSTICE_PROFILES['Samuel A. Alito, Jr.']}
{prompt_utils.JUSTICE_PROFILES['Amy Coney Barrett']}
{prompt_utils.JUSTICE_PROFILES['Brett M. Kavanaugh']}
{prompt_utils.JUSTICE_PROFILES['Elena Kagan']}"""

# f"For reference: {CONSOLIDATED_PROFILES} 

ADVERSARIAL_GENENERATION_METADATA = {
    "DECORUM": {
        "role": "You are giving attorneys examples of what NOT to do in Court.",
        "task": "Your task is to generate the attorney's remark in the current turn that will break courtroom decorum.",
        "specification_examples": """Decorum can be broken for many reasons, up to and not including:
            - addressing a justice as "judge" instead of "Your Honor"
            - being clever or snarky, petulant
            - making off-color remarks
            - personally attacking the opposing counsel
            - referring to individuals referenced in the case by anything but their surnames
            - being sarcastic, insulting, or threatening
            - adopting a colloquial style of sepaking
        Please use your best judgement in breaking decorum. Your examples should obviously break decorum but still be related to the case and transcript.""",
    },
    "RAGE_BAIT": {
        "role": "You are giving attorneys examples of what NOT to do in Court.",
        "task": "Your task is to generate an attorney's remark in the current turn to RAGE BAIT the last justice. Be respectful but PURPOSEFULLY GO AGAINST that justice's known political ideology.",
        "specification_examples": "If the last justice who spoke is liberal, express agreement with conservative talking points. If the last justice who spoke is conservative, express agreement with liberal talking points. " \
        "Try to keep your remark related to the case and transcript. Feel free to contradict your previous arguments.",
    },
    "SWITCHING_SIDES": {
        "role": "You are giving attorneys examples of what NOT to do in Court.",
        "task": "Your task is to generate an attorney's remark in the current turn that CONTRADICTS their main argument, often enumerated in the opening statement.",
        "specification_examples": "The remark should DIRECTLY GO AGAINST AN ATTORNEY'S OPENING STATEMENT ARGUMENT and/or express agreement with the arguments of the OPPOSING counsel."
    },
    "MISSTATEMENT": {
        "role": "Your expertise is in logical fallacies and you are giving attorneys examples of what NOT to do in Court.",
        "task": "Your task is to generate an attorney's remark in the current turn to answer a MISSTATEMENT of the justice question.",
        "specification_examples": "Attorneys make misstatements when they answer a question tangential to the one a justice actually asks. Misstatements can be obvious or subtle." \
        "Please use your best judgement in generating a misstatement-- your examples should be obvious enough misstatements to be easily seen but be reasonably made in the context of the case and transcript."
    },
    "IGNORANCE": {
        "role": "Your expertise is in logical fallacies and you are giving attorneys examples of what NOT to do in Court.",
        "task": "Your task is to generate an attorney's remark in the current turn that ignores the last justice's question and restates an argument or makes a new one without signposting.",
        "specification_examples": "As you know, attorneys should directly answer a question presented to them and signpost if they're going to answer a previous question." \
        "This style of ignoring can be obvious or subtle. Your examples of ignoring should be obvious enough to be easily seen but be reasonably made in the context of the case and transcript."
    },
}