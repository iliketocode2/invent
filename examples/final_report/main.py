"""
Open Source Contributions Report, Spring 2026.
Tufts University CS — built with the Invent framework.
"""

import invent
from invent.ui import *
from datetime import datetime

await invent.setup()


def navigate(message):
    """Route 'navigate' channel press events to the named page."""
    page_id = message.source.name.split("_btn")[0]
    invent.show_page(page_id)


invent.subscribe(navigate, to_channel="navigate", when_subject=["press"])

_NAV_PAGES = [
    ("Home", "cover"),
    ("PyScript", "pyscript"),
    ("Invent", "invent_work"),
    ("Demos", "demos"),
    ("Mentors", "quotes"),
    ("Reflect", "reflection"),
]


def _nav_header():
    """
    Return a new sticky Header with nav buttons.

    Widget instances cannot be shared across pages in Invent, so
    this factory must be called once per page to create a fresh
    Header object each time.
    """
    return Header(
        sticky=True,
        children=[
            Button(
                text=label,
                name=f"{page_id}_btn",
                purpose="SECONDARY",
                size="SMALL",
                channel="navigate",
            )
            for label, page_id in _NAV_PAGES
        ],
    )


# -- Cover Page --


cover = Page(
    id="cover",
    children=[
        Column(
            children=[
                _nav_header(),
                Label(text="# Open Source Contributions Report"),
                Label(
                    text=(
                        "Spring 2026 - Tufts University CS\n\n"
                        "William Goldman - "
                        "[@iliketocode2](https://github.com/iliketocode2)"
                    )
                ),
                Alert(
                    title="About This Report",
                    text=(
                        "This report is itself an Invent application: "
                        "one of the two open-source projects I worked "
                        "on this semester. Use the navigation bar at the "
                        "top to move between sections."
                    ),
                    purpose="PRIMARY",
                ),
                Label(text="## Semester at a Glance"),
                Table(
                    data=[
                        ["", "PyScript", "Invent"],
                        ["Merged PRs", "2", "5"],
                        ["PRs in review", "0", "1"],
                        ["Discussions started", "1", "0"],
                        ["Issues triaged", "2", "0"],
                        ["Lines added (merged)", "80", "1,353"],
                    ],
                    row_headers=True,
                    label="Contribution Summary, Spring 2026",
                ),
                Alert(
                    title="Two Projects, One Semester",
                    text=(
                        "PyScript is Anaconda's platform for running "
                        "Python in the browser (19k+ GitHub stars). "
                        "Invent is a Python-first browser app framework "
                        "built on top of PyScript."
                    ),
                    purpose="SECONDARY",
                ),
                Alert(
                    title="Weekly Meetings",
                    text=(
                        "Throughout the semester I had weekly meetings "
                        "with Nicholas Tollervey and Chris Rogers."
                        "These meetings guided the direction for my "
                        "contributions and provided regular feedback on "
                        "my progress in both PyScript and Invent."
                    ),
                    purpose="SECONDARY",
                ),
            ]
        )
    ],
)


# -- PyScript Page --


