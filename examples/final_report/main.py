"""
Open Source Contributions Report — Spring 2026, Tufts University CS.
Built with Invent — one of the two projects contributed to this semester.
"""

import invent
from invent.ui import *
from datetime import datetime

# -- Navigation --


def navigate(message):
    """Route 'navigate' channel press events to the named page."""
    page_id = message.source.name.split("_btn")[0]
    invent.show_page(page_id)


invent.subscribe(navigate, to_channel="navigate", when_subject=["press"])


def _btn(label, page_id, purpose="PRIMARY"):
    """Return a navigation Button that targets the given page ID."""
    return Button(
        text=label,
        name=f"{page_id}_btn",
        purpose=purpose,
        channel="navigate",
    )


# -- Cover Page --


cover = Page(
    id="cover",
    children=[
        Column(
            children=[
                Label(
                    text=(
                        "# Open Source Contributions Report\n\n"
                        "**Spring 2026 · Tufts University CS**\n\n"
                        "William Goldman · "
                        "[@iliketocode2]"
                        "(https://github.com/iliketocode2)"
                    )
                ),
                Alert(
                    title="About This Report",
                    text=(
                        "This report is itself an **Invent** application "
                        "— one of the two open-source projects I worked on "
                        "this semester. Use the buttons below to navigate "
                        "between sections."
                    ),
                    purpose="PRIMARY",
                ),
                Row(
                    children=[
                        _btn("PyScript Work", "pyscript"),
                        _btn("Invent Work", "invent_work"),
                        _btn("Live Demos", "demos"),
                        _btn("Mentors Say...", "quotes"),
                        _btn("Reflection", "reflection"),
                    ]
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
                    label="Contribution Summary · Spring 2026",
                ),
                Alert(
                    title="Two Projects, One Semester",
                    text=(
                        "**PyScript** is Anaconda's platform for running "
                        "Python in the browser (19k+ GitHub stars). "
                        "**Invent** is a Python-first browser app framework "
                        "built on top of PyScript. Both are maintained by "
                        "many of the same people, which made contributing "
                        "to both a uniquely cohesive experience."
                    ),
                    purpose="SECONDARY",
                ),
            ]
        )
    ],
)


# -- PyScript Page --


