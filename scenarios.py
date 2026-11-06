"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    # ── Criterion 1: False Positive Rate on Human Writing ────────────────────
    # In criteria.md, Criterion 1 requires that of 10 distinct samples of
    # verified human writing, at most 1 (<= 10%) is classified as "ai".
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "So the other day I was walking down this street when 10 really aggressive young men came up to me. They tried to [unalive] me! Tear my limbs off! Smash my tape recorder! It's a daaaangerous place.",
            "At their new old house, said to be haunted, the children first run into “soot spreaders,” which are said to be spirits inhabiting abandoned houses that move away if the new inhabitants smile enough. The younger Mei later discovers and chases after a little funny creature, discovers another one, and eventually follows them to a hole in a giant camphor tree where she falls and lands on the giant version of the funny fluffy creatures, which she names “Totoro” after a character from a book.",
            "A hacker obtaining millions of Yahoo passwords is a Confidentiality and Data Integrity violation. Passwords are secure data and the leaking of them breaches both the confidentiality of the passwords and the data in the account. Unauthorized access to the account is also a Data Integrity violation as there is no knowing how the data may be tampered by bad actors.",
            "A slightly more advanced encryption method is XOR, which simply takes 1 bit from the input and 1 bit from the password, performs a XOR operation (1 if the bits differ), and repeats for the entirety of the input, looping the password if necessary. This isn’t the most secure method as it is vulnerable to frequency analysis and bruteforcing if it’s a short key, but it has been used, for instance, in production releases of visual novels using the KiriKiri engine to try and encrypt the data to prevent decompilation. There are significantly more combinations than just 26 depending on key length.",
            "I think the issue of whether this constitutes a privacy violation or not depends on the terms of service presented to the user when they receive their device and attempt to use it. If the privacy policy of the device says that the company is allowed to collect these kinds of analytics and do whatever they want with it, like handing it over to the government, if the customer hits Agree it is not a privacy violation. If the navigation device makes no attempt to inform the customer that their data is being collected and used, this is a privacy violation.",
            "A person lives in an apartment building where the landlord charges rent per person instead of per room for whatever reason. This person has someone they know who is having a hard time so they offer to let them crash at their apartment for however long they need. Now the water use is roughly doubled because they both take their own showers and this is not Japan where families share the same bath water (though apparently it’s normal to shower before entering the bath tub so it’s relatively clean). The landlord is an unsavory person with ties to law enforcement and obtains utility statistics suggesting that an unauthorized person is living in the apartment and goes to extort more rent.",
            "Unfortunately for Rita Espinoza, the case for her video being “fair use” does not look very promising. Rita has a 5-minute video that just so happens to contain 30 seconds of a copyrighted song, but the type of video is not specified, so I would imagine that it is irrelevant to the hypothetical and is therefore not an educational video of some sort, which would fall under educational fair use rules.",
            "For the sake of argument, let’s consider a scenario at a Certain Company that specializes in producing smart devices. At a highly publicized event, they unveil the new release of their mobile operating system, in which they announce that alongside new AI features and random tweaks to the interface design, as a result of extensive efforts to rearchitect the graphics rendering pipeline, background process scheduling, and the introduction of a new proprietary energy-aware CPU governor, they have managed to reduce UI microstutters by “up to” 100% at a 120hz refresh rate target and decrease idle battery consumption by “up to” 40% while the device runs cooler overall.",
            "Clickjacking is the takeover of a user’s mouse action in order to perform an action that the user does not intend. There are a few methods of clickjacking. One of them involves hiding a button under an unrelated banner, such as a fictional dismiss button for something like a pop-up, which hides a social media Like widget underneath that triggers when the user clicks.",
            "So another day I was walking down this street when 2 really aggressive young kids came up to me. They harrassed me! Asked me stupid questions! Steal my cellular phone! It's a daaangerous place.",
        ],
    },
    # ── Criterion 2: Score Separation Between Clear Human and Clear AI Text ────
    # In criteria.md, Criterion 2 requires measuring the mean score gap (>= 0.40)
    # between 5 clearly-human texts and 5 clearly-AI texts.
    {
        "name": "score separation - human",
        "criterion": 2,
        "texts": [
            "So the other day I was walking down this street when 10 really aggressive young men came up to me. They tried to [unalive] me! Tear my limbs off! Smash my tape recorder! It's a daaaangerous place.",
            "A slightly more advanced encryption method is XOR, which simply takes 1 bit from the input and 1 bit from the password, performs a XOR operation (1 if the bits differ), and repeats for the entirety of the input, looping the password if necessary. This isn’t the most secure method as it is vulnerable to frequency analysis and bruteforcing if it’s a short key, but it has been used, for instance, in production releases of visual novels using the KiriKiri engine to try and encrypt the data to prevent decompilation. There are significantly more combinations than just 26 depending on key length.",
            "Unfortunately for Rita Espinoza, the case for her video being “fair use” does not look very promising. Rita has a 5-minute video that just so happens to contain 30 seconds of a copyrighted song, but the type of video is not specified, so I would imagine that it is irrelevant to the hypothetical and is therefore not an educational video of some sort, which would fall under educational fair use rules.",
            "Clickjacking is the takeover of a user’s mouse action in order to perform an action that the user does not intend. There are a few methods of clickjacking. One of them involves hiding a button under an unrelated banner, such as a fictional dismiss button for something like a pop-up, which hides a social media Like widget underneath that triggers when the user clicks.",
            "So another day I was walking down this street when 2 really aggressive young kids came up to me. They harrassed me! Asked me stupid questions! Steal my cellular phone! It's a daaangerous place.",
        ],
    },
    {
        "name": "score separation - ai",
        "criterion": 2,
        "texts": [
            "The implementation of automated testing frameworks provides substantial benefits for modern software development teams. By establishing systematic validation procedures, engineers can identify regression errors before deploying code to production environments. Furthermore, comprehensive test suites ensure that software components maintain expected behavior across varying operating conditions. These automated validation processes significantly reduce the manual effort required during routine quality assurance cycles. Ultimately, integrating continuous testing into the development lifecycle enhances overall system reliability and improves user satisfaction.",
            "Effective communication plays a crucial role in modern collaborative environments. When team members exchange ideas clearly and transparently, organizational productivity increases significantly. Furthermore, structured feedback mechanisms allow individuals to identify potential bottlenecks before they escalate into major obstacles. Ultimately, fostering a culture of continuous dialogue ensures that all participants remain aligned with overarching project objectives.",
            "Cloud computing architectures offer scalable solutions for organizations seeking to optimize resource utilization. By decoupling compute resources from physical on-premise hardware, enterprises can dynamically adjust capacity based on real-time traffic demands. Additionally, automated provisioning scripts streamline deployment pipelines and minimize human configuration errors. In conclusion, adopting modern cloud infrastructure delivers enhanced operational resilience while lowering long-term operational costs.",
            "Machine learning models rely heavily on high-quality training datasets to achieve robust generalization performance. During the data preprocessing phase, practitioners must carefully remove redundant records and normalize feature values across dimensions. Furthermore, implementing rigorous cross-validation protocols helps mitigate overfitting on localized distribution artifacts. Consequently, maintaining disciplined data curation pipelines directly determines the reliability of downstream algorithmic predictions.",
            "Microservice architectures decompose complex software systems into modular, independently deployable services. Each service encapsulates a bounded context and communicates with other components through lightweight protocols such as REST or gRPC. Furthermore, decentralized data management allows individual teams to select the database technology best suited to their specific domain requirements. Consequently, this architectural paradigm accelerates continuous deployment cycles while isolating runtime failures.",
        ],
    },

    # ── Criterion 3: Label Reachability and Coverage ─────────────────────────
    # Changed criterion index from 2 to 3 to match criteria.md numbering.
    # Contains 1 clearly AI text, 1 genuine human text, and 1 borderline text.
    # Note: The human sample uses formal dictionary definition phrasing, which
    # serves as a realistic test of whether formal register tricks the detector.
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            "The implementation of automated testing frameworks provides substantial benefits for modern software development teams. By establishing systematic validation procedures, engineers can identify regression errors before deploying code to production environments. Furthermore, comprehensive test suites ensure that software components maintain expected behavior across varying operating conditions. These automated validation processes significantly reduce the manual effort required during routine quality assurance cycles. Ultimately, integrating continuous testing into the development lifecycle enhances overall system reliability and improves user satisfaction.",
            "Irony is a juxtaposition of what, on the surface, appears to be the case with what is actually or expected to be the case. Originally a rhetorical device and literary technique, irony has also come to assume a metaphysical significance with implications for one's attitude towards life.",
            "Distributed version control systems changed how software development teams collaborate on complex projects. Before modern tools became widespread, handling concurrent edits across multiple branches was difficult and error-prone. Centralized systems made access controls relatively simple to administer across an organization. However, allowing developers to maintain independent commit histories locally provided greater flexibility during daily development, even when working offline for extended periods.",
        ],
    },

    # ── Criterion 4: Graceful Rejection of Malformed Input ───────────────────
    # Uncommented and mapped to Criterion 4 from criteria.md.
    # Tests that 100% of malformed bodies trigger 4xx client errors rather than
    # crashing the server with a 500 error or falsely returning 200.
    {
        "name": "malformed input",
        "criterion": 4,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },

    # Note on Criterion 5 (Appeal Path Integrity):
    # A criterion about the appeal path cannot be tested purely by POST /submit
    # via run_eval.py, as it requires submitting a text, extracting the content_id,
    # and issuing POST /appeal. This is tested and recorded in the criteria table.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
