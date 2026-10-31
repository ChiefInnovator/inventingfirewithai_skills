# Traveler onboarding and private preferences

## First use: three starter questions

A skill is reusable instructions and bundled resources, not an automatic database or install-time hook. Run onboarding on the first invocation when no usable traveler profile exists. Do not claim installation itself ran onboarding. Read supplied context first; do not repeat answered questions. Ask the three prompts below together, replacing already answered prompts with a short acknowledgment. Accept partial answers, “skip,” and “not sure.” If the user needs immediate help, solve the urgent request first and defer nonessential onboarding.

1. **Trip:** “Where are you going, when, and who is traveling?”
2. **Experience:** “What would make the trip great for you—food, culture, relaxation, adventure, nightlife, or something else—and what pace and budget feel comfortable?”
3. **Practical fit:** “What should I account for, such as food restrictions, accessibility, transport, lodging needs, or fixed commitments, and may I remember your preferences for future trips?”

Keep the three prompts brief; examples are optional, not a demand to answer every field. After the answers, give a useful first recommendation or plan. Offer: “I can tailor this further with a few optional questions, or we can start here.” Ask additional questions only if the user opts in or a missing fact is essential to the requested action. Optional topics include coffee/tea, cuisines, local-versus-famous venues, walking distance or steps, hotel brands and loyalty, nightlife, photography, language, budget details, and work or fitness needs. Ask in small relevant batches, not an exhaustive questionnaire.

## Separate instructions, preferences, and trip state

- Keep shared skill files destination-independent and free of personal defaults. Do not embed a real traveler's name, diet targets, companions, map preference, booking authorizations, or history in the distributed package.
- Store reusable preferences in the current user's private profile, only with their permission. Keep current trip dates, locations, companions, reservations, and statuses in a separate trip record; do not turn them into permanent preferences.
- Load the profile when available. Apply current explicit instructions first, then current trip constraints, then saved preferences. Treat inferred preferences as tentative and never as consent to book or spend.
- Preserve provenance and last-updated date; distinguish stated, observed, and inferred information. Do not overwrite a newer correction with an old summary. Unknown means unknown, not an inherited sample value.

## Persistence across hosts

Discover an authorized private storage capability before promising retention. Prefer the host's user-scoped memory or private document storage. A profile file in a skill directory or public repository is not private storage and may be redistributed or overwritten by updates.

- With consent and a supported private store, create or update one profile and retain the store's returned identifier in that user's private context. Search the user's existing profile before creating another; use a stable descriptive title such as “Travel preferences.” Read the latest version before edits and preserve unrelated fields.
- For a filesystem-only host, use a user-approved private location outside repositories and installed skill folders. Do not assume that local files survive sessions or synchronize across agents. Avoid secrets and unnecessary identity data; restrict file access where supported.
- Without durable storage, use conversation context and state plainly that cross-session retention is unavailable. Offer a portable profile only when wanted. Do not claim a save succeeded without a successful write.
- Do not invent a universal storage API, install hook, automatic cross-harness profile sync, or identity mapping. Each installation resolves its own authorized user's profile. Share generic instructions across harnesses; transfer private preferences only at the user's request through an appropriate private channel.
- Allow the user to review, correct, or delete saved preferences. Declining persistence must not block travel help. Store only approved fields; do not save passport/payment credentials, booking access codes, precise location history, or companions' private details in the preference profile.

## Minimal profile structure

Use the native store's format; these are optional fields, not mandatory questions:

- schema_version: 1
- updated_at: actual timestamp
- persistence_consent: scope and date of the user's approval
- preferences: interests, pace, budget/currency, food needs, mobility/transport, lodging, language, navigation, fitness/work, communication
- evidence: for each populated preference, source/date and stated/observed/inferred status

Keep missing fields absent or null. Keep transaction authorizations scoped to the relevant request or explicitly stated standing instruction, with their limits; never create blanket consent for other users.
