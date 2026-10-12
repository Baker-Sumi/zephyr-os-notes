# Zephyr内部構造解説

Zephyr RTOSの導入済みワークスペース、ソースツリー、設定、ビルド、起動、デバイスモデルを内部から学ぶための日本語解説書です。組込み開発経験者が、導入時に配置されたファイルからZephyrの実装を追跡できるようになることを目標にします。

- **対象版:** Zephyr v4.4.2
- **基準タグ:** [`v4.4.2`](https://github.com/zephyrproject-rtos/zephyr/tree/v4.4.2)
- **公開サイト:** [Zephyr内部構造解説](https://baker-sumi.github.io/zephyr-os-notes/)
- **読み始める場所:** [索引](docs/00-はじめに/00-索引.md)
- **執筆規約:** [AGENTS.md](AGENTS.md)

## ローカルプレビュー

公開原稿は`docs/`にあり、MkDocs MaterialでGitHub Pagesへ配信します。

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-site.txt
python -m mkdocs serve --config-file mkdocs.yml
```

`http://127.0.0.1:8000/`をブラウザで開きます。原稿を変更するとMkDocsがプレビューを更新します。

次のコマンドは、Obsidian固有構文、相対リンク、MkDocsのstrict buildをまとめて確認します。

```sh
python scripts/validate_site.py
```