pyscript_page = Page(
    id="pyscript",
    children=[
        Column(
            children=[
                _nav_header(),
                Label(text="# PyScript Contributions"),
                Label(
                    text=(
                        "PyScript enables Python in the browser. "
                        "19,000+ GitHub stars, maintained by Anaconda. "
                        "[pyscript.net](https://pyscript.net/)"
                    )
                ),
                Label(text="## Merged Pull Requests"),
                ContentCard(
                    title=("PR #2447: Enable str to be appended to Element"),
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text="**Merged: Feb 4, 2026** - +33 / -5 lines - 2 files"
                        ),
                        Label(
                            text=(
                                "Extended Element.append() in "
                                "pyscript/web.py to accept plain strings "
                                "and other primitives. Previously, passing "
                                "a string raised a TypeError. The fix uses "
                                "the browser's native DOM append(), which "
                                "creates a text node rather than an element"
                                " node."
                            )
                        ),
                        Code(
                            code=(
                                "# Native DOM append creates a text node:\n"
                                "elif isinstance(\n"
                                "    item, (str, int, float, bool)\n"
                                "):\n"
                                "    self._dom_element.append(item)"
                            )
                        ),
                        Label(
                            text="[View PR #2447 on GitHub](https://github.com/pyscript/pyscript/pull/2447)"
                        ),
                    ],
                ),
                ContentCard(
                    title=("PR #2455: Fix ElementCollection.update_all"),
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text="**Merged: Feb 25, 2026** - +47 / -4 lines - 2 files"
                        ),
                        Label(
                            text=(
                                "update_all was using setattr() directly,"
                                " bypassing Element.update()'s class and "
                                "style handling. Passing classes='active' "
                                "via update_all would overwrite the "
                                "attribute instead of calling "
                                "self.classes.add(). This PR routes all "
                                "calls through element.update() to fix the"
                                " bug and remove duplicated logic."
                            )
                        ),
                        Row(
                            children=[
                                Label(
                                    text="[View PR #2455 on GitHub](https://github.com/pyscript/pyscript/pull/2455)"
                                ),
                                Label(
                                    text="[Docs PR #214](https://github.com/pyscript/docs/pull/214)"
                                ),
                            ]
                        ),
                    ],
                ),
                Label(text="## Discussion Started"),
                ContentCard(
                    title=(
                        "Discussion #2453: "
                        "Improving ElementCollection.update_all"
                    ),
                    purpose="PRIMARY",
                    children=[
                        Label(
                            text=(
                                "Before opening PR #2455, I started a "
                                "public design discussion to confirm the "
                                "approach with maintainers Nicholas "
                                "Tollervey and Andrea Giammarchi. The "
                                "thread also surfaced a broader question "
                                "about whether PyScript's web API should "
                                "stay Pythonic (sets/dicts for classes and"
                                " styles) or lean into native DOM APIs "
                                "like classList."
                            )
                        ),
                        Label(
                            text="[View Discussion #2453 on GitHub](https://github.com/pyscript/pyscript/discussions/2453)"
                        ),
                    ],
                ),
                Label(text="## Community Issue Triage"),
                Accordion(
                    children=[
                        Column(
                            name=(
                                "Issue #2466: "
                                "Try block indentation inconsistency"
                            ),
                            children=[
                                Label(
                                    text=(
                                        "A user reported that try blocks "
                                        "inside script tags failed unless "
                                        "indented with tabs. I investigated"
                                        " and traced the behaviour to the "
                                        "codedent library's first-line strip"
                                        " logic, which is consistent with "
                                        "Python's own indentation rules. "
                                        "Resolved as expected behaviour."
                                    )
                                ),
                                Label(
                                    text="[View Issue #2466 on GitHub](https://github.com/pyscript/pyscript/issues/2466)"
                                ),
                            ],
                        ),
                        Column(
                            name=(
                                "Issue #2464: "
                                "Matplotlib regression in py-editor"
                            ),
                            children=[
                                Label(
                                    text=(
                                        "A user found that matplotlib "
                                        "stopped rendering in py-editor "
                                        "after PyScript 2025.8.1. I diffed "
                                        "the releases and traced the issue "
                                        "to a change in ffi.py that replaced"
                                        " 'value is None' checks with a "
                                        "jsnull comparison. In a worker "
                                        "context, JS null values were "
                                        "arriving as jsnull instead of None."
                                        " Maintainer Andrea Giammarchi "
                                        "confirmed the root cause and "
                                        "referenced pyscript.ffi.is_none "
                                        "as a mitigation."
                                    )
                                ),
                                Label(
                                    text="[View Issue #2464 on GitHub](https://github.com/pyscript/pyscript/issues/2464)"
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        )
    ],
)


# -- Invent Work Page --


invent_work_page = Page(
    id="invent_work",
    children=[
        Column(
            children=[
                _nav_header(),
                Label(text="# Invent Contributions"),
                Label(
                    text=(
                        "Invent is a Python-first browser app framework "
                        "built on PyScript. The page you are reading "
                        "right now is itself an Invent app! Invent is "
                        "originally created by Nicholas Tollervey. "
                        "[inventframework.org](https://inventframework.org/)"
                    )
                ),
                Label(text="## Merged Pull Requests"),
                ContentCard(
                    title="PR #142: Divider Widget",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text="**Merged: Mar 10, 2026** - +84 / -7 lines - 4 files"
                        ),
                        Label(
                            text=(
                                "Added a Divider widget that separates "
                                "items in a Row (renders vertically) or a "
                                "Column (renders horizontally). The "
                                "challenge: render() is called before "
                                "_parent is assigned, so orientation cannot"
                                " be determined at render time. Solved by "
                                "overriding the parent setter and resolving "
                                "orientation there."
                            )
                        ),
                        Label(
                            text="[View PR #142 on GitHub](https://github.com/invent-framework/invent/pull/142)"
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #143: Rating Widget (v1)",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text="**Merged: Mar 10, 2026** - +327 / -6 lines - 4 files"
                        ),
                        Label(
                            text=(
                                "Added a Rating widget with half-star "
                                "precision. Each star is split into "
                                "invisible left and right click zones: "
                                "the left half scores i minus 0.5, the "
                                "right half scores i. Supports 3, 5, or "
                                "10 stars, read-only mode, and a brief "
                                "popup animation when the value changes."
                            )
                        ),
                        Label(
                            text="[View PR #143 on GitHub](https://github.com/invent-framework/invent/pull/143)"
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #144: Rating Widget (v2 — Fixes)",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text="**Merged: Mar 16, 2026** - +76 / -65 lines - 3 files"
                        ),
                        Label(
                            text=(
                                "Follow-up refinements: added 1-star "
                                "support, zero-star selection, configurable"
                                " step size as a ChoiceProperty, an "
                                "optional numeric label, and a "
                                "cursor-pointer hover effect on 1-star "
                                "mode."
                            )
                        ),
                        Label(
                            text="[View PR #144 on GitHub](https://github.com/invent-framework/invent/pull/144)"
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #145: Webcam Widget",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text="**Merged: Apr 3, 2026** - +693 / -2 lines - 5 files"
                        ),
                        Label(
                            text=(
                                "Added a Webcam widget with photo, video, "
                                "and both modes. Uses getUserMedia() for "
                                "the live feed, a hidden canvas for frame "
                                "capture via drawImage(), and MediaRecorder"
                                " for video recording. Captured media is "
                                "downloaded via a temporary anchor element."
                                " The widget publishes photo_captured and "
                                "video_recorded events. Original "
                                "implementation reference: Infania's "
                                "component library."
                            )
                        ),
                        Row(
                            children=[
                                Label(
                                    text="[View PR #145 on GitHub](https://github.com/invent-framework/invent/pull/145)"
                                ),
                                Label(
                                    text="[Infania's component library](https://infania.pyscriptapps.com/componentize/latest/index.html)"
                                ),
                            ]
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #146: Min/Max Naming Standardization",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text="**Merged: Apr 10, 2026** - +173 / -162 lines - 10 files"
                        ),
                        Label(
                            text=(
                                "Standardized min/max property naming "
                                "across Invent: numeric and date ranges "
                                "now use min_value/max_value; string "
                                "constraints use min_length/max_length. "
                                "Updated property.py, slider.py, "
                                "rating.py, textinput.py, carousel.py, "
                                "and all related tests and examples."
                            )
                        ),
                        Label(
                            text="[View PR #146 on GitHub](https://github.com/invent-framework/invent/pull/146)"
                        ),
                    ],
                ),
                ContentCard(
                    title=("PR #147: Webcam + OpenCV Playground (In Review)"),
                    purpose="WARNING",
                    children=[
                        Label(
                            text="**Open - pending review** - +702 / -112 lines - 9 files"
                        ),
                        Label(
                            text=(
                                "Extends Webcam with a preview_layout "
                                "property (stacked or side-by-side) and "
                                "a show_image() method that pushes any "
                                "data URL into the preview panel. Adds an "
                                "OpenCV Playground example where users "
                                "write Python OpenCV code in a CodeEditor "
                                "and run it against a live camera feed "
                                "using PyScript's Donkey (worker) pattern."
                                " Not yet merged: we are still figuting out"
                                "how to standardized test pages for widgets"
                                "that require developer interaction to test."
                            )
                        ),
                        Label(
                            text="[View PR #147 on GitHub](https://github.com/invent-framework/invent/pull/147)"
                        ),
                    ],
                ),
            ]
        )
    ],
)