pyscript = Page(
    id="pyscript",
    children=[
        Column(
            children=[
                Label(
                    text=(
                        "# PyScript Contributions\n\n"
                        "[PyScript](https://pyscript.net/) lets you run "
                        "Python directly in the browser. It has 19,000+ "
                        "GitHub stars and is maintained by Anaconda."
                    )
                ),
                Row(
                    children=[
                        _btn("← Home", "cover", "SECONDARY"),
                        _btn("Invent Work →", "invent_work"),
                    ]
                ),
                Label(text="## Merged Pull Requests"),
                ContentCard(
                    title=("PR #2447 · Enable str to be appended to Element"),
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text=(
                                "**Merged:** Feb 4, 2026 "
                                "· +33 / −5 lines · 2 files changed\n\n"
                                "Extended `Element.append()` in "
                                "`pyscript/web.py` to accept plain strings "
                                "(and other primitives). Previously, passing "
                                "a string raised a `TypeError`. The fix "
                                "delegates to the browser's native DOM "
                                "`append()`, which creates a text node — "
                                "preserving CSS selectors and layout "
                                "performance that would break if a `<span>` "
                                "were used instead.\n\n"
                                "[View PR on GitHub]"
                                "(https://github.com/pyscript/pyscript"
                                "/pull/2447)"
                            )
                        ),
                        Code(
                            code=(
                                "# The final fix — native DOM append\n"
                                "# handles primitives as text nodes:\n"
                                "elif isinstance(item, "
                                "(str, int, float, bool)):\n"
                                "    self._dom_element.append(item)"
                            )
                        ),
                    ],
                ),
                ContentCard(
                    title=("PR #2455 · Fix ElementCollection.update_all"),
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text=(
                                "**Merged:** Feb 25, 2026 "
                                "· +47 / −4 lines · 2 files changed\n\n"
                                "`update_all` was using `setattr()` "
                                "directly, bypassing `Element.update()`'s "
                                "class and style handling. Passing "
                                "`classes='active'` via `update_all` would "
                                "overwrite the attribute instead of calling "
                                "`self.classes.add()`. This PR routes all "
                                "calls through `element.update()` — fixing "
                                "the bug and removing duplicated logic.\n\n"
                                "Corresponding docs PR: "
                                "[pyscript/docs #214]"
                                "(https://github.com/pyscript/docs"
                                "/pull/214)\n\n"
                                "[View PR on GitHub]"
                                "(https://github.com/pyscript/pyscript"
                                "/pull/2455)"
                            )
                        ),
                    ],
                ),
                Label(text="## Discussion Started"),
                ContentCard(
                    title=(
                        "Discussion #2453 · "
                        "Improving ElementCollection.update_all"
                    ),
                    purpose="PRIMARY",
                    children=[
                        Label(
                            text=(
                                "Before opening PR #2455, I started a "
                                "public design discussion to confirm the "
                                "approach with maintainers Nicholas Tollervey"
                                " and Andrea Giammarchi. The thread also "
                                "surfaced a broader question about whether "
                                "PyScript's web API should stay 'Pythonic' "
                                "(sets/dicts for classes/styles) or lean "
                                "into native DOM APIs like `classList` — a "
                                "debate that reflects the core tension in "
                                "PyScript's design philosophy.\n\n"
                                "[View Discussion]"
                                "(https://github.com/pyscript/pyscript"
                                "/discussions/2453)"
                            )
                        ),
                    ],
                ),
                Label(text="## Community Issue Triage"),
                Accordion(
                    children=[
                        Column(
                            name=(
                                "Issue #2466 · "
                                "Try block indentation inconsistency"
                            ),
                            children=[
                                Label(
                                    text=(
                                        "A user reported that `try` blocks "
                                        "inside `<script type='py'>` tags "
                                        "failed unless indented with tabs. "
                                        "I investigated, traced the behaviour "
                                        "to the [codedent]"
                                        "(https://github.com/WebReflection"
                                        "/codedent) library's first-line "
                                        "strip logic, and explained why it "
                                        "is consistent with Python's own "
                                        "indentation rules. The issue was "
                                        "resolved as expected behaviour, not "
                                        "a bug in PyScript itself.\n\n"
                                        "[View Issue]"
                                        "(https://github.com/pyscript/pyscript"
                                        "/issues/2466)"
                                    )
                                ),
                            ],
                        ),
                        Column(
                            name=(
                                "Issue #2464 · "
                                "Matplotlib regression in py-editor"
                            ),
                            children=[
                                Label(
                                    text=(
                                        "A user found that matplotlib stopped"
                                        " rendering in `py-editor` after "
                                        "PyScript 2025.8.1. I diffed the "
                                        "releases and traced the regression "
                                        "to a change in `ffi.py` that "
                                        "replaced `value is None` checks "
                                        "with a `jsnull` comparison. In a "
                                        "worker context, JS null values were "
                                        "arriving as `jsnull` instead of "
                                        "`None`, causing null checks to fail "
                                        "silently. Maintainer Andrea "
                                        "Giammarchi confirmed the root cause "
                                        "and referenced the "
                                        "`pyscript.ffi.is_none` API that was "
                                        "added as a mitigation.\n\n"
                                        "[View Issue]"
                                        "(https://github.com/pyscript/pyscript"
                                        "/issues/2464)"
                                    )
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


invent_work = Page(
    id="invent_work",
    children=[
        Column(
            children=[
                Label(
                    text=(
                        "# Invent Contributions\n\n"
                        "[Invent](https://inventframework.org/) is a "
                        "Python-first browser app framework built on "
                        "PyScript. This page you are reading right now "
                        "is itself an Invent app."
                    )
                ),
                Row(
                    children=[
                        _btn("← PyScript", "pyscript", "SECONDARY"),
                        _btn("Live Demos →", "demos"),
                    ]
                ),
                Label(text="## Merged Pull Requests"),
                ContentCard(
                    title="PR #142 · Divider Widget",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text=(
                                "**Merged:** Mar 10, 2026 "
                                "· +84 / −7 lines · 4 files\n\n"
                                "Added a `Divider` widget that separates "
                                "items in a `Row` (vertical) or a `Column` "
                                "(horizontal). The challenge: `render()` is "
                                "called before `_parent` is assigned, so "
                                "orientation cannot be determined at render "
                                "time. Solved by overriding the `parent` "
                                "setter and resolving orientation there.\n\n"
                                "[View PR]"
                                "(https://github.com/invent-framework"
                                "/invent/pull/142)"
                            )
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #143 · Rating Widget (v1)",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text=(
                                "**Merged:** Mar 10, 2026 "
                                "· +327 / −6 lines · 4 files\n\n"
                                "Added a `Rating` widget with half-star "
                                "precision. Each star is split into "
                                "invisible left and right click zones: "
                                "clicking the left half scores `i − 0.5`, "
                                "the right scores `i`. Supports 3, 5, or "
                                "10 stars, read-only mode, and a brief "
                                "popup animation when the value changes.\n\n"
                                "[View PR]"
                                "(https://github.com/invent-framework"
                                "/invent/pull/143)"
                            )
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #144 · Rating Widget (v2 — Fixes)",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text=(
                                "**Merged:** Mar 16, 2026 "
                                "· +76 / −65 lines · 3 files\n\n"
                                "Follow-up refinements to the Rating "
                                "widget: added 1-star support, zero-star "
                                "selection, configurable step size as a "
                                "`ChoiceProperty`, an optional numeric "
                                "label, and a cursor-pointer hover effect "
                                "on 1-star mode.\n\n"
                                "[View PR]"
                                "(https://github.com/invent-framework"
                                "/invent/pull/144)"
                            )
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #145 · Webcam Widget",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text=(
                                "**Merged:** Apr 3, 2026 "
                                "· +693 / −2 lines · 5 files\n\n"
                                "Added a `Webcam` widget with three modes:"
                                " `photo`, `video`, and `both`. Uses "
                                "`getUserMedia()` for the live feed, a "
                                "hidden `<canvas>` for frame capture (via "
                                "`drawImage()`), and `MediaRecorder` for "
                                "video. Captured media is downloaded via a "
                                "temporary `<a>` element. The widget also "
                                "publishes `photo_captured` and "
                                "`video_recorded` events for reactive use."
                                "\n\nOriginal implementation reference: "
                                "[Infania's component library]"
                                "(https://infania.pyscriptapps.com"
                                "/componentize/latest/index.html)\n\n"
                                "[View PR]"
                                "(https://github.com/invent-framework"
                                "/invent/pull/145)"
                            )
                        ),
                    ],
                ),
                ContentCard(
                    title="PR #146 · Min/Max Naming Standardization",
                    purpose="SUCCESS",
                    children=[
                        Label(
                            text=(
                                "**Merged:** Apr 10, 2026 "
                                "· +173 / −162 lines · 10 files\n\n"
                                "Standardized min/max property naming "
                                "across Invent: numeric and date ranges "
                                "now use `min_value`/`max_value`; string "
                                "constraints use `min_length`/`max_length`."
                                " Updated `property.py`, `slider.py`, "
                                "`rating.py`, `textinput.py`, `carousel.py`"
                                ", and all related tests and examples.\n\n"
                                "[View PR]"
                                "(https://github.com/invent-framework"
                                "/invent/pull/146)"
                            )
                        ),
                    ],
                ),
                ContentCard(
                    title=(
                        "PR #147 · Webcam + OpenCV Playground " "(In Review)"
                    ),
                    purpose="WARNING",
                    children=[
                        Label(
                            text=(
                                "**Status:** Open — pending review\n"
                                "+702 / −112 lines · 9 files changed\n\n"
                                "Extends `Webcam` with a `preview_layout` "
                                "property (`stacked` | `side-by-side`) and "
                                "a `show_image()` method that pushes any "
                                "data URL into the preview panel. Also adds"
                                " an **OpenCV Playground** example: users "
                                "write Python OpenCV code in a `CodeEditor`"
                                " widget and run it against a live camera "
                                "feed using PyScript's Donkey (worker) "
                                "pattern.\n\n"
                                "**Not yet ready to merge:** the OpenCV "
                                "example page needs to be separated from "
                                "the widget changes before merging.\n\n"
                                "[View PR]"
                                "(https://github.com/invent-framework"
                                "/invent/pull/147)"
                            )
                        ),
                    ],
                ),
            ]
        )
    ],
)


