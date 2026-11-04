# lochan-qapp

The workspace's test app, and the starter a new Lochan app is copied from: one
app folder (`packages.json`) serving one domain package (`packages/demo`).

## Build and deploy

The app is built and served by the lochan build, from a lochan checkout whose
last build is green:

```bash
bin/deploy-app <qapp folder>
```

`bin/deploy-app` is `daksh build --app <folder>`. It pulls the packages
`packages.json` names onto the last green lochan build (a `dev` source is the
folder it names, a `repo` source that repo at its full-hash `ref`), runs the
build's checks and tests over them, signs the app image, and deploys it: the
image, its Postgres, its frontend and nginx in front of both, at
`packages.json` `ports.prod`. It is done when `/health/certificate` answers
certified through nginx.

Deploy reads the app's production secrets and origins from `.env.prod` in this
folder and refuses one that leaves a required key unset or a placeholder.
`python3 -m daksh.generators.generate-app-config --config packages.json --prod`
writes it; `daksh secrets rotate <app> --key <KEY> --generate` replaces one key. `.env.*` is gitignored and never committed.

## Layout

```
packages.json           which packages the app serves, from where, and its host ports
packages/<name>/        a package of this app, authored here
  mandi.json            the package manifest (name, entry point)
  backend/<module>/     its Python module
data/                   app-level data
```

`packages.json`:

- `primary` names the package the app serves.
- `packages.<name>.dev` is the package's folder, relative to this one. A
  package that lives in its own repo is named by `repo` and a full-hash `ref`
  instead.
- `ports` declares the app's host ports, one block per tier (`prod`, `staging`,
  `dev`). A block is given once, by `daksh.generators._ports.next_block`, and is
  data from then on.

## Adding a package

`packages/demo/` is a starting point: rename it, or author your own beside it.
Name each package in `packages.json` with its `dev` folder, and point `primary`
at the one the app serves.

## Secrets beyond `.env.prod`

LLM API keys, OAuth credentials and SMTP passwords belong in LOCKBOX,
encrypted at rest:

```bash
daksh secrets push <app> --key CLAUDE_API_KEY --value -
daksh secrets list <app>          # names only, never values
```