# -- Live Demos Page --


demos_page = Page(
    id="demos",
    children=[
        Column(
            children=[
                _nav_header(),
                Label(text="# Live Widget Demos"),
                Label(
                    text=(
                        "The widgets below were contributed this semester."
                        " They are rendered live!"
                    )
                ),
                Label(text="## Rating Widget"),
                Label(
                    text=(
                        "Supports 1, 3, 5, or 10 stars with optional "
                        "half-star precision and read-only mode. "
                        "Click the stars to interact."
                    )
                ),
                Row(
                    children=[
                        Label(text="5-star, half-step (interactive):"),
                        Rating(step="0.5", max_value="5"),
                    ]
                ),
                Row(
                    children=[
                        Label(text="10-star read-only (value 7.5):"),
                        Rating(
                            value=7.5,
                            step="0.5",
                            max_value="10",
                            read_only=True,
                        ),
                    ]
                ),
                Row(
                    children=[
                        Label(text="1-star (like / dislike):"),
                        Rating(
                            value=1,
                            step="1",
                            max_value="1",
                            show_label=False,
                        ),
                    ]
                ),
                Divider(),
                Label(text="## Webcam Widget"),
                Label(
                    text=(
                        "Supports photo, video, and both modes. "
                        "The widget below is in photo mode: press the "
                        "shutter button to capture a still frame."
                    )
                ),
                Webcam(mode="photo"),
            ]
        )
    ],
)