# -- Live Demos Page --


demos = Page(
    id="demos",
    children=[
        Column(
            children=[
                Label(text="# Live Widget Demos"),
                Label(
                    text=(
                        "The widgets below were contributed this semester. "
                        "They are rendered live — this is not a screenshot."
                    )
                ),
                Row(
                    children=[
                        _btn("← Invent Work", "invent_work", "SECONDARY"),
                        _btn("Mentors Say... →", "quotes"),
                    ]
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
                        Label(text="10-star read-only (value: 7.5):"),
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
                        "Supports `photo`, `video`, and `both` modes. "
                        "The widget below is in `photo` mode — press the "
                        "shutter button to capture a still frame."
                    )
                ),
                Webcam(mode="photo"),
            ]
        )
    ],
)


# -- Quotes Page --


quotes = Page(
    id="quotes",
    children=[
        Column(
            children=[
                Label(text="# What My Mentors Said"),
                Alert(
                    title="Placeholders",
                    text=(
                        "Actual quotes will be added here once gathered. "
                        "The speech bubbles below use placeholder text."
                    ),
                    purpose="WARNING",
                    dismissable=True,
                ),
                Row(
                    children=[
                        _btn("← Live Demos", "demos", "SECONDARY"),
                        _btn("Reflection →", "reflection"),
                    ]
                ),
                Timeline(
                    children=[
                        ChatBubble(
                            author_name="Nicholas Tollervey",
                            author_image=("https://github.com/ntoll.png"),
                            direction="received",
                            timestamp=datetime(2026, 4, 18),
                            content=(
                                "*[Quote from Nicholas Tollervey "
                                "(ntoll) — Invent maintainer and "
                                "PyScript core contributor. "
                                "To be added.]*"
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
                                "*[Quote from Andrea Giammarchi "
                                "(WebReflection) — PyScript core "
                                "maintainer. To be added.]*"
                            ),
                        ),
                        ChatBubble(
                            author_name="Chris [TBD]",
                            direction="received",
                            timestamp=datetime(2026, 4, 18),
                            content=(
                                "*[Quote from Chris — identity to be "
                                "confirmed. To be added.]*"
                            ),
                        ),
                        ChatBubble(
                            author_name="Infania",
                            direction="received",
                            timestamp=datetime(2026, 4, 18),
                            content=(
                                "*[Quote from Infania — contributor "
                                "whose webcam component library served "
                                "as the reference for PR #145. "
                                "To be added.]*"
                            ),
                        ),
                    ]
                ),
            ]
        )
    ],
)


