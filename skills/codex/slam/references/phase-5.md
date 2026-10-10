## 5 — Obtain and address AI review

Read [GitHub review workflow](github-review.md) for review requests, pagination, replies, and thread resolution. Fetch all review summaries, inline comments, issue comments, and review threads. Determine actual identities from returned records; don't filter out feedback based on one remembered bot login.

Confirm an AI review actually ran on `SLAM_HEAD`. Triage each comment: fix valid in-scope findings, reply with evidence when declining, and document out-of-scope findings without expanding the PR. Resolve only handled threads; an unresolved human disagreement is not yours to dismiss. Preserve required human approvals/change requests.

After fixes, commit, verify, push, and obtain a new review for the new head when available; auto-review may not rerun on pushes. Do not turn duplicate bot comments into an endless fix loop: compare prior responses and escalate substantive disagreements. Silence is never approval.

If AI review is unavailable or explicitly refuses the PR (for example a size limit), report that accurately. Stop if AI review is required by user/repository policy. If optional, continue only after completing local review and all required gates, recording the absence. A pending review stays pending; do not label it unavailable merely because it is slow.
