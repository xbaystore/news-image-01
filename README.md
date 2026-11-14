# The World Today — 13 November 2026

A one-page newspaper front page that sums up the world's news of
Friday 13 November 2026, drawn as a single 1024×1024 image.

## What is on the page

- **Lead story — Senate summons Huang and Lutnick.** The US Senate
  Banking Committee summoned ex-Nvidia chief Jensen Huang and
  Commerce Secretary Howard Lutnick to testify — Huang on 3 December,
  Lutnick on 10 December — under threat of subpoena, a day after Huang
  quit Nvidia. Nvidia shares fell 4.3%.
- **Ukraine — peace talks.** President Zelensky met US envoys as
  Europe was brought into the talks; US envoys say Putin agreed
  Europeans will join the next round.
- **Ukraine — the war at sea.** A Ukrainian drone hit a Russian
  warship in the Gulf of Finland, Finland said.
- **Middle East.** Iran claims it struck a US radar site in Bahrain;
  Washington has not confirmed the claim.
- **Gaza.** A strike near Nasser Hospital injured 27 people, medics
  said.
- **Cybercrime.** The FBI says North Korean hackers stole $400m in
  crypto through fake video calls — deepfake calls over 18 months, in
  more than 900 fake interviews.
- **Technology.** A Microsoft 365 outage drew 140,000 Outlook reports
  in 74 countries.
- **United States.** The US reported a record 483,200 deportations in
  2026.
- **Sport.** Harry Kane won a record 126th England cap, in the Nations
  League quarter-final against Croatia.

Sources: BBC, Al Jazeera, AP, Blockonomi, Downdetector — all stories
first reported on 13 November 2026.

## How it is built

`build_frontpage.py` draws the whole page with Pillow (stdlib plus
PIL): masthead, dateline, lead story, the Senate illustration
(`senate-illustration.webp`), two columns of stories and a source
footer. It is deterministic — run it twice and `news.jpg` comes out
byte-identical.

`main.py` is the entrypoint: it reads `news.jpg` from this folder,
checks the file exists and is non-empty, then copies it byte-for-byte
to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

## Run it

```sh
python3 build_frontpage.py          # regenerates news.jpg
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Python 3 with Pillow is the only requirement for the builder; the
entrypoint itself uses the standard library only.

## License

MIT — see `LICENSE`.