# -- Quotes Page --


quotes_page = Page(
    id="quotes",
    children=[
        Column(
            children=[
                _nav_header(),
                Label(text="# What My Mentors Said"),
                Timeline(
                    children=[
                        ChatBubble(
                            author_name="Nicholas Tollervey",
                            author_image=("https://github.com/ntoll.png"),
                            direction="received",
                            timestamp=datetime(2026, 4, 18),
                            content=(
                                "It has been an absolute joy collaborating with Will. He is a credit to Tufts and, most importantly, to himself.\n\n"
                                "Will engaged with a broad range of open-source development activities, including:\n\n"
                                "- On-boarding into two distinct open-source projects, each with different technical requirements and conventions.\n"
                                "- Autonomously triaging, addressing, testing and submitting improvements to both projects.\n"
                                "- Mentoring a new collaborator (Infania) as they joined the Invent project.\n"
                                "- Engaging with the wider BosPy Python community, with a lightning talk in the works for an upcoming face-to-face meetup.\n"
                                "- Weekly one-to-one meetings in which he was regularly put on the spot to discuss his work, reflect on progress and plan next steps.\n\n"
                                "Will handled all of this with aplomb.\n\n"
                                "For assessment purposes, I want to be direct: over the years I have helped many graduate engineers take their first steps into the software profession, "
                                "and Will stands out. His can-do attitude, his willingness to get stuck in, and his ability to quickly pick up unfamiliar practices, tools and processes "
                                "put him ahead of the majority of those I have worked with at this stage of their careers. I would recommend him without hesitation. He would be an asset "
                                "to any team.\n\n Bravo, Will — I hope you stay in touch with PyScript and keep up the excellent work."
                            ),
                        ),
                        ChatBubble(
                            author_name="Andrea Giammarchi",
                            author_image=(
                                "https://github.com/WebReflection.png"
                            ),
                            direction="received",
                            timestamp=datetime(2026, 4, 18),
                            content=(
                                "My main regret around Will is that I had not enough time to fully collaborate with such a great person.\n\n"
                                "- Will cared about the project\n"
                                "- Will cared about the users\n"
                                "- Will helped tackle bugs without making too many assumptions, always asking for feedback and producing meticulous examples to help find or fix issues.\n"
                                "- Will suggested changes even in projects he only recently encountered, showing both curiosity and the initiative I value in contributors.\n\n"
                                "I wish Will the best in anything he's pursuing because I am sure both attitude and skills are there and future collaborators will rarely be disappointed if Will keeps up the great work."
                            ),
                        ),
                        ChatBubble(
                            author_name="Chris Rogers",
                            author_image=(
                                "https://engineering.tufts.edu/me/sites/g/files/lrezom586/files/styles/large/public/crogers.png?itok=xUgfCQPh"
                            ),
                            direction="received",
                            timestamp=datetime(2026, 4, 21),
                            content=(
                                "Will has done a great job of jumping into the"
                                " deep end, learning on his own, and developing "
                                "many substantive changes to a new open source "
                                "library aimed at making interactive web pages easier "
                                "to build.  He has learned how one works in the open "
                                "source world, from effective GitHub use to interacting "
                                "with the local Python group."
                            ),
                        ),
                    ]
                ),
            ]
        )
    ],
)


