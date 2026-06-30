# TrustPager Client Platform Guide

> **This file is a Claude Project knowledge base document.** Use it to instruct and train clients on how to use the TrustPager platform.

## Instructions for Claude

**CRITICAL: When answering any question about how to do something on TrustPager, you MUST include the clickable URL from this document.** Never describe a location without linking to it. If a client asks "how do I create a workflow?", respond with the instructions AND the link: [Workflows](https://app.trustpager.com/crm/workflows).

- **Always link to the relevant page** when explaining how to do something
- **Use the exact URLs** from this document — the base URL is `https://app.trustpager.com`
- **For pages with dynamic IDs** (e.g. a specific deal or contact), explain where to navigate and provide the parent page link
- **Always describe button locations** — say where on the page the button is (top-right, within a card, in the toolbar, etc.) and what icon it has
- **Audience:** This guide is for clients (not admins). Clients have access to their own company only
- **Tone:** Friendly, clear, and professional. Assume the client may not be tech-savvy

---

> TrustPager is an all-in-one CRM, automation, and communication hub built for Australian businesses.
>
> **Platform URL:** [https://app.trustpager.com](https://app.trustpager.com)

---

## How To — Quick Reference

Every common action you'll want to take on the platform, with step-by-step instructions.

### CRM

**How to create a workflow:**
1. Go to [Workflows](https://app.trustpager.com/crm/workflows).
2. Click the **dropdown button** (+ icon with a down arrow) in the **top-right corner** of the page header.
3. Choose a template: Inbound Sales, Outbound Sales, Onboarding, or Retention. Or click **"Generate with AI"** to have AI create a custom pipeline.
4. The new workflow opens automatically in Kanban board view.

**How to create a deal:**
1. Go to [Opportunities](https://app.trustpager.com/crm/opportunities).
2. Click the **"Add Deal"** tab (+ icon) in the **top-right** ViewToggle control. The page switches to a create form.
3. Fill in: Deal Name (required), Value, Probability %, Expected Close Date, Lead Source, Workflow, Stage, Account, Contact, and Notes.
4. Click **"Create Deal"** (bottom of the form). You'll be taken to the deal detail page.
5. **Alternative:** From a pipeline Kanban board, click the **"+" button at the bottom of any stage column** to create a deal directly into that stage.

**How to move a deal between stages:**
1. Open a workflow from [Workflows](https://app.trustpager.com/crm/workflows) and click into the pipeline.
2. On the Kanban board, **click and drag a deal card** from one stage column to another.
3. If the target stage has automations, a **confirmation modal** will appear listing what will run.
   - If an automation has **more than one action**, each action is listed with its own toggle beneath the automation row. Untick individual actions to skip them on this move only (the automation still runs -- just those specific actions are bypassed).
   - Click **"Confirm"** to proceed (with any toggles applied) or **"Cancel"** to abort the entire move.

**How to create an account:**
1. Go to [Accounts](https://app.trustpager.com/crm/accounts).
2. Click the **"Add Account"** tab (+ icon) in the **top-right** ViewToggle control.
3. Fill in the two-column form: Left column has Account Name (required), Email, Mobile, Landline, Website, Industry. Right column has Address fields and Notes. Use Mobile for mobile numbers and Landline for office/fixed-line numbers.
4. Click **"Create Account"** at the bottom-right of the form.

**How to create a contact:**
1. Go to [Contacts](https://app.trustpager.com/crm/contacts).
2. Click the **"Add Contact"** tab (+ icon) in the **top-right** ViewToggle control.
3. Fill in: First Name (required), Last Name (required), Email, Mobile (for mobile numbers), Landline (for office/fixed-line numbers), and Notes.
4. Click **"Create Contact"** at the bottom-right. To link this contact to employers, visit the contact detail page after creating.

**How to create a product:**
1. Go to [Products](https://app.trustpager.com/settings/products).
2. Click the **"Add Product"** tab (+ icon) in the **top-right** ViewToggle control.
3. Fill in: Product Name (required), SKU, Price (required), Currency (defaults to AUD), Unit (Once Off, Each, Hour, Month, etc.), Category (Service, Product, Subscription, etc.), Description.
4. Click **"Create Product"** at the bottom-right.

**How to create a task:**
1. Go to [Tasks](https://app.trustpager.com/tasks/tasklist).
2. Click the **"New Task"** button (+ icon) in the **top toolbar / filter card**.
3. A modal appears. Fill in: Title (required), Description, Status (Todo/In Progress/Completed), Priority (Low/Medium/High/Critical), Due Date (with quick shortcuts: Today, Tomorrow, In a week), Assignee, Category/Folder, and optionally link to an Opportunity.
4. Click **"Create"** in the modal footer.
5. **Tip:** You can edit any task field inline by clicking it directly in the table — title, status, priority, due date, and assignee are all editable in-place.

**How to organise tasks into folders:**
1. On the [Tasks](https://app.trustpager.com/tasks/tasklist) page, look at the **left sidebar**.
2. You'll see "All Tasks" and any existing folders with task counts.
3. Click the **"+" button** next to the folder list header to create a new folder.
4. Name it and press Enter. Assign tasks to folders when creating or editing them.

**How to bulk move deals:**
1. Go to [Opportunities](https://app.trustpager.com/crm/opportunities).
2. In the table, **tick the checkboxes** on the left side of each deal you want to move.
3. A bulk action bar appears at the top. Select the target pipeline and stage, then click **"Move"**.

**How to add a tag to an opportunity:**
1. Open any opportunity (deal) detail page at [Opportunities](https://app.trustpager.com/crm/opportunities).
2. In the opportunity header, look for the **Tags** section and click **"+ Add Tag"**.
3. A modal opens. Either:
   - **Type a new tag name** and pick a colour, then click **"Add Tag"** -- the tag is added to the deal and automatically saved to the company tag palette for future quick-picks.
   - **Click an existing tag** from the "Or pick an existing tag" quick-pick strip at the bottom -- instantly applies it and closes the modal.
4. Tags appear as coloured pills on the opportunity card.

**How to set up company-wide tag quick-picks (Tag Palette):**
- The tag palette is built automatically: whenever you create a new tag on any opportunity, it is added to the company-wide palette.

**How to use Product Buckets on an opportunity (group products by area/room):**

Product Buckets let you group line items under named sections on the opportunity Products card (e.g. "Main Bathroom", "Ensuite", "Laundry"). Invoices and estimates render each bucket as a grouped section with its own subtotal.

1. Open any opportunity at [Opportunities](https://app.trustpager.com/crm/opportunities).
2. Scroll to the **Products** card.
3. Click **"Add Product Bucket"** (top-right corner of the Products card).
4. Enter a name (e.g. "Main Bathroom") and save.
5. When adding a product to the deal, use the **bucket dropdown pill** on the line item to assign it to a bucket.
6. To rename a bucket, click its name inline. To delete a bucket, click the trash icon -- line items in that bucket remain on the deal as ungrouped.

**Product Bucket Label presets:** Go to [Settings > CRM](https://app.trustpager.com/settings/crm) and scroll to **Product Bucket Labels** to add workspace-level bucket name presets (quick-pick suggestions when creating a bucket).
- To manage the palette directly via API or MCP, use `GET /company/settings/tag-palette` and `PATCH /company/settings/tag-palette`.

**How to add payer companies (billing parties) to an opportunity:**

A billing party is a separate company that pays the fees for a matter, while the client on the opportunity stays the same. For example: an employer pays an employee's health assessment, or a trust fund pays conveyancing fees. Adding a billing party makes that company's invoices (from your connected accounting integration) appear on the opportunity's Invoices card alongside the client's.

1. Open the opportunity at [Opportunities](https://app.trustpager.com/crm/opportunities).
2. Scroll to the **Invoices** card.
3. In the **Payer companies** section at the bottom of the Invoices card, click **"Add payer"**.
4. Search for the company by name and click to add it. You can also enter an optional note (e.g. "Employer pays LMI").
5. The payer company's unpinned invoices from your accounting integration now surface on this opportunity.
6. To remove a payer, click the **X** next to the company name.

Note: only invoices that are not already pinned to a different opportunity are pulled in. A payer company and its invoices are not deleted when you remove the link.

**How to search and filter any list:**
- Every list page (Accounts, Contacts, Deals, Products, Tasks) has a **search bar at the top** of the table.
- Type to search by name, email, phone, or other relevant fields — results filter in real time.
- Use the **dropdown filters** next to the search bar to narrow by status, category, pipeline, stage, account, etc.

**How to delete a record:**
- In any list view (Accounts, Contacts, Deals, Products), click the **three-dot menu (...)** on the right side of a row.
- Select **"Delete"** (trash icon, red text) from the dropdown.
- Confirm deletion in the modal that appears.
- **Bulk delete:** Tick multiple checkboxes, then use the bulk action bar to delete all selected.

**Archive instead of delete (non-destructive):**
- Opportunities, contacts, and companies can be **archived** rather than deleted. Archiving hides a record from active lists, the pipeline board, and dashboard counts, but keeps it fully searchable, exportable, and instantly restorable. Nothing is removed.
- **To archive:** in the list, click the Archive icon in the action toolbar to enter select mode, tick the records, then click **Archive**.
- **To view or restore:** once anything is archived, an **Archive** button (with a count) appears on the right of the search bar. It opens a searchable browser where you can **Open** or **Restore** each record. You can also Restore from the **Archived** badge at the top of a record's detail page.
- Use archive for records you have finished with but want to keep (e.g. years of completed jobs), and delete only when a record should be removed permanently.

**Deleting an Opportunity (deal) -- what gets removed and what is preserved:**

When you delete an opportunity, a modal appears showing the impact:
- **Permanently deleted:** The opportunity record itself, and all line items (products attached to it). Line items cannot be recovered.
- **Preserved (not deleted):** Activities, call logs, emails, meetings, and notes logged against the linked contact or account remain intact. Tasks linked to the opportunity have their deal link cleared but are not deleted.
- **"Mark as Lost" option:** Instead of deleting, you can click **"Mark as Lost"** in the same modal. This closes the opportunity as lost without removing any data, and is preferred when you want to keep the history for reporting.

The modal lists exactly which records will be affected before you confirm, so you can review the impact before proceeding.

### E-Signatures

**How to send a document for e-signature:**
1. Go to [PDFs](https://app.trustpager.com/content/documents).
2. Open a document in the **Document Builder** or select a saved document.
3. Click the **"Send for Signing"** action button.
4. Add recipients — enter each signer's name and email. You can add multiple signers.
5. Click **"Send"**. Each recipient receives an email with a secure signing link and a 4-digit PIN for authentication.

**How to track signature status:**
1. Go to [Services > Signatures](https://app.trustpager.com/content/documents/signatures) (the **"Sent"** tab on the PDFs page).
2. Envelopes are grouped by document template, showing completed/pending/declined counts per template.
3. Click a template group to see all envelopes. Click an envelope for full details.
4. Status badges show real-time progress: **Sent**, **Viewed**, **Signed**, **Completed**, **Declined**, **Voided**, **Expired**.
5. Multi-recipient envelopes show individual progress (e.g. 2/3 signed).

**How to manage a signature envelope:**
1. Open an envelope from [Services > Signatures](https://app.trustpager.com/content/documents/signatures).
2. Available actions: **Void** (cancel the envelope), **Resend** (re-send signing email to pending recipients), **Download** (original, signed, or sealed PDF).
3. View the full **audit trail** — every action (viewed, signed, declined, voided) is logged with timestamps.

**How to view signatures on a deal:**
1. Open any Deal detail page from [Opportunities](https://app.trustpager.com/crm/opportunities).
2. Scroll to the **"Signing"** section. This shows all envelopes linked to the deal, their status, and recipient progress.

**Key details about e-signatures:**
- **No third-party tool needed** — signatures are fully built into TrustPager.
- **Signers don't need an account** — they receive an email, verify with a 4-digit PIN, and sign in-browser.
- **Signature methods** — signers can draw, type, or upload their signature.
- **Tamper-proof** — once all recipients sign, the document is sealed with a SHA-256 hash for tamper detection.
- **Signer-fillable fields** — document templates can include fields the signer must complete at signing time (e.g. Company ACN, witness name, date of birth). The signer sees these as labelled input boxes inside the document and fills them in the signing page. Once signed, the values are baked into the sealed PDF.

### AI SMS Agent

**How the AI SMS agent works:**
- When an inbound SMS arrives on your TrustPager phone number with an active AI text agent, the AI automatically reads the conversation, checks the prospect's CRM data (deal stage, pipeline, contact info), and sends a contextual reply.
- The AI is **pipeline-aware** — it pushes leads toward the next sales milestone based on where they are in your workflow.

**How to toggle AI on/off for a conversation:**
1. Go to [SMS Inbox](https://app.trustpager.com/inbox/sms).
2. Open a conversation. Use the **toggle switch** to enable or disable the AI agent for that specific conversation.
3. When you want to take over manually, flip the switch off. AI responses are marked with a **Bot icon**.

**Safety features:**
- The AI defers to humans for complaints, pricing negotiations, legal questions, or when the prospect explicitly asks to speak to a person.
- Responses are SMS-optimised: plain text, kept under 160 characters when possible, no markdown or emojis.

### AI Edit with AI (Text Editing)

**How to edit text with AI:**
1. Right-click on any text field (deal notes, contact descriptions, email bodies, document text, etc.).
2. Select **"Edit with AI"** (Wand icon) from the context menu.
3. A modal opens showing your original text in a read-only preview.
4. Select a **writing style** from the dropdown (Professional, Casual, Concise, etc.).
5. Type or dictate your edit instructions (e.g., "Make this shorter", "More formal tone", "Fix grammar").
6. Click **"Apply Edit"**. The AI refines your text while preserving its meaning.
7. The edited text is inserted back into the field.

### AI Fill with AI (Form Auto-Fill)

**How to auto-fill forms with AI:**
1. On any form with AI-fillable fields (deals, contacts, emails, documents), look for the **"Fill with AI"** button (Wand icon, pill-shaped badge).
2. Click it to open the Fill with AI modal.
3. Select a **writing style** from the dropdown.
4. Type or dictate what you want generated (e.g., "Follow-up about the pricing call with John").
5. Click **"Generate"**. The AI fills all applicable form fields automatically.
6. The modal closes and your form fields are populated. Edit any field manually if needed.

### AI Needs Analysis

**How to generate a needs analysis for a deal:**
1. Open any Deal detail page from [Opportunities](https://app.trustpager.com/crm/opportunities).
2. Scroll to the **"Needs Analysis"** card section.
3. Click the **"Generate Analysis"** button (FileSearch icon) in the top-right of the card.
4. Optionally add custom instructions in the modal (e.g., "Focus on compliance requirements").
5. Click **"Generate Analysis"**. Progress steps show: gathering data, checking sufficiency, running analysis, saving.
6. The completed analysis includes:
   - **Executive Summary** — overview of the client's situation
   - **Needs & Solutions** — matched pairs of identified needs with proposed solutions
   - **Recommended Products** — linked to your product catalogue
   - **Guaranteed Deliverables** — title and description for each deliverable
   - **Closing Strategy** — internal-only section (hidden from clients)
7. All fields are editable. Drag items to reorder. Add or remove items with the **"+"** buttons.
8. Click **"Re-analyse"** to regenerate with updated deal data.

### AI Form Prefill (Document Signing)

**How to prefill signing forms with AI:**
1. When sending a document for signing that has form fields, look for the **"Prefill with AI"** button (Wand icon).
2. The modal shows what deal data will be analysed (deal name, contact, account, activities, products, SMS/calls).
3. Optionally add instructions for additional context.
4. Click **"Generate"**. Progress steps update in real time.
5. Result shows "X of Y fields prefilled" — the AI populated form fields using real deal data.
6. Review and manually adjust any prefilled values before sending.

### AI Call Coaching

**How to generate coaching from a call:**
1. Go to [Phone Calls](https://app.trustpager.com/inbox/phone-calls) and open a call transcript.
2. Find the **"AI Coaching"** card section (GraduationCap icon).
3. Click **"Generate Coaching"**. The AI analyses the transcript for each team member.
4. Results show per team member:
   - **Overall score** (0-100) with category breakdowns
   - **Strengths** — what went well
   - **Areas for improvement** — specific coaching points
   - **Coaching summary** — actionable advice
5. Expand each team member's results for detailed insights.
6. Click the **refresh button** to regenerate coaching with updated context.

### AI Image Generation (Image Builder)

**How to generate images with AI:**
1. Go to [Images](https://app.trustpager.com/content/images) and click the **"Projects"** tab.
2. Click the **"Create New Project"** card (+ icon) and select a preset category.
3. The Image Builder opens full-screen with a prompt sidebar and canvas.
4. In the **"Prompt"** tab (right sidebar):
   - Enter a description (minimum 2 characters)
   - Select Image Type (Photography, Illustration, etc.)
   - Choose Style, Influence, Environment, Background, Mood, and Colours
   - Set Aspect Ratio and dimensions
5. Click **"Generate"** at the bottom of the sidebar.
6. The image appears on the canvas. All versions are saved in the history carousel at the bottom.
7. Switch to the **"Edit"** tab for post-processing:
   - **Inpaint** — draw a mask on a region and describe what to change
   - **Upscale** — enlarge 2x or 4x
   - **Remove Background** — one-click background removal
8. Click **"Download"** in the header to save the final image.

### PDFs, Files, Images & Forms

**How to upload a PDF:**
1. Go to [PDFs](https://app.trustpager.com/content/documents).
2. Make sure you're on the **"Saved"** tab (shown in the page header tabs).
3. You'll see a **drag-and-drop upload zone** — either drag a PDF onto it, or click to browse.
4. The PDF uploads with an animated progress indicator.

**How to create a document from scratch:**
1. Go to [PDFs](https://app.trustpager.com/content/documents).
2. Click the **"Templates"** tab, then click into an existing template or create one. This opens the **Document Builder** in full-screen mode.
3. Use the builder to add sections, text, images, and layout. Click **"Save"** when done.

**How to organise PDFs into folders:**
1. On the [PDFs](https://app.trustpager.com/content/documents) page, look at the **left sidebar**.
2. Select a document type tab (All, Agreement, Form, Invoice, Letter, Other).
3. Folders appear below the type tabs. Click the **"+" button** to create a new folder.

**How to send a document:**
1. Open the document detail page from [PDFs](https://app.trustpager.com/content/documents) > Saved tab.
2. Click the **"Send"** button in the top-right actions area.
3. Enter the recipient's details and click **"Send"**.

**How to upload a file:**
1. Go to [Files](https://app.trustpager.com/content/files).
2. Drag any file onto the **upload zone**, or click to browse. Accepts all file types — PDFs, images, videos (MP4, WebM, MOV up to 50 MB), Word, Excel, PowerPoint, CSV, text, archives (zip, rar, 7z), and more. PDFs are automatically stored in the PDFs system; images are stored in the Images system; videos are stored in the Videos system; everything else is stored as a secure file.
3. Optionally add a description and select a folder.
4. Click **"Upload"**. A progress bar tracks the upload status.

**How to upload a video:**
1. Go to [Files](https://app.trustpager.com/content/files).
2. Drag an MP4, WebM, or MOV file (up to 50 MB) onto the **upload zone**, or click to browse and select your video.
3. The file uploads directly to cloud storage — a progress bar tracks the status.
4. Once complete, the video appears in the **Videos** tab with a thumbnail preview. Click the card to preview it or use the three-dot menu to download or delete.

**How to manage files:**
1. On the [Files](https://app.trustpager.com/content/files) page, each file card has a **three-dot menu** (top-right of card in grid view, right side in list view).
2. Menu options: **View File** (opens preview), **Move File** (change folder), **Delete**.
3. Use the **category tabs** (All, Documents, Spreadsheets, Presentations, Text, Archives, Images, Videos) to filter by file type.
4. Use the **left sidebar** to filter by folder, create new folders, rename, or delete folders.

**How to preview a file:**
1. On the [Files](https://app.trustpager.com/content/files) page, click any file card.
2. Office files (docx, xlsx, pptx) open in a full-screen Google Docs Viewer. Text/CSV files display inline. Archives show a download button. Videos show an inline player with a thumbnail.
3. Click **"Download"** in the toolbar to save the file locally. For videos, the Download button generates a secure link and triggers an immediate file save to your device.

**How to upload an image:**
1. Go to [Images](https://app.trustpager.com/content/images).
2. Drag an image onto the **upload zone**, or click to browse.
3. Optionally toggle **"Optimise for Web"** to compress the image for faster loading.
4. Select a folder and add a description if needed, then click **"Upload"**.

**How to make an image public (share via direct URL):**
1. Go to [Images](https://app.trustpager.com/content/images) > **Manage** tab.
2. Find the image you want to share. Private images show a lock icon on the card.
3. Open the three-dot menu on the image card and click **"Make Public"**.
4. The image moves to the public CDN -- you'll see the direct URL you can share or embed.

**How to make an image private (revoke public access):**
1. Go to [Images](https://app.trustpager.com/content/images) > **Manage** tab.
2. Find the public image. Public images show their CDN URL on the card.
3. Open the three-dot menu and click **"Make Private"**.
4. The image is moved to private storage. The old public URL stops working immediately.

**How to publish a document to a public URL:**
1. Go to [PDFs](https://app.trustpager.com/content/documents) and open a document from the **Saved** tab.
2. In the document detail view, find the **"Publish"** button in the toolbar or document actions.
3. Click **"Publish"** -- the document PDF is copied to the public CDN and a shareable URL is generated. Your original private copy is kept.
4. Share the public URL directly with anyone (no login required to view).

**How to unpublish a document (revoke public access):**
1. Open the published document from [PDFs](https://app.trustpager.com/content/documents) > **Saved** tab.
2. Click **"Unpublish"** in the toolbar. The public CDN copy is deleted and the URL stops working. Your private original is unchanged.

**How to attach a file to a CRM entity:**
1. Open a Contact, Account, or Opportunity detail page.
2. In the sidebar, find the **Files** section.
3. Click **"Add"** and choose **"Upload New"** or **"Link Existing"**. Uploaded files are automatically routed — PDFs go to the PDFs system, images go to Images, and everything else becomes a secure file.

**How to download all attachments as a ZIP file:**
1. Open any Opportunity, Contact, or Account detail page.
2. Find the **Documents**, **Files**, or **Images** section in the sidebar.
3. Click the **three-dot menu (...)** next to the "Add Document / Add File / Add Image" button for the section you want to download.
4. Click **"Download all (.zip)"**. Your browser downloads a single ZIP containing every file in that section.
- Each section (Documents, Files, Images) downloads separately.
- The ZIP filename is based on the record name and today's date (e.g. "Smith_John_2026-05-19.zip").
- Files that cannot be fetched are noted in a _manifest.txt file inside the ZIP.

**How to create a form:**
1. Go to [Forms](https://app.trustpager.com/operations/forms).
2. On the **"Templates"** tab, choose from pre-built templates in the visual grid, click **"Blank Form"** to start from scratch, or click **"Generate with AI"** (wand icon).
3. This opens the **Form Builder** in full-screen mode. Add fields, configure layout, and click **"Save"**.

**How to set up CRM Variable Injection on a form field:**
1. In the **Form Builder**, click a field to open its properties in the **right sidebar**.
2. Scroll to the **"CRM Variable Injection"** section (below the Required/Visible toggles).
3. Search and select a CRM field (Account, Contact, or Opportunity fields including custom fields).
4. Choose an **injection mode**: **Write if empty** (only fills blank CRM fields) or **Always overwrite** (replaces existing values).
5. When this form is filled in linked to an opportunity, each field update automatically writes to the mapped CRM field in real time.
6. Injection runs before automations, so downstream workflows have access to the updated data.

**How form autosave works (forms linked to an opportunity):**
- Forms sent from an opportunity open in a collaborative fill mode. Each field saves automatically as it is filled -- there is no Submit button to press.
- Reopening the same form (from the opportunity or from the Sent tab) resumes exactly where it was left off. No data is lost between sessions.
- The form is marked complete once all required fields have been filled. CRM fields update in real time as each field is saved.
- Only one response exists per form per opportunity -- re-opening always resumes the same session, never creates a duplicate.

**How to view form responses:**
1. Go to [Forms](https://app.trustpager.com/operations/forms).
2. Click the **"Sent"** tab in the page header.
3. Click into a specific form to see all submissions.
4. Click a submission to see the full response detail.

**How to convert a completed form submission to a PDF:**
1. Open a completed form submission (Sent tab > select form > click a submission).
2. In the submission detail, click the **"Convert to PDF"** button (available for completed submissions linked to an opportunity).
3. The PDF is generated and attached to the linked opportunity's Documents tab.
4. Credit cost: 1 credit per page of the generated PDF.

**How to delete a form submission:**
1. Go to [Forms](https://app.trustpager.com/operations/forms) and click the **Sent** tab.
2. Click a form to open its submissions list. Click the **Delete** button (trash icon) on the submission row, or open the submission and click **Delete Submission** in the header.
3. In the confirmation dialog, optionally tick **"Also delete archived PDF"** to remove the auto-archived PDF from the Documents library.
4. Click **Confirm Delete**. The submission and any uploaded files are permanently removed. This cannot be undone.
   - Note: This requires the **forms:delete** permission scope. Contact your workspace admin if the button is not visible.
   - Tip: Use **Void** instead if you only want to expire an unfilled submission without removing the record.

**How to enable automatic PDF archiving for a form template:**
1. Go to [Forms](https://app.trustpager.com/operations/forms), open the **Templates** tab.
2. Click **Edit** on the form template, then open the right sidebar.
3. In the **"PDF Archive"** section, toggle on **"Archive submissions as PDF"**.
4. Optionally set the **Folder** (default: "Client Forms") and **Document Type** (default: "Other") for the archived PDFs.
5. Click **Save**. From this point, every new completed submission that is linked to an opportunity will automatically generate a PDF and attach it to that opportunity.

### Lead Generation

The Lead Generation tool searches Google Maps for businesses in a specific location and lets you import them directly into your CRM as contacts and accounts.

**How to run a lead generation search:**
1. Go to [Lead Generation](https://app.trustpager.com/growth/lead-gen).
2. Enter a **Search Query** (e.g. "electricians", "dentists", "restaurants") in the search bar at the top.
3. Enter a **Location** (e.g. "Sydney, NSW", "Melbourne, VIC").
4. Optionally set **Max Results** (1-500) and **Radius (km)**.
5. Optionally enable **"Require email address"** (on by default). When enabled, only businesses with a scraped email are returned -- results without an email are automatically excluded. The search always runs in the background when this toggle is on (results are not instant even for small searches).
6. Click **"Search"**. For up to 100 results (without email requirement), the search completes instantly. For larger searches (101-500) or when "Require email address" is on, a progress indicator shows while results are fetched -- the page will update automatically when complete.
7. Results appear in a table sorted by Google rating. Each row shows: business name, category, phone, website, email, rating, reviews, and match status.

**How to read match status:**
- **New** -- not in your CRM. This is a fresh lead.
- **Previously Found** -- appeared in a past search but was not imported.
- **Already in CRM** -- phone or website matches an existing contact or account. Click the match link to view the CRM record.

**How to import results:**
1. On the search results page, tick the checkboxes for the businesses you want to import.
2. Click **"Import Selected"** in the toolbar.
3. In the import modal:
   - Optionally select a **Workflow** and **Stage** to create an opportunity for each imported business.
   - Optionally add **Tags** to apply to imported records.
   - Set a **Lead Source** label (default "Lead Generation").
4. Click **"Import"**. Each selected business creates one contact and one account (linked together). If a workflow and stage were selected, an opportunity is also created.
5. An activity note is automatically logged on each contact with the Google Maps source data.

**How to save a search for repeated use:**
1. After running a search, click **"Save Search"** (BookmarkPlus icon) in the search toolbar.
2. Give it a name (e.g. "Sydney Electricians"), then click **"Save"**.
3. Saved searches appear in the **"Saved Searches"** tab on the Lead Generation page.
4. Click **"Run"** on any saved search to re-run it with the same parameters.
5. The saved search tracks how many times it has run and when it was last run.

**How to manage saved searches:**
1. Go to [Lead Generation](https://app.trustpager.com/growth/lead-gen) and click the **"Saved Searches"** tab.
2. Each saved search card shows: name, query, location, run count, and last run date.
3. Click **"Edit"** (pencil icon) to update the name, query, location, max results, or default import settings.
4. Click **"Archive"** (trash icon) to remove a saved search. Past results are preserved.

**How to create an outreach initiative:**
1. Go to [Lead Gen Initiatives](https://app.trustpager.com/growth/lead-gen/initiatives).
2. Click the **"+ New Initiative"** button in the top-right corner.
3. Give the initiative a **Name** (e.g. "Q3 Roofing Outreach") and optional description.
4. Click **"Create"**. The initiative opens in **draft** status.

**How to add steps to an initiative:**
1. Open an initiative from [Lead Gen Initiatives](https://app.trustpager.com/growth/lead-gen/initiatives).
2. Click **"+ Add Step"** in the steps panel.
3. Choose an **Action Type:**
   - **Send Email** -- sends an email via your connected Gmail account. You must have Gmail connected under Settings.
   - **Send SMS** -- sends an SMS to the lead's phone number.
   - **Notify Me** -- sends you an internal email alert about this lead.
4. For email and SMS steps, write the **Subject** and **Body** using template tokens (e.g. `{{lead.name}}`, `{{lead.business_name}}`) to personalise each message.
5. Set a **Delay** (days to wait after the previous step before sending this one). Set to 0 for immediate send.
6. Click **"Save Step"**.

**How to enrol leads into an initiative:**
1. Run a [Lead Generation](https://app.trustpager.com/growth/lead-gen) search and view results.
2. Select the leads you want to enrol using the **checkboxes** on each row.
3. Click **"Enrol in Initiative"** from the bulk-action toolbar that appears at the bottom of the page.
4. Choose the initiative from the dropdown and click **"Enrol"**.
5. Enrolled leads appear under the initiative's **Enrolments** tab with their current step and next scheduled action.

**How to activate and run an initiative:**
1. Open the initiative and click **"Activate"** (or set status to **Active** in the settings). This enables the dispatcher to begin sending.
2. Steps are processed automatically on a daily schedule. To process immediately, click **"Run Now"** on the initiative detail page.
3. Monitor progress on the **Enrolments** tab -- each row shows the lead, current step, status, and next action date.

**How to pause or stop an initiative:**
- Click **"Pause"** to temporarily halt all sends. Enrolments are preserved and resume when you reactivate.
- Click **"Delete"** to permanently remove the initiative and all enrolments. There is no undo.

### Workspace Spreadsheets (Export Templates with Saved Views)

Saved, reusable spreadsheet templates that pull joined CRM data into a live grid — opportunity + primary contact phone/email + account + custom fields, one row per opp. Each template has shared columns and one or more **saved views** (named filter sets). Available at [Spreadsheets](https://app.trustpager.com/operations/spreadsheets).

**How to create a spreadsheet:**
1. Go to [Spreadsheets](https://app.trustpager.com/operations/spreadsheets).
2. Click the **"New"** button in the top-right.
3. Give it a name (e.g. "Monthly HubSpot Reconciliation"), pick a **Root entity** — Opportunity, Contact, Account, or Work Order. Each output row represents one root record.
4. Click **"Create & open"** to enter the builder canvas.
5. **Add columns** from the right sidebar's "Columns" tab. The catalogue is grouped — Opportunity fields, Pipeline & Stage, Primary Contact, All Linked Contacts, Primary Account, Deal Products, Assigned User, etc.
6. For relation columns (anything joined from another entity), click the column to edit its **relation mode**: Primary only / First N / All comma-joined / Explode rows. "Explode" produces one output row per related record (useful for multi-stakeholder deals).
7. Switch to the **"Filters"** tab and add filters to scope the data. The filter panel is fully type-aware — picker dropdowns for Pipeline, Stage, Assigned User, Work Order Status (no UUID pasting); enum dropdowns for Status, Lead Source, Opportunity Type, etc. that show the workspace's configured options; date pickers for date fields; Yes/No toggles for booleans. Custom fields appear under a **"Custom fields"** group — supports text, dropdown, date, checkbox, and multiselect custom fields directly. **Tags** support two operators: **"is one of"** (row has ANY of the selected tags -- OR logic) and **"is none of"** (row has NONE of the selected tags -- NOR logic, useful to exclude labelled segments like VIP or COLD). The operator list is filtered to what's valid for each field (date fields don't offer `contains`, text doesn't offer `between`, etc.). Each row collapses to a plain-English summary ("Pipeline is Sales Pipeline", "Created on or after 1 May 2026") for scannable stacks.
8. Switch to the **"Output"** tab to choose XLSX or CSV (UTF-8 BOM toggle on by default — keep it on for Excel/HubSpot compatibility), and set a filename pattern with tokens `{name}` / `{YYYY-MM-DD}` / `{YYYY}` / `{MM}` / `{DD}`.
9. The canvas shows a **live preview** of the first 10 rows — updates as you change columns or filters. Auto-save kicks in after a 1-second pause.
10. Click **"Export"** (top-right) to download the file immediately. The toast confirms which view was exported.

**How to use saved views:**
Every workspace spreadsheet starts with a "Default view". Each view shares the template's columns + output but holds its own filter set — so one template can drive "May invoicing", "Open jobs only", "Quotes only", etc. without re-entering filters each time.

1. Open any spreadsheet at `/operations/spreadsheets/<template-id>`.
2. The **view picker pill** sits next to the title at the top — `[icon] Active view name (N) ▼`.
3. Click the pill to open the popover. Search across views with the input at the top.
4. Click a row to **switch** views — the URL updates to `?view=<view-id>` (shareable / browser-back works between views).
5. Hover a row to reveal **pencil** (rename inline) and **trash** (delete) actions. The trash is disabled when only one view remains.
6. Click **"+ New view"** at the bottom to create a new view (auto-named `View 2`, `View 3`, etc.) — switch to it immediately and rename inline from the popover.
7. Filter edits **save to the active view** (1-second debounce). Column / name / output edits save to the template and apply across every view.

**How to open a saved spreadsheet:**
1. Go to [Spreadsheets](https://app.trustpager.com/operations/spreadsheets).
2. Click the card to open the builder. The card chip shows the **active view's first filter** as a plain-English summary ("Pipeline is Sales Pipeline +2") so you can see at a glance what each spreadsheet is scoped to.
3. Once inside, switch views via the picker pill or click **"Export"** to download the active view.

**How to manage templates:**
- Each template card has a `⋮` menu with: Edit, Duplicate, Archive, Delete.
- Templates auto-save — there's no save button.
- If filters return zero rows, the canvas lists the active filters and offers a **"Clear all filters"** button instead of an empty grid.

**Quick-export from any list page:**
- Every list view (Opportunities, Contacts, Accounts, Tasks, etc.) has a small Download icon in the toolbar — exports the current visible page to CSV. Use this for ad-hoc snapshots; use the Export Builder for full datasets, joined data, or saved configurations.

### Notepads

**How to create a notepad:**
1. Go to [Notepads](https://app.trustpager.com/operations/notepads).
2. Click the **"New Notepad"** button (+ icon) in the **top-right** of the page header.
3. A new notepad is created and the editor opens automatically.
4. Type a title at the top (auto-saves with a short delay).
5. Write content using the rich text editor — supports bold, italic, underline, strikethrough, headings (H1-H3), lists, tables, text colour, highlighting, and alignment.
6. All changes **auto-save** — you'll see "Saving..." then "Saved" in the header.

**How to use AI in notepads:**
1. In the notepad editor, click the **Wand icon** (top-right of the toolbar) to open the **AI Text Panel**.
2. The panel slides in from the right. Type a prompt and the AI generates text to insert into your notepad.
3. Click the **Image icon** (top-right of the toolbar) to open the **AI Image Panel** — generates images directly inside your notepad.

**How to control who can see a notepad (visibility):**
1. Open a notepad and click the **visibility badge** (shows "All Users", "Admins Only", etc.) near the top of the editor.
2. Choose a visibility level from the dropdown:
   - **All Users** -- everyone in your workspace can see this notepad.
   - **Admins Only** -- only admin-role users can see it.
   - **Creator Only** -- only you (the creator) can see it.
   - **Restricted** -- only specific people or roles you grant access to can see it.
3. For **Restricted** notepads, an **ACL picker** appears. Click **"Add person or role"** to grant access to individual users or role groups (e.g. Client Admin, Client Editor).
4. To remove someone's access, click the **X** next to their name in the ACL list.

**How to control who can see a folder (folder visibility):**
1. On the [Notepads](https://app.trustpager.com/operations/notepads) page, right-click a folder in the **left sidebar** (or use the three-dot menu next to it) and select **"Edit folder"**.
2. Set the **Visibility** for the folder. A folder set to **Admins Only** hides itself and all notepads inside it from non-admin users.
3. For **Restricted** folders, add users or roles in the ACL picker -- access cascades to all notepads inside the folder unless a notepad has its own stricter visibility.

**How to organise notepads:**
1. On the [Notepads](https://app.trustpager.com/operations/notepads) page, use the **left sidebar** to browse folders.
2. Click the **"+" button** to create a new folder.
3. Use the **three-dot menu** on any notepad card for: Open, Add/Remove Favourite (Star icon), Move File (FolderInput icon), Delete.
4. Click the **Star icon** to mark a notepad as a favourite. Use the **"Favourites"** toggle in the sidebar to filter.

**Using the API or AI agents to edit notepads (append, prepend, section patches):**
AI agents and the API can edit notepads without re-sending the full content. Three modes are available on `update_notepad`:
- **Append** -- adds new content to the end of the notepad (e.g., a daily log entry). Pass `mode: "append"` and `content`.
- **Prepend** -- adds content to the start (e.g., a summary header). Pass `mode: "prepend"` and `content`.
- **Section patches** -- replaces or appends to specific sections by heading name. Useful for structured documents (e.g., update just the "Action Items" or "Status" section). Pass a `patches` array with `match_heading` and `new_content` per section.

These modes let agents grow or update a notepad incrementally -- no need to download and re-upload the whole document. Agents can also pass `return_content: true` to receive the updated HTML in the response.

### Playbooks

Playbooks are drag-and-drop boards where you build onboarding flows, training modules, and reference libraries for your team. Each Playbook holds multiple cards -- video players, links, notepads, PDFs, images, and secure files -- arranged in a responsive grid.

**URL:** https://app.trustpager.com/training/playbooks

**How to create a Playbook:**
1. Go to [Playbooks](https://app.trustpager.com/training/playbooks).
2. Click **"New Canvas"** in the top-right.
3. Enter a canvas name and optionally choose the **"Getting Started"** template to pre-load 6 starter cards.
4. Click **"Create"**.

**How to add a card to a canvas:**
1. Open a canvas.
2. Click **"Add Card"** (the + button in the header or on the canvas itself).
3. The **card wizard** opens. Select a card type:
   - **Notepad** -- creates or links an editable rich-text card
   - **YouTube** -- embeds a YouTube video
   - **Link** -- shows a clickable external URL tile
   - **HTML Embed** -- embeds any URL in an iframe
   - **PDF (Document)** -- links to a document from your Documents library (opens as PDF viewer)
   - **Image** -- links to an image from your Files library
   - **Secure File** -- links to a file from your Secure Files library
4. For PDF, Image, and Secure File cards: Step 2 of the wizard lets you **upload a new file** or **link an existing one** from your libraries.
5. Complete the remaining steps (title, description, category) and click **"Add to Canvas"**.

**How to move and resize cards:**
- Drag any card by its header to reposition it on the grid.
- Drag the bottom-right corner of a card to resize it.
- Changes save automatically.

**How to filter cards by category:**
- Use the filter pills at the top of the canvas: PDFs, Images, Files, or the original category pills (Training, Sales, Policy, Reference).
- Click a pill to show only cards of that type. Click again to clear.

**How to edit or delete a card:**
1. Hover over the card to reveal the **three-dot menu** (top-right of the card).
2. Choose **"Edit"** to update the title, description, or linked content.
3. Choose **"Delete"** to remove the card from the canvas.
4. Note: deleting a card does NOT delete the underlying notepad, document, or file.

### Workflow Training

Workflow Training shows each pipeline alongside its linked training resource. Team members can open the training directly from the pipeline board or from this page.

**URL:** https://app.trustpager.com/training/workflows

**How to link training to a pipeline:**
1. Go to [Workflow Training](https://app.trustpager.com/training/workflows).
2. Hover over any pipeline card and click the **settings gear** that appears in the top-right corner.
3. The **Training Link** modal opens with a segmented control:
   - **External URL** -- paste any URL (Notion, Loom, Google Doc, internal wiki, etc.)
   - **Playbook** -- search and pick a canvas you have built in Playbooks
4. Select your option, then click **Save**.
5. A "View Training" button now appears on the pipeline card footer and on the pipeline board.

**How to open training from the pipeline board:**
- Go to [Workflows](https://app.trustpager.com/crm/workflows) and open any pipeline.
- If a training resource is linked, a **"View Training"** button appears in the action bar at the top.
- Clicking it opens the Playbook in-app (canvas link) or the external URL in a new tab (external URL).

**Note:** `sop_url` (external URL) and `learning_hub_canvas_id` (in-app canvas) are mutually exclusive. Setting one clears the other.

### AI Knowledge

AI Knowledge stores company knowledge entries for your AI agents and team. Entries are indexed with semantic embeddings so AI agents can retrieve relevant context automatically using natural language search.

**How to add a knowledge entry:**
1. Go to [AI Knowledge](https://app.trustpager.com/training/knowledge).
2. Click the **"New Entry"** button in the **top-right** of the page header.
3. Fill in the **Title** and **Content** fields. Content is the full text of the knowledge.
4. Choose a **Category**: General (default), Agent (AI behavioral instructions), FAQ, Policy, Procedure, or Product.
5. Add optional **Tags** to help with filtering.
6. Click **Save**. An embedding is generated automatically -- the entry is now available for semantic search.

**How to search the knowledge base:**
- Use the **search bar** at the top of the [AI Knowledge](https://app.trustpager.com/training/knowledge) page to filter entries by title or content.
- AI agents use semantic search automatically -- they find relevant entries even if the exact words don't match.

**Category guide:**
- **General** -- default for miscellaneous knowledge
- **Agent** -- behavioral instructions for AI agents (e.g. "Always confirm pricing before quoting")
- **FAQ** -- common questions and answers
- **Policy** -- company policies and rules
- **Procedure** -- step-by-step processes
- **Product** -- product or service information

### Knowledge Bases

Knowledge Bases are named collections that group knowledge entries and attach them to specific agents. Where individual knowledge entries are searchable workspace-wide, a Knowledge Base scopes an agent's search to only the content that is relevant to it.

**How to create a Knowledge Base:**
1. Go to [AI Knowledge](https://app.trustpager.com/ai-agents/knowledgebase).
2. Click **"New Knowledge Base"** and give it a name and optional description.
3. Choose a **Resync Frequency** (Manual, Daily, or Weekly) to control how often the KB auto-refreshes from its sources.
4. Click **Save**.

**How to populate a Knowledge Base:**
- **From help center articles:** click **"Sync Help Center"** to ingest all published articles as embedded entries.
- **From the product catalog:** click **"Sync Products"** to ingest active CRM products.
- **From a web page:** paste a URL and click **"Ingest URL"** -- the page is fetched and its text embedded.
- **From text:** paste or upload text content directly via **"Add Text"**.

**How to attach a Knowledge Base to an agent:**
1. Open the Knowledge Base detail page.
2. Click **"Attach Agent"** and select the agent type (Voice or Workflow) and the specific agent.
3. The agent's searches will now be scoped to entries in this KB.

**Key points:**
- One KB can be attached to many agents; one agent can have many KBs attached.
- Both voice agents and workflow (AI) agents use the same unified Knowledge Base system.
- Deleting a KB removes agent attachments but keeps the individual entries.
- If you already have a voice agent knowledge base set up through the voice agent settings, use **"Adopt Existing"** to migrate it into the unified system without losing content.

### Work Orders (on Deals)

**How to manage work orders on a deal:**
1. Open any Deal detail page from [Opportunities](https://app.trustpager.com/crm/opportunities).
2. Scroll to the **"Work Orders"** card section. Work order slots are created automatically based on product quantity.
3. Each work order shows as an inline accordion. Incomplete orders have an **amber border** with a warning icon and progress bar showing how many required fields remain.
4. Click an accordion to expand it and fill in the fields directly on the page. Fields auto-save when you click away (no save button needed).
5. Once all required fields are filled, the accordion auto-collapses with a **green border** and checkmark.
6. If a product has custom discovery questions configured, those questions appear instead of the company defaults.
7. Click **"Clear"** at the bottom of an expanded work order to reset it.

**How to send a Work Status update to a client:**
1. Open the deal detail page and scroll to the **"Work Orders"** card.
2. Click the dropdown arrow on the card header and select **"Send Work Status"**.
3. A modal appears. Enter the client's **Name** and **Email** (required), and optionally add a **Personal Message** and set an **Expiry** (default 30 days).
4. Click **"Send"**. The client receives a branded email with a PIN-protected link to view all work order progress for the deal.
5. The Work Status Portal shows each work order's deliverable name and current status (with colour). The client does not need to log in to TrustPager.
6. To revoke access, click the dropdown arrow on the card header and select **"Revoke Work Status"**.

### Supplier Products (on Accounts)

**How to manage supplier products on an account:**
1. Open any Account detail page from [Accounts](https://app.trustpager.com/crm/accounts).
2. Scroll to the **"Supplier Products"** card section.
3. Click **"Add"** to create a new supplier product cost line linked to this account.
4. Fill in the product, cost, quantity, and other fields. Click **"Save"**.
5. Each supplier product line shows cost details and can be edited or deleted.

### Quick Links (on Deals, Accounts, and Contacts)

**How to add or edit quick links:**
1. Open any Deal, Account, or Contact detail page.
2. Find the **Quick Links** card in the right sidebar.
3. Click **"Add Links"** (if no links exist) or **"Edit Links"** (pencil icon, if links already exist).
4. A modal opens showing all configured quick link types (e.g. Google Drive, Notion, Slack, Dropbox, etc.). These types are configured by your admin in CRM Settings.
5. Enter or paste a URL for each link type you want to set. URLs without `https://` are auto-prefixed.
6. Click **"Save"** to apply. The card immediately shows the saved links as clickable items.
7. Click any link in the card to open it in a new tab.

**Quick link types** are configured company-wide by admins via [Settings > CRM](https://app.trustpager.com/settings/crm). Each entity (deal, account, or contact) stores its own URLs for each type.

### Custom Fields

**How to use custom fields:**
- Custom fields are available on **Deals**, **Contacts**, and **Accounts**.
- They appear as additional fields on detail pages below the standard fields.
- Custom fields are configured by your admin and can hold text, numbers, dates, dropdown values, or **URLs**.
- **URL custom fields** render as a clickable link with an open-in-new-tab icon. Click the icon to open the link in a new browser tab. Use these for Google Drive folders, client portal links, signed agreement URLs, or any external resource tied to the record. A valid URL starting with `http://` or `https://` is required; `https://` is prepended automatically if missing.
- Custom fields are included in automations, AI scoring, and form CRM Variable Injection.

**Conditional logic on deal custom fields:**
- Some deal custom fields may be configured with visibility rules -- they only appear when certain conditions are met (e.g. "Purchase Date" only shows when "Application Type" is "Purchase"). This is normal -- the field is not missing, just hidden until the relevant trigger field is set.
- Some deal custom fields auto-populate when a deal is created or updated. For example, "Settlement Date" might automatically be set to today + 1 month when you select "Refinance" as the application type. These automatic values can always be overridden by editing the field directly -- once you manually enter a value, the automatic rule will no longer update it.

### Communications

**How to send an SMS:**
1. Go to [SMS Inbox](https://app.trustpager.com/inbox/sms).
2. Click the **"Compose Message"** button (message icon) in the **top-right** of the page.
3. Enter the phone number and type your message.
4. Click **"Send"** to send immediately, or click the dropdown caret next to **Send** and choose **"Schedule send..."** to defer the message to a specific time.

**How to schedule an email or SMS for later:**
1. Compose the message as normal (Compose Email modal or SMS conversation page).
2. Click the dropdown caret next to the **Send** button.
3. Choose **"Schedule send..."**.
4. Pick a date, time, and timezone. Click **"Schedule send"**.
5. The message appears in the [Dispatcher → Scheduled tab](https://app.trustpager.com/inbox/dispatcher) and will fire automatically at the chosen time.
6. Scheduled sends are automatically cancelled if the contact unsubscribes, replies, opts out of SMS, or if a tied deal is closed (won/lost) — you can still send manually if you choose.

**How to view scheduled and dispatched messages (the Dispatcher):**
1. Go to [Dispatcher](https://app.trustpager.com/inbox/dispatcher).
2. **Scheduled** tab shows pending messages waiting to send.
3. **History** tab shows: **Delivered** (provider confirmed receipt), **Sent** (in-flight), **Undelivered** (bounced / no-answer / SMS rejected — see error message), **Failed** (after retries), **Cancelled** (auto-cancelled by reply/unsubscribe/close).
4. Hover over an Undelivered or Failed row's error message to see the full provider reason.

**How to view email threads:**
1. Go to [Email Inbox](https://app.trustpager.com/inbox/email).
2. Click any thread in the list to open the full conversation chain.
3. Use the reply box at the bottom to respond.

**How to send an email with a file attachment:**
1. Go to [Email Inbox](https://app.trustpager.com/inbox/email).
2. Click **"Compose"** (pencil icon, top-right).
3. Fill in the recipient, subject, and body.
4. Click the **paperclip (Attach File) icon** below the message body.
5. Select a file from your workspace file library or upload a new one.
6. Click **Send**. The attachment appears as a chip in the sent thread.

File size limits: 7 MB total when sending via TrustPager Mail; 25 MB total when sending via Gmail. To change which provider is used, go to [Settings > Email](https://app.trustpager.com/settings/email).

**How to mark all email threads as read:**
1. Go to [Email Inbox](https://app.trustpager.com/inbox/email).
2. Click the **"Mark All Read"** button in the **top-right** of the toolbar.
3. All unread threads are marked as read instantly. The button is only visible when unread threads exist.

**How to mark all SMS conversations as read:**
1. Go to [SMS Inbox](https://app.trustpager.com/inbox/sms).
2. Click the **"Mark All Read"** button in the **top-right** of the toolbar.
3. All unread conversations are marked as read instantly.

**How to connect your WhatsApp account:**

WhatsApp uses a personal pairing model -- each team member links their own WhatsApp phone number to the workspace. Once paired, incoming WhatsApp messages appear in the [WhatsApp Inbox](https://app.trustpager.com/inbox/whatsapp) and you can send messages from there.

1. Go to [Account > Connect](https://app.trustpager.com/account/connect).
2. Click **"Connect WhatsApp"** and a QR code will appear.
3. On your phone, open WhatsApp, go to **Settings > Linked Devices > Link a Device**, and scan the QR code.
4. Once paired, the status shows **Connected** with your linked phone number.
5. Your WhatsApp conversations will appear in the [WhatsApp Inbox](https://app.trustpager.com/inbox/whatsapp).

**How to send a WhatsApp message:**
1. Go to [WhatsApp Inbox](https://app.trustpager.com/inbox/whatsapp).
2. Click **"Compose"** (or open an existing conversation).
3. Type your message and click **"Send"**.

**How to send to a WhatsApp group:**
1. Go to [WhatsApp Inbox](https://app.trustpager.com/inbox/whatsapp) and open the **Groups** tab.
2. Click on a group to open the conversation.
3. Type your message and click **"Send"**.

**Important notes:**
- WhatsApp is linked per user, not per workspace. Each team member must connect their own phone.
- If a contact has opted out of WhatsApp, messages to them are automatically suppressed.
- You must have your phone online and connected to send and receive messages.

**How to create an email marketing campaign:**
1. Go to [Email Marketing](https://app.trustpager.com/growth/email-blasts).
2. Click the **"New Campaign"** button in the **top-right** of the page.
3. Fill in the campaign name and click **"Create"**. This creates a draft campaign and opens the campaign editor.
4. In the editor, fill in: Subject line, email body (rich text), and optional Intro Text, CTA button (text + URL).
5. Set your audience in the **"Audience"** section: choose tags, or a specific pipeline stage, to target specific contacts.
6. Click **"Preview Audience"** to see exactly which contacts will receive the email before sending.
7. When ready, click **"Send Campaign"** to broadcast immediately.

**How to track campaign performance:**
1. Go to [Email Marketing](https://app.trustpager.com/growth/email-blasts).
2. Click any sent campaign to open its detail page.
3. The detail page shows: Sent, Delivered, Opened, Clicked, Bounced, and Unsubscribed counts with percentages.
4. Scroll to **"Recipients"** to see per-contact delivery status (delivered, opened, clicked, bounced).

**How to manage unsubscribes:**
- Unsubscribes are managed automatically. When a recipient clicks the unsubscribe link in a campaign email, they are removed from all future campaigns from your company.
- Hard bounces are also automatically unsubscribed to protect your sender reputation.
- You can view all unsubscribed contacts at [Email Marketing](https://app.trustpager.com/growth/email-blasts) (look for the "Unsubscribes" tab or section).

### Communication Preferences and Opt-Outs

TrustPager manages email and SMS opt-outs automatically to help you comply with the Australian Spam Act and similar regulations.

**How contacts opt out:**
- **SMS STOP:** When a contact texts STOP, STOPALL, UNSUBSCRIBE, CANCEL, END, or QUIT to any of your TrustPager phone numbers, they are automatically opted out of SMS. No manual action is needed.
- **SMS re-subscription:** If a previously opted-out contact texts START, UNSTOP, or YES, they are re-subscribed automatically.
- **Email unsubscribe link:** When a contact clicks the unsubscribe link in any email (campaigns or automated emails), they are opted out of all future emails.
- **Hard bounce or spam complaint:** If an email hard-bounces or the recipient marks it as spam, the contact is automatically opted out to protect your sender reputation.

**What happens when a contact is opted out:**
- Any SMS sent to an opted-out contact is silently skipped. The message is NOT delivered. It does not appear in the SMS conversation thread.
- Any email or automation send to an opted-out contact is silently skipped at dispatch time.
- This applies to all sends: manual sends from the inbox, automation sends, AI SMS agent replies, and scheduled communications.

**How to view and manage a contact's communication preferences:**
1. Open any Contact detail page at [https://app.trustpager.com/crm/contacts/{id}](https://app.trustpager.com/crm/contacts).
2. Look for the **"Communication Preferences"** card on the page.
3. You can manually toggle **Email Opted Out** and **SMS Opted Out** on behalf of the contact if you have written proof of their consent to change the preference.
4. Never re-subscribe a contact without explicit consent from that person.

**Note:** Opted-out contacts remain in your CRM -- only outbound communications are blocked. You can still view their profile, activities, and history.

### Automations

**How to create an automation:**
1. Go to [Automations](https://app.trustpager.com/auto/automations).
2. Click the **"Create"** button (+ icon) in the **top-right of the toolbar/filter card**.
3. The Automation Wizard modal opens. Follow the steps:
   - **Step 1:** Select a trigger type (form submitted, stage changed, SMS received, etc.)
   - **Step 2:** Configure trigger conditions
   - **Step 3:** Select an action (Send Email via TrustPager Mail, Send Email via Gmail, Send Report Email, create lead, update deal, etc.)
   - **Step 4:** Configure action parameters
   - **Step 5:** Name and enable the automation
4. Click **"Save"** to create.

**How to add a second trigger (OR logic):**

An automation can fire from more than one entry point. Open the automation detail page, find the **Triggers** card, and click **"Add Trigger"** to attach a second (or third) trigger with a different event type. The automation fires when **any** trigger matches -- for example, fire the same action chain when a website form is submitted OR when a client completes an internal form.

**How to schedule a Voice Call / SMS / Email automation action:**

When configuring a Send Email, Send SMS, or Voice Outbound Call action, the wizard's content step now includes a **"When should this … send?"** picker:
- **Send immediately** — runs the action as soon as it fires (default).
- **Business hours only** — sends now if currently in business hours, otherwise queues until the next business-hours window. Timezone is resolved from the contact's timezone field, the phone country code, or the company default — in that order.
- **After a delay** — wait N minutes after the trigger fires, then send. Optionally combine with **"Also respect business hours"** to defer past the next window if the delay lands out of hours.
- **At a specific time** — schedule for an exact date/time.

Scheduled actions appear in the [Dispatcher](https://app.trustpager.com/inbox/dispatcher) → Scheduled tab. They are auto-cancelled if the contact unsubscribes, opts out of SMS, replies before the send, or if a tied deal is moved to won/lost.

**How to add conditions to an automation:**

Conditions let you control exactly which deals trigger an automation. For example, only fire for VIP-tagged deals, or only when the deal value is above $5,000.

1. Open an automation from [Automations](https://app.trustpager.com/auto/automations) by clicking its name.
2. Find the **"Conditions"** card on the automation detail page (between the Trigger Source and the action list).
3. Click **"Add Condition"** to add a rule. Choose:
   - **Field** -- what to check (e.g. Tags, Deal Value, Lead Source, Contact Email)
   - **Operator** -- how to compare (e.g. contains, is equal to, is at least, exists)
   - **Value** -- what to compare against (e.g. a tag name, a number, a source name)
4. Add multiple conditions to require ALL of them to pass before the automation fires.
5. Click **"Save"** to apply.

When a condition is not met, the automation run status shows as **"Skipped"** in the logs -- this means it was triggered but the conditions filtered it out.

**How to enable or disable an automation:**
1. Go to [Automations](https://app.trustpager.com/auto/automations).
2. Each automation card has a **toggle switch** on the right side. Click it to enable or disable.

**How to view automation logs:**
1. Go to [Automation Logs](https://app.trustpager.com/auto/logs) or [Data > Automation Logs](https://app.trustpager.com/data/automation-logs).
2. Each row shows an execution with timestamp, status (Completed, Failed, Skipped), and the automation name.
3. **Skipped** status means either: (a) conditions were not met so no actions ran, or (b) every action in the automation was individually suppressed via the per-action picker.
4. Click the **eye icon** on the right side of any row to see step-by-step execution details. The run record shows which action IDs were skipped.

**How to duplicate an automation:**
1. Go to [Automations](https://app.trustpager.com/auto/automations).
2. Click the **three-dot menu (...)** on the automation card.
3. Select **"Duplicate"** from the dropdown.

**Available automation triggers:**

| Trigger | Description |
|---|---|
| Form Submitted | When a form is submitted on a website |
| SMS Received | When an inbound SMS message is received |
| Email Received | When an inbound email is received |
| Call Analyzed | When a voice call has been analyzed |
| Checkout Completed | When a Stripe checkout is completed |
| Automation Completed | When another automation finishes |
| Booking Created | When a customer books an appointment |
| Booking Cancelled | When a booking is cancelled |
| Booking Rescheduled | When a booking is moved to a new time |
| Document Sent | When a document is generated and sent |
| Signature Sent | When a document is sent for signing |
| Signature Completed | When all recipients have signed |
| Signature Declined | When a recipient declines to sign |
| Form Sent | When a form is sent to a recipient |
| Form Completed | When a recipient completes a form |
| n8n Workflow | When an n8n workflow sends a webhook |
| Zapier Zap | When a Zapier Zap sends a webhook |
| Generic Webhook | Custom webhook integration |
| Xero Contact Created/Updated | When contacts change in Xero |
| Xero Invoice Created/Updated/Paid | When invoices change in Xero |
| Cal.com Booking Created/Rescheduled/Cancelled | When Cal.com bookings change |
| Zoom Meeting Ended | When a Zoom meeting finishes |
| Zoom Phone Call Ended | When a Zoom Phone call finishes |
| Zoom Voicemail Received | When a voicemail is left on Zoom Phone |
| Facebook Lead Ad | When a Facebook Lead Ad form is submitted |

**Available automation actions:**

| Category | Action | Description |
|---|---|---|
| **Communication** | Send Email via TrustPager Mail | Send a branded or custom HTML email via TrustPager Mail. Supports inline file attachments (max 7 MB total, max 20 files). |
| | Send Email via Gmail | Send an email via Gmail (appears in Sent folder). Supports rich text formatting including bold, italic, lists, links, and clickable images (image icon in toolbar). Supports file attachments -- select documents from the workspace file library in the wizard (max 25 MB total). |
| | Send Report Email | Send a live Reports dashboard as a formatted email digest. Renders all dashboard cards server-side per recipient. Choose TrustPager Mail or Gmail as the provider. Supports an optional HTML intro and outro around the report block. Skips sending automatically when the dashboard has no data for that recipient (suppress if empty, on by default). |
| | Send SMS | Send an SMS message to a contact |
| | Trigger Voice Call | Initiate an AI voice call to a contact |
| | Notify Assigned Staff | Send email/SMS notifications to staff assigned to the deal |
| | Send Slack Message | Post a message to a Slack channel |
| | Send Marketing Email | Send a marketing/broadcast email |
| **Documents** | Open Document | Open the document builder with a template |
| | Send Document | Generate a document and email it to the recipient |
| | Send for Signing | Generate a document and send for e-signature |
| **Forms** | Open Form | Open the form builder with a template |
| | Send Form | Send a form via email with PIN verification |
| **CRM** | Create Lead | Create or update customer, contact, and deal (find-or-create matching for inbound form/webhook leads) |
| | Create Opportunity | Spawn a new opportunity from KNOWN customer + contacts + products. No find-or-create. Built for recurring auto_schedule patterns (e.g. weekly gigs). Supports merge tags in the opportunity name; auto-fills customer/contact from audience row when used in an Auto Schedule with audience_type 'deals' or 'contacts'. |
| | Move Deal | Move the deal to a different pipeline stage. NOTE: does NOT trigger stage automations on the destination stage -- prevents cascade loops. To run actions on arrival, add them to the same automation that contains this Move Deal action. |
| | Apply Tags | Add tags to the deal (deduplicates by name) |
| | Remove Tags | Remove tags from the deal by name |
| | Update CRM Next Action | Set a follow-up reminder on a deal |
| | Add Tasks | Create a set of tasks on the deal |
| | Save Activity | Log a CRM activity linked to contacts |
| | Open Link | Open a URL in a new browser window |
| **Integrations** | Create Xero Contact | Create a contact in Xero |
| | Create Xero Invoice | Create an invoice in Xero |
| | Create Xero Repeating Invoice | Create a repeating invoice in Xero |
| | Create Xero Contact & Invoice | Create both a contact and invoice in Xero |
| | Generate Portant Document | Trigger a Portant workflow |
| | Add to ActiveCampaign Automation | Sync contact and add to automation |
| | Create Cal.com Booking | Schedule a booking on Cal.com |
| | Send Result to Facebook | Send conversion events to Facebook Pixel |
| | Call External Webhook | Send a POST request to an external URL |
| | Send to Zapier | Fire a Zapier Catch Hook with the full trigger payload (deal, contact, custom fields). Branded wizard with step-by-step Zapier setup instructions. URL must start with https://hooks.zapier.com/ |
| **Flow Control** | Trigger Automation | Fire another automation |
| | Add to Auto Queue | Enroll a contact/deal into a timed sequence |
| | Remove from Auto Queue | Cancel all pending steps for a contact/deal |

**How to set up a "Send to Zapier" automation action:**
1. In an automation, click **"Add Action"** and select **"Send to Zapier"**.
2. In Zapier, open (or create) a Zap and set the trigger to **"Webhooks by Zapier" -> "Catch Hook"**. Copy the Catch Hook URL Zapier gives you (it starts with `https://hooks.zapier.com/`).
3. Paste the Catch Hook URL into the **"Zapier Catch Hook URL"** field in TrustPager.
4. Leave **"Include trigger data"** enabled to pass deal, contact, and custom field data into Zapier so downstream steps can map each field.
5. Click **"Send Test"** to send a sample payload to your Zap. In Zapier, the Catch Hook step will show sample data you can use to configure downstream steps.
6. Click **"Save Action"** once the test succeeds.

After the automation fires, the run log records: "Sent to Zapier" with a link to the Catch Hook URL.

### Auto Queues

Auto Queues are timed multi-step automation sequences. Enroll a contact or deal, and each step fires automatically after a configured delay -- perfect for nurture sequences, onboarding flows, and follow-up reminders.

**How to create an Auto Queue:**
1. Go to [Auto Queues](https://app.trustpager.com/auto/queues).
2. Click the **"Create Queue"** button (+ icon) in the **top-right** of the page header.
3. Enter a name and optional description, then click **"Create"**.
4. You'll be taken to the queue detail page.

**How to add steps to an Auto Queue:**
1. Open a queue from [Auto Queues](https://app.trustpager.com/auto/queues).
2. Click the **"Add Step"** button (+ icon) at the top of the Steps card.
3. Enter a name for the step and set the delay (days, hours, minutes) -- this is how long after the previous step before this one fires.
4. Click **"Add Step"**. A new automation is created and linked to this step.
5. Click the step card to open its automation editor and configure what actions run (send email, send SMS, trigger voice call, etc.).

**How to reorder steps:**
1. On the queue detail page, **grab the drag handle** (grip icon on the left of each step card) and drag steps up or down.
2. The delays between steps are preserved -- each step keeps its "wait after previous" timing.

**How to edit step timing:**
1. Click the **clock icon** on a step card to open the timer modal.
2. Adjust the delay (days, hours, minutes) -- this is the wait time after the previous step.
3. Click **"Save"**.

**How to enroll contacts/deals into a queue:**
1. Create an automation at [Automations](https://app.trustpager.com/auto/automations) with any trigger (e.g. deal moves to a stage).
2. Add the **"Add to Auto Queue"** action and select which queue to enroll into.
3. Optionally set an **Enrollment Time** -- enter a template variable like `{{contact.birthday}}` or a fixed ISO date. When set, all step delays are calculated from this time instead of when the automation fires. Leave blank to start delays from the moment of enrollment.
4. When the trigger fires, the contact/deal is enrolled and all steps are scheduled automatically.

**How to manually add contacts or deals to a queue:**
1. Open a queue from [Auto Queues](https://app.trustpager.com/auto/queues).
2. In the **Active Enrollments** card, click the **"+ Add to Queue"** button in the card header.
3. In the modal, choose to enroll by **Contacts** or **Deals** (switching the tab).
4. Search for and select the contacts or deals you want to enroll (up to 500 at a time).
5. Optionally set an **Enrollment Time** to backdate step delays (leave blank to start from now).
6. Click **"Add to Queue"**. Contacts already enrolled with a pending step are automatically skipped (idempotent).

**How to remove contacts/deals from a queue:**
1. On the queue detail page, find the enrollment in the **Active Enrollments** section.
2. To remove one enrollment: click the **"Cancel"** button (X icon) on the right side of the enrollment row.
3. To remove multiple enrollments: tick the checkboxes on the left of each row, then click **"Remove from Queue"** in the bulk action bar that appears at the bottom.
4. Alternatively, use the **"Remove from Auto Queue"** action in an automation to cancel enrollments automatically when a trigger fires.

**How to configure auto-cancellation:**
Configure cancellation via an automation with a **Remove from Auto Queue** action. In the automation builder, add an action of type "Remove from Auto Queue" and select the queue. Trigger the automation on the event that should cancel enrolment (e.g. stage_changed to Won or Lost). This is the supported pattern -- the legacy "Cancel Triggers" sidebar setting on the queue detail page writes to deprecated fields and is no longer effective through the API.

**How to pause a queue:**
1. On the queue detail page, toggle the **Active** switch off in the right sidebar Settings card.
2. When paused, no new enrollments are processed. Existing pending steps continue to run.

### Auto Schedules

Auto Schedules fire an automation on a clock-based schedule (e.g. every weekday at 9am, every Monday), expanding to the current audience at fire time. Unlike Auto Queues (which run per-contact drip sequences), Auto Schedules are broadcast-style -- one fire per schedule, one automation run per audience row.

**Common use cases:** daily staff task digest, weekly stale-deal follow-up, monthly re-engagement send, periodic pipeline review.

**Who can manage Auto Schedules:** Admin and Editor roles. Viewers have read-only access.

**How to create an Auto Schedule:**
1. Go to [Auto Schedules](https://app.trustpager.com/auto/schedules).
2. Click the **"New Schedule"** button in the top-right of the page header.
3. Set the **Name** and optional **Description**.
4. Choose a **Schedule** preset (Every 15 min, Hourly, Daily, Weekdays, Specific Days, Weekly, Monthly, etc.) or enter a custom cron expression. The **Live Preview** shows the next 5 fire times so you can confirm the pattern.
5. Set the **Timezone** (defaults to Australia/Sydney).
6. Choose the **Audience** -- who receives an automation run on each fire:
   - **Users** -- every staff member (or filtered by role)
   - **Tasks by Assignee** -- one run per staff member with open tasks (digest pattern)
   - **Contacts** -- one run per matching contact (with optional filters)
   - **Deals** -- one run per matching open deal (with optional filters)
7. Select the **Automation** to fire.
8. Optionally set an **End Date** (stop after a specific date) or **Max Fires** (auto-deactivate after N fires).
9. Toggle **Active** and click **Save**.

**How to preview the audience before enabling:**
1. Open the schedule from [Auto Schedules](https://app.trustpager.com/auto/schedules).
2. Click **"Preview Audience"** in the Audience section. It shows how many rows would be resolved right now, with a sample.
3. Use this to verify filters are correct before the first scheduled fire.

**How to manually fire a schedule:**
1. Open the schedule from [Auto Schedules](https://app.trustpager.com/auto/schedules).
2. Click the **"Fire Now"** button (play icon) in the top-right. This resolves the audience immediately and sends one automation run per row.
3. Fire Now does NOT count toward max_runs or advance the next scheduled fire time -- safe to use for testing.

**How to view fire history:**
1. Open the schedule from [Auto Schedules](https://app.trustpager.com/auto/schedules) and click the **"Runs"** tab.
2. Each row shows the fire time, audience size, how many automation runs were triggered, how many failed, and the final status.

**How to pause or deactivate a schedule:**
1. Open the schedule from [Auto Schedules](https://app.trustpager.com/auto/schedules).
2. Toggle the **Active** switch off in the right sidebar. The schedule stops firing but is not deleted.

### Team & Settings

**How to invite a team member:**
1. Go to [Settings > Team](https://app.trustpager.com/settings/team).
2. Click the **"Invite Member"** button (UserPlus icon) in the **top-right** of the page header. Only visible if you have Client Admin role.
3. Fill in: Full Name (required), Email Address (required), Role (Editor or Viewer).
4. Click **"Send Invitation"** at the bottom of the form.

**How to resend an invitation:**
1. Go to [Settings > Team](https://app.trustpager.com/settings/team).
2. Find the pending team member in the list (their status badge will say "Pending").
3. Click the **refresh icon** (circular arrows) on the right side of their row.

**How to change your password:**
1. Go to [Account > Security](https://app.trustpager.com/account/security).
2. Enter your current password and new password.
3. Click **"Update Password"**.

**How to update your profile:**
1. Go to [Account > Profile](https://app.trustpager.com/account/profile).
2. Edit your display name, avatar, or email.
3. Changes save automatically.

**How to configure email settings:**
1. Go to [Settings > Email](https://app.trustpager.com/settings/email).
2. Edit the fields: From Name, Email Handle (which generates the From Email), Staff Email, Logo (upload via the drag-drop area or paste a URL), Primary Colour, Secondary Colour.
3. Changes **auto-save** after a brief pause — you'll see a success toast notification. There is no explicit Save button.

**How to set up a custom sending domain (optional -- send from your own domain):**
If you want to send emails from your own domain (e.g. `support@yourcompany.com`) instead of the default `@mail.trustpager.net`:
1. Go to [Settings > Email](https://app.trustpager.com/settings/email) and scroll to the **Sending Domains** section.
2. Click **"Add domain"** and enter your bare domain (e.g. `yourcompany.com`).
3. Two DNS records will appear -- copy and paste them at your domain registrar or DNS host. No changes to SPF or MX are required.
4. Click **"Verify"** once the DNS records are saved. DNS propagation can take a few minutes; click Verify again if not yet confirmed.
5. Once verified (green checkmark), open the email config (pencil icon) and set the Sending Address to your verified domain with your chosen handle (e.g. `support`). Your emails will now send from `support@yourcompany.com`.

**How to enable/disable CRM features:**
1. Go to [Settings > CRM](https://app.trustpager.com/settings/crm).
2. Use the **toggle switches** to enable or disable: CRM module, Contacts, Accounts.
3. Changes take effect immediately.

**How to configure Birthday Messages:**
1. Go to [Settings > CRM](https://app.trustpager.com/settings/crm) and click the **"Birthday"** tab.
2. Each row is a birthday message template for a specific year of the contact relationship (Year 1, Year 2, etc.).
3. For each template, set:
   - **Label** -- the display name (e.g. "Year 1")
   - **Channels** -- choose Email, SMS, or both
   - **Email Subject** and **Email Body** -- message sent via email
   - **SMS Body** -- message sent via SMS
4. Supported merge tags: `{first_name}`, `{last_name}`, `{company_name}`, `{age}`
5. The birthday cron runs daily at 6 AM AEST. It matches contacts whose Date of Birth (day + month) equals today's date and sends the template matching their year count.
6. To add a contact's birthday, go to their Contact detail page and fill in the **Date of Birth** field in the contact info card.
7. **For imported contacts:** if the real-world relationship is older than the CRM record, set the **Relationship Started** field on the contact (under Date of Birth on the contact detail page). The birthday year-tiering uses this date instead of when the contact was added to TrustPager -- so a client you've known for 10 years gets the Year 3+ template, not Year 1. Leave blank for new contacts; defaults to the record creation date.

### Billing & Subscription

**No-card Pro trial:**
When you create a TrustPager workspace, a free 14-day Pro trial starts automatically -- no credit card required. You get 500 starter credits and full Pro plan access for 14 days. When the trial expires, your workspace downgrades to the Free plan automatically. If you add a payment method (via the Add Payment CTA) during your trial, the remaining trial days carry over -- you are NOT charged early and you do NOT get a fresh 14 days.

**Trial progress banner:**
During your Pro trial, a banner appears at the top of [Settings > Billing](https://app.trustpager.com/settings/billing) showing how many days remain and an **"Add Payment Method"** button. Click it to lock in your trial and continue on Pro after it ends.

**Free plan features:**
On the Free plan you keep access to: Scheduling, Calendar, Bookings, Forms, Notepads, Whiteboards, Websites, Email Campaigns, Lead Gen, Contacts, Files, and training Resources. CRM (Opportunities, Companies, Contacts CRM views), Automations, Calendar AI, All Files, Images, and Workflow Training are hidden and require Pro.

**Free plan limitations:**
On the Free plan, the Permissions settings page is locked -- you will see a "Pro Plan Required" banner and cannot edit role scopes or create custom roles. The API is fully blocked (every call returns a PLAN_REQUIRED error). Upgrade to Pro to unlock full feature access.

**How to upgrade from Free / start a paid subscription:**
1. Go to [Settings > Billing](https://app.trustpager.com/settings/billing).
2. Click **"Upgrade to Pro"** or **"Add Payment Method"** (if on trial) -- you will be redirected to the Stripe checkout page.
3. Enter your payment details to start a paid Pro subscription.

**How to view your subscription:**
1. Go to [Settings > Billing](https://app.trustpager.com/settings/billing).
2. The **Subscription Card** (left) shows your current plan (Free/Pro/Enterprise), status (trialing/active), billing interval, next renewal date, seats included, and price.
3. The **Credit Balance Card** (right) shows remaining credits, usage progress bar, AUD value, conversion rate, purchase bonus, and next allocation date.

**How to manage your subscription:**
1. Go to [Settings > Billing](https://app.trustpager.com/settings/billing).
2. Click the **"Manage"** button (ExternalLink icon) on the Subscription Card.
3. This opens the **Stripe Customer Portal** where you can update payment methods, change plans, or cancel.
4. Note: if you are on a no-card trial (no Stripe subscription yet), the "Manage" button will show a prompt to add your payment method first.

**How to top up credits:**
1. Go to [Settings > Billing](https://app.trustpager.com/settings/billing).
2. Click the **"Top Up"** button (+ icon) on the Credit Balance Card.
3. Select a preset amount (**$10**, **$25**, **$50**, **$100**) or enter a custom amount ($5–$10,000).
4. The modal shows the credit calculation with any bonus multiplier applied.
5. Click **"Purchase Credits"** — you'll be redirected to Stripe checkout.

**How to view invoices and transaction history:**
1. On the [Billing](https://app.trustpager.com/settings/billing) page, scroll down to see:
   - **Invoice History** — click the **Eye icon** to view an invoice or the **Download icon** to get the PDF.
   - **Transaction History** — shows all credit allocations, top-ups, deductions, and adjustments with running balance.

### Service Requests & Feedback

**How to submit a service request or feature request:**
1. Click the **message bubble icon** (MessageCircleQuestion) in the **top-right of the navigation bar** (always visible on every page).
2. The Service Request modal opens with your current page context auto-captured.
3. Enter a **Title** (required) and **Description** (required) explaining what you need.
4. Optionally use the **"Fill with AI"** button to generate a draft title and description.
5. Click **"Send Request"**. A success confirmation appears.
6. The team will review your request and contact you within **24 hours**.

**Viewing and adding notes to a service request:**
1. Go to [Settings > Service Requests](https://app.trustpager.com/settings/service-requests).
2. Click on any request row to expand it.
3. In the expanded view, a **Notes** section shows existing notes with the author's avatar and timestamp.
4. Type in the **"Add a note..."** text field at the bottom of the notes section.
5. Press **Enter** (or click the **Send** button) to submit the note. It appears instantly alongside your avatar.

**Editing your own notes:**
- Click the **pencil icon** that appears on your own notes when you hover over them.
- The note switches to an inline edit field. Make your changes and press **Enter** or click the **checkmark** to save.
- Edited notes show an **(edited)** badge next to the timestamp.
- You can only edit notes you authored -- other users' notes do not show the pencil icon.

**Linking related requests:**
- When viewing an expanded request, a **Related Tickets** section shows any linked requests as clickable chips.
- Click a chip to jump directly to that related request.
- To add links via API: use `POST /service-requests/:id/links` with an `add` array of UUIDs.
- Links are two-way -- linking A to B also links B to A automatically.

**API / MCP:** AI agents can also submit service requests via `POST /service-requests` (API) or `create_service_request` (MCP tool). Notes can be appended via `POST /service-requests/:id/notes` or `add_service_request_note`. Notes can be edited via `PATCH /service-requests/:id/notes/:noteId` or `update_service_request_note`. Requests can be linked via `POST /service-requests/:id/links` or `link_service_requests`. Listing and filtering available via `GET /service-requests` or `list_service_requests`. Requires `service-requests:write` scope for write operations, `service-requests:read` for listing.

### Voice Agents & Browser Calls

**How to test a voice agent in your browser:**
1. Go to [Voice Agents](https://app.trustpager.com/auto/voice-agents) and click into an agent.
2. On the agent detail page, find the **Test** section.
3. Fill in any dynamic variables (customer name, phone number, etc.) if the agent requires them.
4. Click **"Start Call"** (Phone icon). Your browser will request microphone permission.
5. The AI voice agent responds in real time — a live transcript shows both your words and the agent's.
6. Use the **Mute/Unmute** toggle (Mic icon) and **Volume** control during the call.
7. Click **"End Call"** (PhoneOff icon, red) when finished.

---

## Platform Sections

The platform is divided into 8 main sections, accessible from the **top navigation bar**.

---

### 1. CRM — Customer Relationship Management

The CRM is your central hub for managing customers, deals, and sales processes.

**Go to:** [CRM Home](https://app.trustpager.com/crm)

#### Workflows (Sales Pipelines)

**Go to:** [Workflows](https://app.trustpager.com/crm/workflows)

Workflows are visual sales pipelines where you track deals through stages.

- **Create a workflow** — Click the **dropdown button** (+ with down arrow) in the **top-right** of the page. Choose from 4 templates (Inbound Sales, Outbound Sales, Onboarding, Retention) or click **"Generate with AI"** to create a custom pipeline.
- **Manage stages** — Inside a workflow, stage columns appear left to right. Click a **stage header** to rename it. Drag stage columns left/right to reorder.
- **Kanban board** — Deals appear as cards within stage columns. **Drag cards** between columns to move them. Click a card to open the deal detail panel.
- **Stage automations** — Click into a workflow's **Settings** (gear icon in the header), then navigate to a stage's automation settings to configure triggers.

#### Opportunities (Deals)

**Go to:** [All Opportunities](https://app.trustpager.com/crm/opportunities)

- **Create a deal** — Click the **"Add Deal"** tab in the **top-right** ViewToggle. Fill in the form and click **"Create Deal"**.
- **Track lead sources** — When creating/editing a deal, use the Lead Source dropdown (options are configured in [CRM Settings](https://app.trustpager.com/settings/crm)).
- **Bulk operations** — Tick checkboxes on multiple rows, then use the bulk action bar that appears at the top.
- **Row actions** — Click the **three-dot menu (...)** on any row for: View Details (eye icon), Edit (pencil icon), Delete (trash icon, red).
- **Meetings card** — Open any deal detail page to see the Meetings card. It shows all scheduler bookings linked to this deal (upcoming at top, past below) with status, time, and a link to the transcript if one was recorded. Use the **Add Booking** dropdown to manually create a booking from an event type template without leaving the deal.

#### Accounts

**Go to:** [Accounts](https://app.trustpager.com/crm/accounts)

- **Create an account** — Click the **"Add Account"** tab in the **top-right** ViewToggle. Fill in the two-column form (business info on the left, address on the right) and click **"Create Account"**.
- **Search** — Use the **search bar at the top** of the table. Filter by industry with the **dropdown** next to it.
- **Row actions** — Three-dot menu on each row: View Details, Edit, Delete.

#### Contacts

**Go to:** [Contacts](https://app.trustpager.com/crm/contacts)

- **Create a contact** — Click the **"Add Contact"** tab in the **top-right** ViewToggle. Fill in First Name, Last Name, Email, Phone, Notes and click **"Create Contact"**. Link to employers from the contact detail page after creating.
- **Search & filter** — Search bar at top, plus an **Account filter dropdown** to show contacts from a specific company.
- **Employers column** — The table shows coloured badges listing each contact's linked companies.

#### Products

**Go to:** [Products](https://app.trustpager.com/settings/products)

- **Create a product** — Click the **"Add Product"** tab in the **top-right** ViewToggle. Fill in Product Name, SKU, Price (AUD), Unit type, Category, Description and click **"Create Product"**.
- **Filter** — Use the **Category dropdown** and **Status dropdown** in the toolbar.
- **Status badges** — Green = Active, Red = Inactive.

**How to configure product-specific work order fields:**

Each product can have its own set of work order discovery questions and statuses, overriding the company-level default. This is useful when different products require different information to be collected during fulfillment.

1. Open a product from [Products](https://app.trustpager.com/settings/products).
2. Scroll to the **"Discovery Questions"** section on the product detail page.
3. Toggle **"Use custom questions for this product"** to on.
4. Add, remove, and reorder fields using the field configurator. Set a field as **"Title"** (the primary display name for the work order) and one as **"Status"** (drives the kanban column).
5. Configure **Statuses** (name and colour) that apply to work orders created for deals with this product.
6. Changes save automatically after a 1-second debounce.
7. To copy the field setup from another product, use the **"Copy from product"** dropdown.
8. To revert to the company default, toggle **"Use custom questions"** back to off.

#### Inventory (Stock Tracking)

**Go to:** [Products](https://app.trustpager.com/settings/products) -- open a product, then use the Inventory card on the detail page.

Inventory tracking is available for products that have **Track Inventory** enabled on the product record. Once enabled, stock is managed through three concepts: locations, batches, and movements.

**Enabling inventory on a product:**
1. Open a product from [Products](https://app.trustpager.com/settings/products).
2. Toggle **"Track Inventory"** on the product detail page.
3. Optionally toggle **"Track Batches"** if you receive goods in discrete lots.
4. Set a **"Low Stock Threshold"** to trigger low-stock warnings.

**Locations (warehouses / stockrooms):**
- Locations are the physical places where stock is held.
- Created and managed via the API or MCP (`create_inventory_location`, `list_inventory_locations`).
- Each location has a name, optional address, and can be set as the default.

**Batches / Lots:**
- A batch is a specific shipment or lot of a product (e.g. LOT-2024-001).
- Track batch number, received date, expiry date, supplier name, and purchase cost.
- The `product_id` is set at creation and cannot be changed.

**Movements (the ledger):**
- Every change to stock on hand is recorded as a movement. The ledger is append-only -- mistakes are corrected by posting an offsetting movement, never by deleting.
- Movement types: `receive` (stock comes in), `ship` (stock goes out), `transfer` (move between locations), `adjust_in` / `adjust_out` (manual corrections), `dispose` (write-off).
- Stock on hand updates automatically when a movement is posted.

**Stock on hand:**
- View current stock per batch per location via `list_inventory_stock`.
- See a product-level summary (total on hand, batch count, earliest expiry) via `get_inventory_stock_summary`.

#### Components (Product Instances / Samples)

**Go to:** [Products](https://app.trustpager.com/settings/products) -- open a product to see its components. Also visible on the **Samples tab** inside the Edit Deal Product modal on an opportunity.

Components are individual instances of a product -- for example, a lab sample or specimen tied to a specific product and job. Each component has:
- A **type** (`unit` for samples; `part` and `bundle` are reserved for future features).
- A **label** (human-readable name).
- A **status** (e.g. pending, in_progress, completed, failed -- free-text, no enforced list).
- An **attributes** field for arbitrary result data (test results, measurements, flags).
- An optional link to an **opportunity / job** via `opportunity_id`.
- An optional **external_ref** for linking to an external system.

The `product_id` is set at creation and cannot be changed. Up to 500 components can be created in a single API call via `bulk_create_components`.

#### Tasks

**Go to:** [Tasks](https://app.trustpager.com/tasks/tasklist)

- **Create a task** — Click **"New Task"** (+ icon) in the **top toolbar**. A modal opens with all task fields.
- **Left sidebar** — Shows folder categories with task counts, plus status filters (Active, Todo, In Progress, Completed).
- **Inline editing** — Click any field directly in the table to edit it: title, status badge, priority dot, due date, assignee avatar, linked deal.
- **Drag to reorder** — Grab the **grip handle** (six dots icon) on the left side of a row and drag.
- **Priority dots** — Colour-coded: Low (grey), Medium (yellow), High (orange), Critical (red).

#### Reporting

**Go to:** [Reporting](https://app.trustpager.com/operations/reporting)

Create and view report dashboards with customisable charts and stat cards.

**Creating a Dashboard:**
1. Go to [Reporting](https://app.trustpager.com/operations/reporting).
2. Choose a template (Sales Overview, Staff Accountability, Pipeline Health, or Marketing ROI).
3. Optionally select a pipeline to filter all charts.
4. Click **"Create Dashboard"** -- all cards are auto-populated from the template.

**Adding a Report Card:**
1. Click **"+ Add Card"** in the top-right of the toolbar.
2. Step 1: Choose what to measure (deal count, revenue, win rate, etc.).
3. Step 2: Choose how to split the data (by team member, lead source, pipeline, etc.).
4. Step 3: Filter by pipeline, status, and date range.
5. Step 4: Pick a chart style (bar, line, donut, table, number) and confirm.

**Switching Dashboards:**
- Click the dashboard name dropdown in the top-left to switch between dashboards.
- Click **"New from template"** at the bottom of the dropdown to create another dashboard.

**Removing a Card:**
- Click the **X** icon in the top-right corner of any chart card.

**Controlling Who Can See a Dashboard (Visibility):**
1. In the reporting toolbar, click the **Visibility** button (located next to "Add Card" in the filter toolbar).
2. Choose a visibility setting:
   - **All Users** -- everyone in your workspace can see this dashboard.
   - **Restricted** -- only specific users or roles you grant access to can see it.
3. For **Restricted** dashboards, an **ACL picker** appears. Click **"Add person or role"** to grant access to individual users or role groups (e.g. Client Admin, Client Editor).
4. To remove someone's access, click the **X** next to their name in the access list.

Note: Admins always retain access regardless of the visibility setting.

#### Calendar

**Go to:** [Calendar](https://app.trustpager.com/tasks/calendar)

The CRM calendar shows four types of items unified in week and month views:

| Item type | What it shows |
|---|---|
| **Reminders** | Deal next-action dates (follow-ups, calls, meetings, site visits, etc.) |
| **Google Calendar** | Synced events from connected Google Calendar accounts |
| **Tasks** | Tasks with due dates |
| **Work Orders** | Work orders with a scheduled date, showing assignee and status |

**Filtering:**
- Click the **Filter** button (top-right) to toggle which item types are visible.
- Select team members to show only their items.

**Navigating:**
- **Week/Month** toggle at top-right switches views.
- Click left/right arrows to move between weeks or months.

**Clicking items:**
- **Reminder** -- opens a Next Action edit modal directly on the calendar.
- **Google Calendar event** -- opens a detail modal showing time, location, and Meet link.
- **Task** -- opens the task edit modal.
- **Work Order** -- opens the Work Order detail modal where you can update schedule date, assignee, status, and all data fields.

**Creating a work order from the calendar:**
1. Click **"+ Work Order"** button (top-right).
2. Step 1: Select the deal/opportunity from the picker.
3. Step 2: Select the specific product line item (deal product).
4. Step 3: Set the scheduled date, assignee, and fill in required work order fields.
5. Click **Create Work Order**.

**Adding a Reminder/Next Action to a Deal:**
1. Open a deal from [Opportunities](https://app.trustpager.com/crm/opportunities).
2. In the Events section of the deal card, click **"Add Event"**.
3. Select an event type from the dropdown (e.g. "Site Visit", "Demo", "Follow-Up Call"). Event types are configured by your admin in [Settings > CRM](https://app.trustpager.com/settings/crm).
4. Fill in the date, time, and any additional details (attendees, meeting link, etc.).
5. If the selected event type has an event queue attached, the deal is automatically enrolled in the reminder sequence starting from the configured offset before the event.

---

### 2. Inbox - Communications Hub

**Sections appear based on active integrations.** If you don't see a tab, its integration hasn't been set up.

| Tab | Link | Requires |
|---|---|---|
| Calls | [Open](https://app.trustpager.com/inbox/phone-calls) | Active phone number in [Settings > Phone](https://app.trustpager.com/settings/phone) |
| SMSs | [Open](https://app.trustpager.com/inbox/sms) | SMS phone numbers in [Settings > Phone](https://app.trustpager.com/settings/phone) |
| WhatsApp | [Open](https://app.trustpager.com/inbox/whatsapp) | WhatsApp phone paired in [Account > Connect](https://app.trustpager.com/account/connect) |
| Emails | [Open](https://app.trustpager.com/inbox/email) | Email configured in [Settings > Email](https://app.trustpager.com/settings/email) |
| Meetings | [Open](https://app.trustpager.com/inbox/meetings) | TrustPager Notetaker or Zoom integration |
| Voice Agents | [Open](https://app.trustpager.com/inbox/calls) | Voice agents in [Auto > Voice Agents](https://app.trustpager.com/auto/voice-agents) |

#### Making an Outbound Call (Browser Softphone)

TrustPager includes a built-in browser softphone -- you can call any contact directly from your browser without a separate app.

**How to make a call:**

1. Open any contact record, opportunity, or go to [Calls](https://app.trustpager.com/inbox/phone-calls).
2. Click the **"New Call"** button (phone icon in the top-right toolbar) or the phone icon inline on a contact card.
3. The **Make a Call** dialer opens. Enter or confirm the destination number in international format (e.g. +61412345678).
4. Click **"Call"**. Your browser microphone activates and the call connects through your workspace phone number.
5. When you hang up, the call is automatically recorded, rehosted to secure storage, and transcribed.
6. The transcript appears in [Calls](https://app.trustpager.com/inbox/phone-calls) within 30-60 seconds and is linked to the contact automatically.

**Requirements:**
- Your workspace must have an active phone number (Settings > Phone).
- Your account must have the calls:send permission.
- Your workspace must have sufficient credits (approximately 170 credits per minute covers the call and transcription).
- Browser microphone access must be allowed when prompted.

**Notes:**
- The call shows your workspace phone number as the caller ID to the recipient.
- Call recordings are stored securely and deleted from the carrier immediately after the call ends.
- AI coaching can be generated from any call transcript -- open a transcript and click "Generate Coaching".

---

### 3. Auto — Automations & Integrations

**Go to:** [Auto Home](https://app.trustpager.com/auto)

#### Automations

**Go to:** [Automations](https://app.trustpager.com/auto/automations)

- **Create** — Click **"Create"** (+ icon) in the **top-right of the toolbar**. Opens the Automation Wizard.
- **Search & filter** — Search bar in toolbar, plus **Status filter** (All/Enabled/Disabled).
- **Each automation card shows:** Name, description, trigger type badge, stats (total runs, success rate, last run), and a **toggle switch** to enable/disable.
- **Three-dot menu** on each card: Edit, View Logs, Duplicate, Delete.

#### Auto Queues

**Go to:** [Auto Queues](https://app.trustpager.com/auto/queues)

- Timed multi-step automation sequences for nurture flows, onboarding, and follow-up reminders.
- **Create** -- Click **"Create Queue"** (+ icon) in the **top-right** of the page header. Enter a name and optional description.
- **Each queue card shows:** Name, description, step count, total duration, active enrollments, completed enrollments, and created date.
- **Queue detail page** -- Two-column layout with steps (left) and settings (right). Steps show a timeline with "Wait X" delays between them. Drag to reorder steps.
- **Active enrollments** show entity name (deal/contact/account), progress, next step name, and a live countdown timer.

#### Agent Hub

**Go to:** [Agent Hub](https://app.trustpager.com/auto/agent-hub)

The Agent Hub shows all AI agent activity in one place. It has 4 tabs:

- **Agents** -- Registry of all registered AI agents (name, type, status, last run). Click any agent row to open its detail page.
- **Runs** -- Full run log with per-agent status, duration, and output summaries.
- **Signals** -- Inter-agent signals and handoffs.
- **Proposals** -- Action proposals submitted by agents that need human approval.

#### Scheduled Agent Detail Page

**Go to:** https://app.trustpager.com/auto/agent-hub/scheduled/:id (click an agent row in the Agents tab)

The detail page uses a two-column layout. The left column (3/4 width) shows run history, signals, and a template notepad. The right column (1/4 width) is a sidebar card with a 12-section accordion:

- **Information** -- Name, display name, description, agent type, and status.
- **Schedule** -- Cron expression and timezone. Click the edit icon to open the schedule modal with a next-5-runs preview.
- **Authorization** -- OAuth scopes and token status for the agent's CRM access.
- **Model** -- AI model and version in use.
- **Persona** -- Preview of the agent's system prompt. Click "View full persona" to see the complete text.
- **Kickoff prompt** -- The message template sent to kick off each run. Click the edit icon to update it.
- **MCP Servers** -- Configured MCP server endpoints.
- **Tools** -- Tool definitions and permission policies.
- **Skills** -- Agent skill configuration.
- **Vaults** -- Attached credential vaults (injected as env vars at session start).
- **Capabilities & wiring** -- Capabilities list and upstream/downstream agent connections.
- **Configuration** -- Raw JSONB configuration block.
- **Developer details** -- Internal IDs, template ID, pinned version, and trigger config.

**Header actions (managed agents only):**
- **Test Run** -- Fires a manual run immediately. Returns a session ID and run ID.
- **Open Settings** -- Opens the full-screen settings editor (see below).

#### Scheduled Agent Settings Editor

**Go to:** https://app.trustpager.com/auto/agent-hub/scheduled/:id/settings (click "Open Settings" in the agent detail header)

Full-screen editor for managed agents. The toolbar has three actions:
- **Refresh** -- Reloads the latest definition from the AI platform.
- **Save Draft** -- Saves local fields (kickoff message template, schedule, timezone) to the registry without bumping the version.
- **Publish** -- Publishes all changes and increments the agent version on the AI platform.

Five mode tabs:
1. **Kickoff** -- Edit the message template that initiates each agent session.
2. **Schedule** -- Set the cron expression, timezone, and view the next 5 scheduled runs.
3. **Persona** -- Edit the agent's system prompt (the full behavioral contract for every session).
4. **Tools** -- Configure which tools and MCP toolsets the agent has access to.
5. **Model** -- Select the AI model and speed tier.

#### Agent Proposals (Proposals Tab)

**Go to:** [Agent Hub > Proposals](https://app.trustpager.com/auto/agent-hub?tab=proposals)

When your AI agents identify an action that should be taken but should not be executed without human sign-off, they submit a proposal here.

**Reviewing a proposal:**
1. Go to [Agent Hub > Proposals](https://app.trustpager.com/auto/agent-hub?tab=proposals).
2. Pending proposals are expanded by default and show the agent's reasoning, context data, and the exact action it wants to take.
3. Click **"Approve"** to execute the action immediately (the result is shown inline).
4. Click **"Reject"** to decline -- you can enter an optional reason, which is fed back to the agent.

**Filter bar** -- Switch between Pending, Approved, Rejected, and All to view history.

**Priority badges** -- Proposals are tagged Low / Medium / High / Critical so you can triage at a glance.

**Proposals expire** -- By default after 7 days. Expired proposals cannot be approved.

#### Integrations

**Go to:** [Integrations](https://app.trustpager.com/auto/integrations)

- Browse available integrations in a grid layout. Click an integration card to begin setup (OAuth or API key).

#### Logs

**Go to:** [Automation Logs](https://app.trustpager.com/auto/logs)

- Table of all automation runs. Click the **eye icon** on any row for step-by-step details.

#### Error Alerts

**Go to:** [Settings > Automation](https://app.trustpager.com/settings/auto) -- **"Error Alerts"** tab.

Configure who gets notified when an automation action fails. Alerts are throttled to one notification per unique error type per hour so you are not flooded during incidents.

- **Email recipients** -- Add one or more email addresses. When any automation action in your workspace fails, each address receives an email with the action type, automation name, error detail, and a direct link to the failed run.
- **SMS recipients** -- Add phone numbers in E.164 format (e.g. 0400 000 000). Requires an active phone number in your workspace. SMS alerts contain a short summary of the failure.
- **To configure:** Go to [Settings > Automation](https://app.trustpager.com/settings/auto), open the **"Error Alerts"** tab, and enter your email and/or phone recipients.

---

### 4. Growth, Content & Ops — Publishing & Communications

The old Tools menu has been split across three top-level sections in the navbar: **Growth** (websites, lead generation, reputation, referrals, email blasts), **Content** (files, documents, images, voices, music), and **Ops** (scheduling, forms, notepads, spreadsheets, whiteboards, reporting).

#### Websites — [Open](https://app.trustpager.com/growth/websites)
- Manage landing pages. Click a website to open it, then click **"Edit"** to enter the drag-and-drop Page Builder.

#### Email Marketing — [Open](https://app.trustpager.com/growth/email-blasts)
- Broadcast email campaigns sent to a filtered audience via TrustPager Mail.
- **Campaign list**: Shows all campaigns with status (draft, sending, sent, failed), recipient count, and open/click stats.
- **Create Campaign**: Click **"New Campaign"** (top-right). Fills in name, subject, body, audience filter, and optional CTA button.
- **Audience filter**: Target by contact tags and/or pipeline stage. Click **"Preview Audience"** before sending to confirm recipient count.
- **Campaign detail**: Shows per-campaign stats (sent, delivered, opened, clicked, bounced, unsubscribed) and per-recipient delivery status.
- **Unsubscribes**: Managed automatically. Recipients who opt out are excluded from all future campaigns.

#### PDFs — [Open](https://app.trustpager.com/content/documents)
- **Three tabs** in the page header: Templates, Saved, Sent.
- **Left sidebar** shows Opportunity filter, document type filters (All, Agreement, Form, Invoice, Letter, Other) with folder organisation below.
- **Top toolbar** has: Search bar, Sort dropdown (Date/Name/Size), View toggle (Grid/List).
- **Upload** via drag-and-drop zone on the Saved tab or click to browse.
- **Sent tab** ([Signatures](https://app.trustpager.com/content/documents/signatures)) — shows all documents sent for e-signature, grouped by template. Track signing status, manage envelopes, download signed PDFs.

#### Files — [Open](https://app.trustpager.com/content/files)
- Central hub for uploading and managing all file types. Accepts PDFs, images, videos (MP4, WebM, MOV up to 50 MB), documents, spreadsheets, presentations, text files, and archives. PDFs are automatically routed to the PDFs system; images are routed to the Images system; videos are routed to the Videos system; everything else is stored as a secure file with signed URLs.
- **Upload** via drag-and-drop zone or click to browse. Progress bar tracks upload status. Videos upload directly to cloud storage.
- **Category tabs**: All | Documents | Spreadsheets | Presentations | Text | Archives | Images | Videos — filter by file type.
- **Left sidebar** shows folders. Create, rename, and delete folders from the sidebar.
- **Top toolbar** has: Search bar, Sort dropdown (Date/Name/Size), View toggle (Grid/List).
- **Preview**: Office files (docx, xlsx, pptx) open in Google Docs Viewer. Text/CSV files preview inline. Archives show download-only. PDFs open in the PDF viewer. Images open in the image viewer.
- **Three-dot menu** on each file card (grid and list view): View File, Move File, Delete.
- Files can also be attached to CRM entities (Contacts, Accounts, Opportunities) from their detail pages via the **Files** section in the sidebar.

#### Forms — [Open](https://app.trustpager.com/operations/forms)
- **Three tabs** in the page header: Templates, Prefilled, Sent.
- **Left sidebar** shows folders with form counts.
- Create from template grid, blank form, or **"Generate with AI"** (wand icon).
- **Three-dot menu** on each form card: Edit, Duplicate, View Submissions, Move to Folder, Archive, Delete.
- **Form completion notifications** — Open a form template → click **Edit** → right sidebar has a **Notifications** section. Add email addresses here to receive a notification whenever that specific form is completed. Workspace-wide defaults can be set at [Settings > CRM](https://app.trustpager.com/settings/crm) → **"Form Notifications"** card. Notification cascade: per-send addresses override template addresses override workspace defaults; all matching addresses are merged.
- **PDF archive on submit** — Open a form template → click **Edit** → right sidebar has a **"PDF Archive"** section. Toggle on "Archive submissions as PDF" to automatically generate a PDF of each completed submission and attach it to the linked opportunity. Set Folder and Document Type for the archived files. Requires a linked opportunity -- submissions without an opportunity are skipped. Costs 1 credit per page.
- **Convert submission to PDF** — On any completed submission detail page, click **"Convert to PDF"** to generate a one-off PDF archive attached to the linked opportunity. Requires the submission to have status "completed" and a linked opportunity.

#### Whiteboards — [Open](https://app.trustpager.com/operations/whiteboards)
- Visual canvas tool. Click to create or open whiteboards.

#### Images — [Open](https://app.trustpager.com/content/images)
- **Two tabs** via ViewToggle (top-right): **Projects** (AI image creation) and **Manage** (image storage).
- **Projects tab** — Card grid of AI image projects. Click **"Create New Project"** (+ icon) to start a new AI image project, which opens the Image Builder.
- **Manage tab** — Upload via drag-and-drop zone or click to browse. Optional **"Optimise for Web"** toggle compresses images for faster loading.
- **Left sidebar** shows Opportunity filter, folders, and AI Generated section. Create, rename, and delete folders from the sidebar.
- **Three-dot menu** on each image card: View, Move, Delete.
- Images are stored in TrustPager's file storage with public URLs for fast delivery.

#### Image Builder — [Open](https://app.trustpager.com/content/images?tab=projects)
- Full-screen AI image generation workspace. Left sidebar has prompt controls; right side shows the canvas.
- **Prompt tab** (right sidebar) — Enter a description, select Image Type, Style, Influence, Environment, Background, Mood, Colours, Aspect Ratio, and dimensions. Click **"Generate"** to create.
- **Edit tab** (right sidebar) — Post-processing tools: **Inpaint** (draw mask + prompt), **Upscale** (2x or 4x), **Remove Background** (one-click).
- **Version history carousel** at the bottom of the canvas shows all generated versions. Click any version to revert.
- **Download** button in the header to save the final image.

#### Notepads — [Open](https://app.trustpager.com/operations/notepads)
- Rich text note-taking tool with auto-save. Card grid layout with folder organisation.
- **Create** — Click **"New Notepad"** (+ icon) in the **top-right** of the page header. Opens the full-screen editor.
- **Editor** features: Bold, italic, underline, strikethrough, headings (H1-H3), lists, tables, text colour, highlighting, alignment, drag-drop images.
- **AI panels** (top-right of editor toolbar): **Wand icon** opens AI Text panel (generate and insert text), **Image icon** opens AI Image panel (generate images inside notepad).
- **Left sidebar** shows folders with notepad counts. Favourites toggle to filter starred notepads.
- **Three-dot menu** on each card: Open, Favourite, Move File, Delete.
- **API/agent iterative editing:** AI agents can append, prepend, or patch individual sections by heading name without re-sending the full document. The `update_notepad` tool supports `mode: "append"`, `mode: "prepend"`, and a `patches` array for section-level edits. This is how Server EVE overnight reports grow notepads incrementally each day.

#### Scheduling — [Open](https://app.trustpager.com/operations/scheduling)
- **Bookings** (left column): View upcoming, past, and cancelled bookings. Click the briefcase icon on a booking to open the linked CRM deal. Mark no-show or cancel from this card.
- **Event Types** (right column): Create and manage event types that customers can book (e.g., 15 Min Booking, 30 Min Consultation). Set duration, buffer times, minimum notice, and slot intervals.
- **Business Hours** (left column, below Bookings): Toggle days on/off, set start/end times per day, choose timezone. Changes auto-save.
- **Date Overrides**: Click **"+ Add Override"** to block specific dates (holidays) or set custom hours.
- **Team Availability**: Expand team members to set individual availability that overrides company defaults.
- **Google Calendar Sync**: Each team member connects their own Google Calendar at [Account > Connect](https://app.trustpager.com/account/connect). This enables bidirectional sync -- bookings create calendar events with Google Meet links, and busy calendar times automatically block booking slots.
- **Pre-Meeting Reminders**: Click a bookable event type to open its detail page. In the right column, use the **Pre-Meeting Reminders** card to add email and/or SMS reminders sent automatically before bookings (e.g., 24h before, 1h before). Choose who gets reminded (booker, attendees, team, or everyone) and customize the message with variables like `{booker_name}`, `{event_type}`, `{time}`, `{meet_link}`, `{management_url}`.
- **Self-Service Booking Management**: Every booking confirmation includes a secure management link (also embedded in the Google Calendar event description) that lets the booker cancel, reschedule, or update their contact details without logging in. The link is delivered via calendar invite and reminder emails using the `{management_url}` template variable. The link expires 24 hours after the booking end time. No login is required -- the link itself is the credential.
- **Multiple Attendees**: Bookings created via API/MCP can include additional attendees who receive Google Calendar invites with the Google Meet link.
- **Embeddable Booking Pages**: Every bookable event type can be embedded directly in your website using a standard `<iframe>`. Go to [Ops > Scheduling](https://app.trustpager.com/operations/scheduling), open the event type, and click the **Customize embed** button (Paintbrush icon). The customiser lets you match the booking widget to your website colours (card background, text, buttons, borders) and layout (width, alignment, flat vs shadowed card). The embed snippet is shown at the bottom of the panel -- copy it and paste it into any page on your website. Your theme is saved server-side, so the snippet never changes when you update the design.
- **Embeddable Form Pages**: Public forms can also be embedded in the same way. Open the form in the form builder, use the **Embed** tab in the sidebar, and copy the `<iframe>` snippet. Theme is configured the same way as booking embeds.
- **TrustPager Notetaker**: An AI meeting bot that joins your Google Meet bookings, transcribes the meeting with speaker attribution, and writes the transcript to the linked CRM deal. Enable it at [Settings > CRM > Scheduling](https://app.trustpager.com/settings/crm). Once enabled, all new bookings with Google Meet links will have the notetaker auto-scheduled. You can also add it manually to an existing booking using the **Add Notetaker** button on the Scheduling page. Pricing: 23 credits per recorded minute (e.g. a 30-minute meeting costs 690 credits). The transcript appears in the deal view under Transcripts after the meeting ends.

#### Connect (Personal Integrations) -- [Open](https://app.trustpager.com/account/connect)
- Found under your profile menu (top-right avatar > **Connect**) or [Account > Connect](https://app.trustpager.com/account/connect).
- **Connection health alert:** If any of your personal integrations (Gmail, Google Calendar, Google Drive) expire or are revoked, a red pulsing button appears in the top navigation bar. Click it to go straight to [Account > Connect](https://app.trustpager.com/account/connect) and reconnect. The button disappears once all connections are healthy.
- **Reconnect email:** When a personal integration disconnects, TrustPager automatically emails you a reconnect link. Workspace admins are also notified so they can follow up if needed. The email is re-sent every 7 days while the connection remains broken. Once you reconnect, the emails stop.
- **Google Calendar**: Click **Connect Google Calendar** to authorize. Once connected, new bookings automatically create Google Calendar events with Google Meet, your busy times block booking slots, and cancelled bookings remove the calendar event. Each team member should connect individually.
- **Gmail**: Click **Connect Gmail** to authorize. Once connected, automations can send emails via your Gmail account using the "Send Email via Gmail" action. Emails appear in your Gmail Sent folder. You can configure which Gmail send-as alias to use per company.

#### Email Settings — [Open](https://app.trustpager.com/settings/email)
- Fields: From Name, Email Handle, Staff Email, Logo (upload area or URL), Primary Colour (colour picker), Secondary Colour.
- **Auto-saves** after a short pause — no Save button needed. Toast notification confirms.

#### SMS & Voice Setup — [Open](https://app.trustpager.com/settings/sms)
- Two-column layout: left column shows SMS settings; right column shows your voice phone numbers.
- **Voice Agent Routing accordion** on each phone number: assign an inbound agent (answers incoming calls) and an outbound agent (caller ID for outbound calls) independently. Click "Save Routing" to apply -- the change takes effect on your voice agents immediately.
- **Monthly fee:** Each active phone number costs 10,000 credits/month. The first mobile number per workspace is free (shown as "Free").
- **Billing disclosure** is shown below each number showing its next charge date.

#### Phone Number Settings — [Open](https://app.trustpager.com/settings/phone)
- View and manage your SMS and voice phone numbers. Click any number row to open the detail page for that number.
- **Phone number detail page** (`/settings/phone/:id`): shows the number's friendly name, capability badges (SMS/Voice/MMS), and the **Call Settings** card.
- **Call Settings card:** Choose how to handle incoming calls using the three-way mode toggle:
  - **AI Voice Agent** -- select the agent that answers incoming calls. Auto-saves when you pick an agent.
  - **Forward** -- enter a destination in E.164 format (e.g. +61400000001). Auto-saves when you click Save.
  - **Just log it** -- calls are logged to activity only; nothing answers and nothing forwards.
- **Outbound calls (read-only):** the "Outbound calls" section shows which AI agents are configured to dial out from this number. This is configured per voice agent, not here.

**How to set up call forwarding:**
1. Go to [Settings > Phone](https://app.trustpager.com/settings/phone).
2. Click the row of the number you want to configure.
3. In the **Call Settings** card, click **Forward** in the mode toggle.
4. Enter the forwarding number in E.164 format (e.g. +61400000001).
5. Click **Save**. The change applies immediately.

#### Regulatory Compliance (Phone Number Setup for SMS) -- [Open](https://app.trustpager.com/settings/sms-setup)
Some countries (including Australia) require identity verification before activating SMS or voice capabilities on a phone number. TrustPager guides you through creating and submitting a regulatory bundle.

**Rejected bundle -- what it means and how to fix it:**
If your bundle is rejected, a red banner appears at the top of the SMS Setup page explaining the rejection. The rejection reason is sourced from the provider review and surfaced directly in the UI.

**Steps to resubmit after a rejection:**
1. Go to [Settings > SMS Setup](https://app.trustpager.com/settings/sms-setup).
2. Read the rejection banner -- it shows the specific reason(s) your bundle failed review. **Check your email** as the provider sends a detailed rejection notice to the email address on your bundle.
3. Click **Update & Resubmit**. The form prefills with your existing bundle data.
4. Correct the details that caused the rejection (business name, address, identity document, etc.).
5. Click **Submit** to send the updated bundle for review. The status returns to "pending review".

**Common rejection reasons:**
- Business name does not match government records -- ensure the name matches your ABN registration exactly.
- Address cannot be verified -- use the address registered with your business authority.
- Identity document issues -- re-upload a clear, valid government ID.

#### Voice Agents — [Open](https://app.trustpager.com/auto/voice-agents)
- Manage AI phone agents. Click an agent to configure behaviour and knowledge base.
- **Edit Settings** button (top toolbar, Settings icon) opens the [Voice Agent Settings](https://app.trustpager.com/auto/voice-agents/{id}/settings) page for editing the agent's conversation flow, voice, language, dynamic variables, and behaviour settings directly in TrustPager.
- The **Settings** page includes tabs for Conversation Flow, Settings (voice speed, responsiveness, interruption sensitivity, backchannel, call limits, voice ID, language), and Channels (phone numbers and website configs linked to the agent).
- Changes are saved to your workspace first, then applied to your live voice agents.

**Built-in scheduling capabilities (available to clients with the Voice Agent package):**

When your voice agent (e.g. Evie, your AI receptionist) is connected to your TrustPager scheduling system, callers can:
- **Check available slots** -- ask the agent "when can I book?" and hear real-time availability.
- **Book an appointment** -- confirm a time and get an instant booking confirmation with all details.
- **Cancel a booking** -- say "I need to cancel my appointment" and the agent cancels it immediately.
- **Reschedule a booking** -- say "I need to move my appointment" and the agent books the new time then cancels the old one.
- **Unsubscribe from all communications** -- say "please remove me from your list" and the agent immediately unsubscribes the caller from all future emails, SMS, and calls. All matching CRM records under that phone number are updated (Spam Act compliant).

These capabilities are wired by your FinalPiece onboarding team as custom tools on your voice agent. No action is required on your end to enable them -- they are included in the voice agent setup.

**Business-hours call forwarding:**

If you want inbound calls automatically forwarded to a different number outside business hours (or during specific windows), you can set this up from the voice agent's detail page.

1. Go to [Voice Agents](https://app.trustpager.com/auto/voice-agents) and click your agent.
2. Scroll to the **"Call Forwarding"** card and switch it on.
3. Enter the **Forwarding Number** (e.g. your mobile or an answering service) in international format (e.g. +61400000001).
4. Choose **"Forward When"**: outside business hours (most common) or during business hours.
5. Set your timezone and tick each weekday with open/close times.
6. Click **Save**. Changes take effect on the next inbound call.

When active, calls that arrive during the forwarding window are silently transferred to the destination number by your AI voice agent. Calls outside the forwarding window are answered by the AI as usual.

#### Referrals — [Open](https://app.trustpager.com/growth/referrals)
Track word-of-mouth referrals and see who is driving the most business.

**Referrers tab (default)** — [Open](https://app.trustpager.com/growth/referrals) — leaderboard showing each contact who has referred business, their total referral count, and conversion rate. Click any row to open the referrer drilldown.

**Referrer drilldown** — [Open](https://app.trustpager.com/growth/referrals/referrers/:contactId) — full history of every referral that contact has generated, with status, category, and conversion detail.

**Referrals tab** — full list of individual referral records with filters for status and category. Each row links to the referred contact and, once converted, to the resulting opportunity.

**How to log a referral manually:**
1. Go to [Referrals](https://app.trustpager.com/growth/referrals).
2. Click **"+ New Referral"** (top-right).
3. Enter the referrer (the person who sent the lead) and the referred contact details.
4. Optionally set a **Category** (e.g. "Client", "Partner") if your workspace has categories configured.
5. Click **Create Referral** to record the referral.

**How to request a referral:**
1. Open a contact or opportunity in the CRM.
2. Use the **Request Referral** action (available via automation or the MCP agent tool `request_referral`).
3. The contact receives an email with a secure referral form link. When someone submits the form, a new referral record is created automatically and linked back to the referring contact.

**How to convert a referral:**
Once a referral has been qualified, open the referral record and click **Convert** to create a linked opportunity in the CRM. The referral status updates to "converted" and the referrer appears on the leaderboard with an updated conversion count.

---

### 5. Data — Logs & Analytics

**Go to:** [Data Home](https://app.trustpager.com/data)

Every log page has: a **search bar**, **filter dropdowns**, and a **table** where each row has an **eye icon** on the right to view full details.

| Log | Link | What It Tracks |
|---|---|---|
| CRM Logs | [Open](https://app.trustpager.com/data/crm-logs) | Field-level change history for contacts, accounts, and opportunities (admin only -- requires crm_audit:read scope) |
| Workflow Logs | [Open](https://app.trustpager.com/data/cms-logs) | Workflow trigger activity and platform automation events |
| Automation Logs | [Open](https://app.trustpager.com/data/automation-logs) | Automation executions and results |
| Integration Logs | [Open](https://app.trustpager.com/data/integration-logs) | Third-party API calls and syncs |
| Webhook Logs | [Open](https://app.trustpager.com/data/webhooks) | Incoming/outgoing webhook activity |
| Website Logs | [Open](https://app.trustpager.com/data/website-logs) | Form submissions from websites |
| Email Logs | [Open](https://app.trustpager.com/data/emails) | Email delivery, opens, clicks, bounces |
| Order Forms | [Open](https://app.trustpager.com/data/order-forms) | Order form submissions |
| Payments | [Open](https://app.trustpager.com/data/payments) | Stripe payment transactions |
| Agreements | [Open](https://app.trustpager.com/data/agreements) | E-signature envelope activity and signing history |
| Auto Queue Tasks | [Open](https://app.trustpager.com/data/event-queue-tasks) | Scheduled auto queue step executions -- monitor, retry failed, cancel pending |

---

### 6. Settings

**Go to:** [Settings Home](https://app.trustpager.com/settings)

| Page | Link | What You Can Do |
|---|---|---|
| CRM Settings | [Open](https://app.trustpager.com/settings/crm) | Toggle CRM, Contacts, Accounts on/off; configure lead sources; manage Scheduled Event Types; import data; configure Birthday Messages (Birthday tab) |
| Automation Settings | [Open](https://app.trustpager.com/settings/auto) | Error Alerts (email/SMS recipients for automation failures), Approvals (pending API action review), AI Agents, Semantic Search |
| Evie AI | [Open](https://app.trustpager.com/settings/evie-ai) | Configure the Evie in-app assistant -- conversation history, persona, and workflow instructions |
| Company | [Open](https://app.trustpager.com/settings/company) | Company name, logo, address, timezone, currency (Admin only) |
| Team | [Open](https://app.trustpager.com/settings/team) | Invite members (top-right button), assign roles, resend invites |
| Billing | [Open](https://app.trustpager.com/settings/billing) | View subscription plan, credit balance, top up credits, manage via Stripe portal, view invoices and transaction history |

---

### 7. Account — Personal Settings

**Go to:** [Account Home](https://app.trustpager.com/account)

| Page | Link | What You Can Do |
|---|---|---|
| My Profile | [Open](https://app.trustpager.com/account/profile) | Edit name, avatar, email |
| Connect | [Open](https://app.trustpager.com/account/connect) | Connect Google Calendar (bidirectional sync, Google Meet links), Connect Gmail (send emails via automations from your Gmail) |
| Security | [Open](https://app.trustpager.com/account/security) | Change password, set up 2FA, view active sessions |
| Preferences | [Open](https://app.trustpager.com/account/preferences) | Notifications, default workflow, theme |

---

## API & MCP Integration

TrustPager provides a REST API and MCP (Model Context Protocol) server for programmatic access to your data. AI agents like Claude can interact with your CRM, automations, contacts, deals, and more.

**API access** requires an API key created by your admin. Contact your admin to get an API key with the appropriate scopes for your use case.

**What the API/MCP can do:**
- Create, read, update, and delete: contacts, accounts, deals, products, tasks, documents, forms, automations, event queues, voice agents, text agents, websites, and more
- Send emails, SMS, and initiate voice calls
- Manage pipelines and move deals between stages
- Search across contacts, accounts, and deals
- Create and manage bookings via the scheduling system
- Submit service requests and feedback
- AI-powered features: entity enrichment, deal scoring, needs analysis, call coaching, text editing, form filling

**MCP integration** allows AI assistants to interact with TrustPager directly. The MCP server is available at [mcp.trustpager.com](https://mcp.trustpager.com) and can be connected via Claude Desktop, Claude.com, or any MCP-compatible client. Each workspace has a unique MCP URL at `https://mcp.trustpager.com/<slug>/mcp` (the slug is shown on the **Settings > API Keys** page), allowing you to connect multiple workspaces simultaneously on Claude.ai.

**API Approval Queue:** If your API key has a "with Approval" permission level for certain resources, write operations (create, update, delete) are held for human review before executing. You can review, approve, or reject pending actions at [Settings > API Keys > Approvals tab](https://app.trustpager.com/settings/api-keys?tab=approvals). A count badge on the Approvals tab shows how many actions are pending. You can also configure Slack notifications (Bell icon on the Approvals tab) to receive instant alerts when actions are queued.

**Scope changes do not auto-propagate to existing connections:** When your admin updates the permitted scopes on an OAuth integration (via Settings > API Keys > Edit), the new scope set does NOT automatically apply to users who are already connected. Each user must disconnect and reconnect at [AI Access](https://app.trustpager.com/auto/ai-access) to pick up the updated permissions.

---

## Common UI Patterns

These patterns are consistent across the whole platform:

- **ViewToggle (top-right):** Many pages have a segmented control with "Manage" (list view) and "Add" (create form) tabs. Click the **"Add"** tab with the **+ icon** to switch to create mode.
- **Three-dot menu (...):** Found on the right side of every table row and card. Click for actions: View (eye), Edit (pencil), Delete (trash, red).
- **Search bar:** Always at the top of list pages. Type to filter results in real time.
- **Filter dropdowns:** Next to the search bar. Narrow by status, category, pipeline, etc.
- **Sorting:** Click any **column header** in a table to toggle sort direction (arrow indicator appears).
- **Bulk select:** Tick **checkboxes** on the left side of rows, then use the bulk action bar that appears at the top.
- **Auto-save:** Some pages (email settings, pipeline settings) save automatically after a short pause — a toast notification confirms.

---

## Key Concepts

### Australian-First Platform

- **Currency:** AUD | **Timezone:** Australia/Sydney | **Phone:** +61 format | **Date:** DD/MM/YYYY

### Roles & Permissions

| Role | Access Level |
|---|---|
| Client Admin | Full access to your company, can invite team members |
| Client Editor | Create and edit content |
| Client Viewer | Read-only access |

### Feature Visibility

Not all sections appear by default. They show up when their features or integrations are enabled:
- **CRM** — enabled in [Settings > CRM](https://app.trustpager.com/settings/crm)
- **Inbox tabs** — appear when their integration is connected (SMS, Email, Zoom, Voice Agents)
- **Log pages** — appear when there's data from the relevant integration
- **AI SMS Agent** — active when a text agent is assigned to your phone number. Toggle per-conversation in [SMS Inbox](https://app.trustpager.com/inbox/sms)
- **AI Needs Analysis** — available on Deal detail pages (FileSearch icon). Generates structured needs analysis from CRM data
- **AI Form Fill** — available on any form with AI-fillable fields (Wand icon). Generates content for form fields
- **AI Edit with AI** — right-click any text field to refine content with AI (Wand icon in context menu)
- **AI Call Coaching** — available on Phone Call detail pages (GraduationCap icon). Generates coaching reports per team member
- **AI Image Builder** — available from [Images > Projects](https://app.trustpager.com/content/images?tab=projects). Full AI image generation and editing workspace
- **Notepads** — always available at [Notepads](https://app.trustpager.com/operations/notepads). Rich text notes with AI text and image generation
- **Billing** — available at [Settings > Billing](https://app.trustpager.com/settings/billing). Subscription management, credit balance, top-ups
- **Service Requests** — always available via the message bubble icon (top-right of navigation bar)
- **Browser Voice Calls** — available on Voice Agent detail pages when voice agents are configured
- **E-Signatures** — built-in, always available. Send documents for signing from the Document Builder