# -- Reflection Page --


reflection = Page(
    id="reflection",
    children=[
        Column(
            children=[
                Label(
                    text=(
                        "# Reflection\n\n"
                        "Tufts CS practicum reflection questions."
                    )
                ),
                Alert(
                    title="Draft — answers not yet filled in",
                    text=(
                        "Replace each placeholder with your own response "
                        "before submitting."
                    ),
                    purpose="WARNING",
                ),
                _btn("← Mentors Say...", "quotes", "SECONDARY"),
                Accordion(
                    children=[
                        Column(
                            name="1. What did you learn technically?",
                            children=[
                                Label(text="*[Your answer here]*"),
                            ],
                        ),
                        Column(
                            name="2. What did you learn professionally?",
                            children=[
                                Label(text="*[Your answer here]*"),
                            ],
                        ),
                        Column(
                            name=(
                                "3. What do you wish your supervisor(s) "
                                "did differently?"
                            ),
                            children=[
                                Label(text="*[Your answer here]*"),
                            ],
                        ),
                        Column(
                            name=("4. What would you have done differently?"),
                            children=[
                                Label(text="*[Your answer here]*"),
                            ],
                        ),
                        Column(
                            name=(
                                "5. What do you wish Tufts offered that "
                                "would have helped you on the job?"
                            ),
                            children=[
                                Label(text="*[Your answer here]*"),
                            ],
                        ),
                    ]
                ),
            ]
        )
    ],
)


# -- App --


app = invent.App(
    name="Open Source Report — Spring 2026",
    pages=[
        cover,
        pyscript,
        invent_work,
        demos,
        quotes,
        reflection,
    ],
)

invent.go()
