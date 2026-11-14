# The World Today — Friday 13 November 2026

Entry for make.fun's `news-image-01`: one image summing up the world's
news of Friday 13 November 2026.

A newspaper front page for the day. The lead story is the US Senate
summoning ex-Nvidia chief Jensen Huang and Commerce Secretary Howard
Lutnick over alleged AI-chip leaks to China, a day after Huang quit as
Nvidia chief; Senate Banking Chair Tim Scott warned Huang of a subpoena
if he refuses to appear. Below it: Europe joining the next round of
Ukraine peace talks and the Ukrainian drone strike on the Russian
corvette Naro-Fominsk; the Israeli strike on Nasser Hospital in Khan
Younis; and the FBI's account of North Korea's $400m crypto theft.
The strip at the foot carries Harry Kane's record 126th England cap,
the US record 483,200 deportations in 2026, and the worldwide
Microsoft 365 outage.

## Stories and sources

- **Senate summons Huang & Lutnick** — Senate Banking Chair Tim Scott
  asked Huang to testify Dec 3 and Lutnick Dec 10, warning Huang of a
  subpoena; House panels asked Huang for a closed-door interview Dec 1.
  Sources: Al Jazeera, Reuters.
- **Europe to join next peace talks** — US envoys say Putin agreed
  Europeans join the next round after US-brokered talks; a Ukrainian
  drone hit the Russian corvette Naro-Fominsk in the Gulf of Finland, a
  strike Finland's defence forces said they detected. Sources: BBC,
  Reuters.
- **Strike on Gaza hospital kills 6** — An Israeli strike hit Nasser
  Hospital in Khan Younis, killing six people including a surgeon and a
  13-year-old boy, and wounding 27. Israel said it targeted a Hamas
  commander inside the complex. Sources: Associated Press, Al Jazeera.
- **FBI: N. Korea stole $400m in crypto** — North Korean hackers used
  900+ deepfake videos and fake video-call platforms over 18 months to
  impersonate trusted contacts. Source: BBC.
- **Also today** — Kane's 126th England appearance, a caps record;
  a record 483,200 US deportations in 2026 (Al Jazeera); Microsoft 365
  mail and Teams down worldwide, 140,000 Outlook reports in 74
  countries (BBC / Downdetector).

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`news.jpg` (1024×1024, about 221 KB) to `entry.png` in the output
directory (`MAKEFUN_OUTPUT_DIR`, default `/output`), after checking
the asset's magic bytes and size against the competition gate. The
judge sees exactly the bytes that ship in this repository; every run
produces identical output.

## How the image was built

`build_frontpage.py` composes the front page with PIL: every word on
the page is rendered by that script in a large legible typeface from
the verified facts above, because image generators garble text. The
one picture on the page — the Senate hearing room with two empty
witness chairs — is a generated illustration
(`senate-illustration.webp`, a build-time asset) with no text in it;
it is cropped and pasted in by the script. Run it with
`python3 build_frontpage.py` to regenerate `news.jpg`.
