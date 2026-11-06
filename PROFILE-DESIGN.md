# Profile design

## References

- [Anurag Hazra](https://github.com/anuraghazra): concise introduction and visible project evidence.
- [Jonah Lawrence / DenverCoder1](https://github.com/DenverCoder1): technology logos, project links, statistics and animated elements.
- [Skill Icons](https://github.com/tandpfun/skill-icons): recognizable original technology marks, provided by the same MIT-licensed project used in the previous README.
- [GitHub Profile Trophy](https://github.com/ryo-ma/github-profile-trophy): real upstream trophy categories and ranks. These are third-party activity cards, not official GitHub Achievements.

The design is custom. No AI-generated raster illustration is used. The hero is rendered from the mathematical vertices and edges of a four-dimensional hypercube.

## Animation

`assets/hero.gif` has 96 frames at 20 fps, loops every 4.8 seconds and weighs approximately 2 MB. It uses 16 vertices and 32 edges, rotated in the XW and YZ planes, projected from 4D to 3D and then onto the screen. It contains no scripts or external dependencies. `assets/hero.svg` is the static version.

To regenerate: install Pillow, then run `python scripts/render_hero.py`. The background is included in `assets/hero-base.png` and its editable SVG source is `assets/hero-base.svg`.

## Technology coverage

All 26 icons from the previous README are present:

- Frontend: TypeScript, JavaScript, React, Next.js, Vue, Vite, HTML, CSS, Tailwind CSS.
- Backend/data: Node.js, NestJS, Express, PostgreSQL, Prisma, MySQL, MongoDB.
- Tools: Git, GitHub, Docker, Figma, VS Code, Python.
- Mobile: Flutter, Dart, Kotlin, Android Studio.

The SVG groups are stored in this repository so rendering does not depend on the icon service. Their names are also in alt text and visible captions. Licenses are in `licenses/`. Logos remain the property of their respective owners.

## Activity updates

`scripts/update_stats.py` refreshes public GitHub statistics and caches trophy cards daily through `.github/workflows/profile-stats.yml`. Trophy categories are Commits, PullRequest, Followers and Repositories, selected from the upstream service without rewriting its scores or ranks.

The upstream primary trophy endpoint returned HTTP 402 during verification. The selected community endpoint, `https://trophy.ryglcloud.net`, is listed by the upstream project. Only the public username is sent to that endpoint; no GitHub credential is sent. Returned SVG is checked before replacing the previous file. If the service fails, the previous valid trophy image remains visible.

Public metrics exclude private repository details. Stars mean received stars, and language counts are detected languages rather than skill ratings. The private experience and education are self-reported text preserved from the previous README.

The workflow uses GitHub's automatic repository token and needs permission to commit generated images. It does not change source code or private repositories.
