# Traveler onboarding and private preferences

## First personalized trip

Read supplied context and an available authorized profile first. When personalized trip planning needs a profile, ask these three brief starter questions, acknowledging answers already supplied. Accept partial answers, “skip,” and undecided destinations or dates. General advice, menu translation, and urgent help do not require onboarding; solve those requests first.

1. **Trip:** “Where are you going, when, and who is traveling?”
2. **Experience:** “What would make the trip great, and what pace and budget feel comfortable?”
3. **Practical fit:** “What food, accessibility, transport, lodging, or fixed commitments matter, and may I remember your travel preferences?”

Give a useful first plan after the answers. Offer optional follow-ups only when useful; ask them in small relevant batches if the user opts in or a missing fact is essential. Topics may include interests, cuisines, walking limits or steps, lodging, language, navigation, work, or fitness. Do not repeat destination/date questions or treat every example as a required field.

## Separate shared instructions, preferences, and trip state

- Keep shared skills free of a real traveler's personal defaults, name, diet targets, companions, navigation choice, booking authorizations, and history. Choose recommendations from the current request and authorized profile, not an embedded sample traveler.
- Keep reusable preferences separate from current trip dates, locations, companions, reservations, and statuses. Apply current explicit instructions, then current trip constraints, then saved preferences. Inferred preferences remain tentative and never authorize transactions.
- Preserve source, date, and stated/observed/inferred status for saved preferences. Do not overwrite a newer correction with an old summary. Missing fields stay unknown.

## Private persistence

Discover an authorized private storage capability before promising retention. Save only on the user's explicit request or consent. A skill folder or repository is not private profile storage.

- Search for the user's existing profile before creating another. Read its latest version before edits, preserve unrelated fields, and retain the store's returned identifier in private user context. Do not claim a save succeeded without a successful write.
- With a filesystem-only host, use a user-approved private location outside repositories and installed skills; restrict access where supported. Do not assume files survive sessions or synchronize across hosts. If durable storage is unavailable, use conversation context and disclose the retention limit.
- Do not invent a universal storage API, install hook, identity mapping, or automatic profile synchronization. Transfer private preferences between hosts only at the user's request through an appropriate private channel.
- Let the user review, correct, or delete saved preferences. Declining persistence must not block travel help. Avoid passport/payment credentials, booking codes, precise location history, and companions' private details.

Use the native store's format. Optional profile fields are schema version, actual update time, consent scope/date, relevant preferences, and evidence for each preference. Keep transaction authorizations with their actual scope and limits; never create blanket consent.
