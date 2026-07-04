# Connect Vercel (put your site live)

## What this unlocks
Once connected, I can take the site you built with `design-my-site` and put it on
a real, shareable URL, deployed for you, previewed first, and shipped to
production only when you say go. Reads are free; I never push to your live URL
without showing you the preview first.

## The honest boundary
There's one sign-in only you can do (it's your Vercel account). I do everything
else: install the tool, run the sign-in for you, check it worked, and handle the
deploy. I'll never ask for a password or a code, you approve the sign-in in your
own browser.

(For the builder: this connector is added via the `vercel` CLI, which the system
installs and runs `vercel login` for on the owner's machine. That is a deliberate,
labelled exception to connect-a-tool's usual "/mcp in the app" flow. The owner
still performs the sign-in themselves; BOS only runs the install/login commands.)

## Step 1: I add the Vercel CLI + `vercel login` (permission first)
"To put your site live I need to add Vercel. It's a one-time, free sign-in with
your Vercel account. Want me to get it ready?"
On yes, I install the Vercel CLI and run the sign-in for you (on your machine, so
I do it, not you):

    npm i -g vercel
    vercel login

## Step 2: You sign in (the one step that's yours)
`vercel login` opens Vercel's sign-in in your browser. Sign in with the account
you want your site to live under (a new free account is fine) and approve it.
- A free Vercel account is generous and enough to get your site live. I'll say so
  before we start, and flag any cost out loud first.
- If you'd rather not use the browser sign-in, Vercel also accepts a token you
  create in your account settings. I only ever hold it the way the CLI stores it,
  never in your project files or anywhere it could be committed.

## Step 3: I verify it worked
Once you're signed in, I do one small read to prove it's live:

    vercel whoami

If it shows your Vercel username, you're connected. If not, we check you signed
into the right account and try the sign-in once more.

## Step 4: Deploy a preview
The moment it verifies, I deploy a preview first (`vercel`, not production) and
hand you back the preview URL to look over. Production only happens on your
explicit go, and I never announce your site as live until Vercel confirms the
real URL. Putting it live for good is what `launch-my-site` walks you through,
preview first, production on your say-so.