# -- Reflection Page --


reflection_page = Page(
    id="reflection",
    children=[
        Column(
            children=[
                _nav_header(),
                Label(text="# Reflection"),
                Label(text="Tufts CS practicum reflection questions."),
                Accordion(
                    children=[
                        Column(
                            name=("1. What did you learn technically?"),
                            children=[
                                Label(
                                    text="This semester my proficiency "
                                    "in Python improved significantly. I now "
                                    "understand more about dunder methods, different "
                                    "applications of data structures, and passing variable "
                                    "parameters to functions. I also learned a lot about the "
                                    "DOM and JavaScript engines. In addition, the differences "
                                    "in capabilities between Python and MicroPython became "
                                    "much clearer."
                                ),
                            ],
                        ),
                        Column(
                            name=("2. What did you learn professionally?"),
                            children=[
                                Label(
                                    text="Professionally, I developed my skills with "
                                    "Git, including writing pull requests and contributing "
                                    "to  open-source projects. I also gained experience "
                                    "writing test cases in both Python and JavaScript, where "
                                    "I learned how to verify changes in the DOM and ensure "
                                    "that classes and properties were applied correctly. In "
                                    "addition at the beginning of the semester, I also learned "
                                    "how to use Figma to prototype and demo a feature I was "
                                    "considering adding to PyScript."
                                ),
                            ],
                        ),
                        Column(
                            name=(
                                "3. What do you wish your supervisor(s) "
                                "did differently?"
                            ),
                            children=[
                                Label(
                                    text="I have no complaints about my advisors/mentors "
                                    "this semester. Nicholas was outstanding; at the beginning "
                                    "of the semester he walked me through both the PyScript and "
                                    "the Invent codebases, showing me how each project is built "
                                    "and deployed. He even sat with me while he pushed a new "
                                    "release of PyScript, allowing me to see the process of "
                                    "updating the production code, documentation, and GitHub "
                                    "Actions usage. Throughout the semester, both he and Chris "
                                    "took time out of their very busy schedules to have a weekly "
                                    "meeting with me. These meetings allowed me to voice my "
                                    "questions and have discussions with folks on call about "
                                    "goals for the week and other code questions."
                                ),
                            ],
                        ),
                        Column(
                            name=(
                                "4. What would you have done " "differently?"
                            ),
                            children=[
                                Label(
                                    text="If I were to redo this semester, I would spend "
                                    "more time during winter break preparing for the Python and "
                                    "browser-related work I encountered. I think it would have "
                                    "been helpful to read more about the DOM and how web pages "
                                    "are structured in order to better understand some of the "
                                    "initial PyScript bugs I worked to resolve. That said, Nicholas "
                                    "did an excellent job helping me learn new Python concepts, "
                                    "such as **kwargs."
                                ),
                            ],
                        ),
                        Column(
                            name=(
                                "5. What do you wish Tufts offered that "
                                "would have helped you on the job?"
                            ),
                            children=[
                                Label(
                                    text="In general, I wish Tufts offered more opportunities "
                                    "for students to work on open-source software. This experience "
                                    "has been incredibly valuable to me as a computer science student; "
                                    "I feel that I have learned more this semester about writing "
                                    "pull requests, the importance of testing, how to write "
                                    "maintainable and accessible code, and most importantly the power "
                                    "of a software community. Being able to hear feedback, find bugs, "
                                    "get help, and discuss code with others is a unique and in fact "
                                    "fun experience! It is much more engaging to work on a project "
                                    "like this and interact with professional, motivated software "
                                    "engineers than to sit in a traditional classroom setting."
                                ),
                            ],
                        ),
                    ]
                ),
            ]
        )
    ],
)


# The app!

app = invent.App(
    name="Open Source Report — Spring 2026",
    pages=[
        cover,
        pyscript_page,
        invent_work_page,
        demos_page,
        quotes_page,
        reflection_page,
    ],
)

invent.go()
