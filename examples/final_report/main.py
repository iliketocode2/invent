"""
Open Source Contributions Report, Spring 2026.
Tufts University CS — built with the Invent framework.
"""

import invent
from invent.ui import *
from datetime import datetime

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


def _link(text, url):
    """Return an Html widget that renders an external hyperlink."""
    return Html(
        html=(
            f'<a href="{url}" target="_blank"'
            f' rel="noopener noreferrer">{text}</a>'
        )
    )


def _pr_meta(merged_or_status, additions, deletions, files):
    """
    Return an Html widget showing PR metadata as a single line.

    merged_or_status: e.g. 'Merged: Apr 3, 2026' or 'Open — in review'
    """
    return Html(
        html=(
            f"<p><strong>{merged_or_status}</strong>"
            f" &nbsp;&bull;&nbsp; +{additions} / -{deletions} lines"
            f" &nbsp;&bull;&nbsp; {files} files</p>"
        )
    )


# -- Cover Page --


cover = Page(
    id="cover",
    children=[
        Column(
            children=[
                _nav_header(),
                Html(html="<h1>Open Source Contributions Report</h1>"),
                Html(
                    html=(
                        "<p>Spring 2026 &mdash; Tufts University CS<br>"
                        "William Goldman &nbsp;&bull;&nbsp; "
                        '<a href="https://github.com/iliketocode2"'
                        ' target="_blank" rel="noopener noreferrer">'
                        "@iliketocode2</a></p>"
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
                Html(html="<h2>Semester at a Glance</h2>"),
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
                Html(html="<h1>PyScript Contributions</h1>"),
                Html(
                    html=(
                        "<p>PyScript enables Python in the browser. "
                        "19,000+ GitHub stars, maintained by Anaconda. "
                        '<a href="https://pyscript.net/" target="_blank"'
                        ' rel="noopener noreferrer">pyscript.net</a></p>'
                    )
                ),
                Html(html="<h2>Merged Pull Requests</h2>"),
                ContentCard(
                    title=("PR #2447: Enable str to be appended to Element"),
                    purpose="SUCCESS",
                    children=[
                        _pr_meta("Merged: Feb 4, 2026", 33, 5, 2),
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
                        _link(
                            "View PR #2447 on GitHub",
                            "https://github.com/pyscript/pyscript"
                            "/pull/2447",
                        ),
                    ],
                ),
                ContentCard(
                    title=("PR #2455: Fix ElementCollection.update_all"),
                    purpose="SUCCESS",
                    children=[
                        _pr_meta("Merged: Feb 25, 2026", 47, 4, 2),
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
                                _link(
                                    "View PR #2455 on GitHub",
                                    "https://github.com/pyscript/pyscript"
                                    "/pull/2455",
                                ),
                                _link(
                                    "Docs PR #214",
                                    "https://github.com/pyscript/docs"
                                    "/pull/214",
                                ),
                            ]
                        ),
                    ],
                ),
                Html(html="<h2>Discussion Started</h2>"),
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
                        _link(
                            "View Discussion #2453 on GitHub",
                            "https://github.com/pyscript/pyscript"
                            "/discussions/2453",
                        ),
                    ],
                ),
                Html(html="<h2>Community Issue Triage</h2>"),
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
                                _link(
                                    "View Issue #2466 on GitHub",
                                    "https://github.com/pyscript/pyscript"
                                    "/issues/2466",
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
                                _link(
                                    "View Issue #2464 on GitHub",
                                    "https://github.com/pyscript/pyscript"
                                    "/issues/2464",
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
                Html(html="<h1>Invent Contributions</h1>"),
                Html(
                    html=(
                        "<p>Invent is a Python-first browser app framework"
                        " built on PyScript. The page you are reading "
                        "right now is itself an Invent app! Invent is" \
                        "originally created by Nicholas Tollervey. "
                        '<a href="https://inventframework.org/"'
                        ' target="_blank" rel="noopener noreferrer">'
                        "inventframework.org</a></p>"
                    )
                ),
                Html(html="<h2>Merged Pull Requests</h2>"),
                ContentCard(
                    title="PR #142: Divider Widget",
                    purpose="SUCCESS",
                    children=[
                        _pr_meta("Merged: Mar 10, 2026", 84, 7, 4),
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
                        _link(
                            "View PR #142 on GitHub",
                            "https://github.com/invent-framework"
                            "/invent/pull/142",
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #143: Rating Widget (v1)",
                    purpose="SUCCESS",
                    children=[
                        _pr_meta("Merged: Mar 10, 2026", 327, 6, 4),
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
                        _link(
                            "View PR #143 on GitHub",
                            "https://github.com/invent-framework"
                            "/invent/pull/143",
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #144: Rating Widget (v2 — Fixes)",
                    purpose="SUCCESS",
                    children=[
                        _pr_meta("Merged: Mar 16, 2026", 76, 65, 3),
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
                        _link(
                            "View PR #144 on GitHub",
                            "https://github.com/invent-framework"
                            "/invent/pull/144",
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #145: Webcam Widget",
                    purpose="SUCCESS",
                    children=[
                        _pr_meta("Merged: Apr 3, 2026", 693, 2, 5),
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
                                _link(
                                    "View PR #145 on GitHub",
                                    "https://github.com/invent-framework"
                                    "/invent/pull/145",
                                ),
                                _link(
                                    "Infania's component library",
                                    "https://infania.pyscriptapps.com"
                                    "/componentize/latest/index.html",
                                ),
                            ]
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #146: Min/Max Naming Standardization",
                    purpose="SUCCESS",
                    children=[
                        _pr_meta("Merged: Apr 10, 2026", 173, 162, 10),
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
                        _link(
                            "View PR #146 on GitHub",
                            "https://github.com/invent-framework"
                            "/invent/pull/146",
                        ),
                    ],
                ),
                ContentCard(
                    title=("PR #147: Webcam + OpenCV Playground (In Review)"),
                    purpose="WARNING",
                    children=[
                        Html(
                            html=(
                                "<p><strong>Open — pending review"
                                "</strong> &nbsp;&bull;&nbsp;"
                                " +702 / -112 lines"
                                " &nbsp;&bull;&nbsp; 9 files</p>"
                            )
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
                        _link(
                            "View PR #147 on GitHub",
                            "https://github.com/invent-framework"
                            "/invent/pull/147",
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
                Html(html="<h1>Live Widget Demos</h1>"),
                Label(
                    text=(
                        "The widgets below were contributed this semester."
                        " They are rendered live!"
                    )
                ),
                Html(html="<h2>Rating Widget</h2>"),
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
                Html(html="<h2>Webcam Widget</h2>"),
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
                Html(html="<h1>What My Mentors Said</h1>"),
                Alert(
                    title="Quotes coming soon",
                    text=(
                        "Actual quotes will be added once gathered. "
                        "The speech bubbles below are placeholders."
                    ),
                    purpose="WARNING",
                    dismissable=True,
                ),
                Timeline(
                    children=[
                        ChatBubble(
                            author_name="Nicholas Tollervey",
                            author_image=("https://github.com/ntoll.png"),
                            direction="received",
                            timestamp=datetime(2026, 4, 18),
                            content=(
                                "[Quote from Nicholas Tollervey — "
                                "Invent creator and PyScript core "
                                "contributor. To be added.]"
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
                                "[Quote from Andrea Giammarchi — "
                                "PyScript core maintainer. To be added.]"
                            ),
                        ),
                        ChatBubble(
                            author_name="Infania",
                            direction="received",
                            timestamp=datetime(2026, 4, 18),
                            content=(
                                "[Quote from Infania — contributor whose "
                                "webcam component library served as the "
                                "reference for PR #145. To be added.]"
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
                Html(html="<h1>Reflection</h1>"),
                Label(text="Tufts CS practicum reflection questions."),
                Accordion(
                    children=[
                        Column(
                            name=("1. What did you learn technically?"),
                            children=[
                                Label(text="This semester my proficiency "
                                "in Python improved significantly. I now "
                                "understand more about dunder methods, different "
                                "applications of data structures, and passing variable "
                                "parameters to functions. I also learned a lot about the "
                                "DOM and JavaScript engines. In addition, the differences "
                                "in capabilities between Python and MicroPython became "
                                "much clearer."),
                            ],
                        ),
                        Column(
                            name=("2. What did you learn professionally?"),
                            children=[
                                Label(text="Professionally, I developed my skills with " \
                                "Git, including writing pull requests and contributing " \
                                "to  open-source projects. I also gained experience " \
                                "writing test cases in both Python and JavaScript, where " \
                                "I learned how to verify changes in the DOM and ensure " \
                                "that classes and properties were applied correctly. In " \
                                "addition at the beginning of the semester, I also learned " \
                                "how to use Figma to prototype and demo a feature I was " \
                                "considering adding to PyScript."),
                            ],
                        ),
                        Column(
                            name=(
                                "3. What do you wish your supervisor(s) "
                                "did differently?"
                            ),
                            children=[
                                Label(text="I have no complaints about my advisors/mentors " \
                                "this semester. Nicholas was outstanding; at the beginning " \
                                "of the semester he walked me through both the PyScript and " \
                                "the Invent codebases, showing me how each project is built "
                                "and deployed. He even sat with me while he pushed a new " \
                                "release of PyScript, allowing me to see the process of " \
                                "updating the production code, documentation, and GitHub " \
                                "Actions usage. Throughout the semester, both he and Chris " \
                                "took time out of their very busy schedules to have a weekly " \
                                "meeting with me. These meetings allowed me to voice my " \
                                "questions and have discussions with folks on call about " \
                                "goals for the week and other code questions."),
                            ],
                        ),
                        Column(
                            name=(
                                "4. What would you have done " "differently?"
                            ),
                            children=[
                                Label(text="If I were to redo this semester, I would spend " \
                                "more time during winter break preparing for the Python and " \
                                "browser-related work I encountered. I think it would have " \
                                "been helpful to read more about the DOM and how web pages " \
                                "are structured in order to better understand some of the " \
                                "initial PyScript bugs I worked to resolve. That said, Nicholas " \
                                "did an excellent job helping me learn new Python concepts, " \
                                "such as **kwargs."),
                            ],
                        ),
                        Column(
                            name=(
                                "5. What do you wish Tufts offered that "
                                "would have helped you on the job?"
                            ),
                            children=[
                                Label(text="In general, I wish Tufts offered more opportunities " \
                                "for students to work on open-source software. This experience " \
                                "has been incredibly valuable to me as a computer science student; " \
                                "I feel that I have learned more this semester about writing " \
                                "pull requests, the importance of testing, how to write " \
                                "maintainable and accessible code, and most importantly the power " \
                                "of a software community. Being able to hear feedback, find bugs, " \
                                "get help, and discuss code with others is a unique and in fact " \
                                "fun experience! It is much more engaging to work on a project " \
                                "like this and interact with professional, motivated software " \
                                "engineers than to sit in a traditional classroom setting."),
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
