## 5 — Monitor and address automatic review

Read [GitHub review workflow](github-review.md) for automatic-review evidence, pagination, replies, and thread resolution. Fetch all review summaries, inline comments, issue comments, and review threads. Determine actual identities from returned records; don't filter out feedback based on one remembered bot login.

If the user explicitly says not to wait for AI review, record that instruction and continue after local review and all mandatory GitHub checks; do not poll an optional review or call it completed. This never waives platform-enforced approvals, unresolved human feedback, or branch protections.

Otherwise, confirm the required reviewer actually completed a review on `SLAM_HEAD`; a request, pending review, quota refusal, or summary saying review was skipped is not completed review. Triage each comment: fix valid in-scope findings, reply with evidence when declining, and document out-of-scope findings without expanding the PR. Resolve only handled threads; an unresolved human disagreement is not yours to dismiss. Preserve required human approvals/change requests.

After real fixes, commit, verify, push, capture the new `SLAM_HEAD`, and wait for its automatic review only when that gate still applies. Every new commit, including a base merge, invalidates earlier head-specific review/check evidence. Never request a review or manufacture a push. Do not turn duplicate bot comments into an endless fix loop: compare prior responses and escalate substantive disagreements. Silence is never approval.

If AI review is unavailable or explicitly refuses the PR (for example a size limit), report that accurately. Stop if AI review is required by user/repository policy. If optional, continue only after completing local review and all required gates, recording the absence. A pending review stays pending; do not label it unavailable merely because it is slow.
