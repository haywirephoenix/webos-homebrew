# webos-homebrew

A [Homebrew Channel](https://github.com/webosbrew/webos-homebrew-channel) repository for rooted LG webOS TVs. In Homebrew Channel, open **Settings**, choose **Add repository** and enter:

```
https://haywirephoenix.github.io/webos-homebrew/apps.json
```

| App | |
|---|---|
| [Local Voice](https://github.com/haywirephoenix/webos-localvoice) | Speech recognition that runs on the TV |
| [Tailscale](https://github.com/haywirephoenix/webos-tailscale) | Install, update and run Tailscale on the TV. Not affiliated with Tailscale Inc. |

`apps.json` points at each app's latest GitHub release. After publishing a release, run `python tools/update.py` and commit `apps.json`. The pages in `descriptions` are shown on each app's page in Homebrew Channel.
