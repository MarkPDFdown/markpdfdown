<div align="center">

<h1>MarkPDFDown</h1>
<p align="center"><a href="./README.md">English</a> | <a href="./README_zh.md">中文</a> | 日本語 | <a href="./README_ru.md">Русский</a> | <a href="./README_fa.md">فارسی</a> | <a href="./README_ar.md">العربية</a></p>

[![Size]][hub_url]
[![Pulls]][hub_url]
[![Tag]][tag_url]
[![License]][license_url]
<p>マルチモーダル大規模言語モデルを活用して、PDFファイルをMarkdown形式に変換する強力なツールです。</p>

![markpdfdown](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/markpdfdown.png)

</div>

## 概要

MarkPDFDownは、PDF文書をクリーンで編集可能なMarkdownテキストに変換するプロセスを簡素化するために設計されています。高度なマルチモーダルAIモデルを活用することで、テキストを正確に抽出し、書式を保持し、表、数式、図表を含む複雑な文書構造を処理できます。

## 機能

- **PDFからMarkdownへの変換**: あらゆるPDF文書を適切にフォーマットされたMarkdownに変換
- **画像からMarkdownへの変換**: 画像を適切にフォーマットされたMarkdownに変換
- **マルチモーダル理解**: AIを活用して文書の構造と内容を理解
- **書式の保持**: 見出し、リスト、表、その他の書式要素を維持
- **カスタマイズ可能なモデル**: ニーズに合わせてモデルを設定可能

## デモ
![](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/demo_02.png)

## インストール

### uvを使用（推奨）

```bash
# uvをまだインストールしていない場合
curl -LsSf https://astral.sh/uv/install.sh | sh

# リポジトリをクローン
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# 依存関係をインストールし、仮想環境を作成
uv sync

```

### condaを使用

```bash
conda create -n markpdfdown python=3.9
conda activate markpdfdown

# リポジトリをクローン
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# 依存関係をインストール
pip install -e .
```
## 使用方法
```bash
# OpenAI APIキーを設定
export OPENAI_API_KEY="your-api-key"
# オプション：OpenAI APIベースを設定
export OPENAI_API_BASE="your-api-base"
# オプション：OpenAI APIモデルを設定
export OPENAI_DEFAULT_MODEL="your-model"

# PDFからMarkdownへ
python main.py < tests/input.pdf > output.md

# 画像からMarkdownへ
python main.py < input_image.png > output.md
```
## 高度な使用方法
```bash
python main.py page_start page_end < tests/input.pdf > output.md
```

## Dockerの使用
```bash
docker run -i -e OPENAI_API_KEY=your-api-key -e OPENAI_API_BASE=your-api-base -e OPENAI_DEFAULT_MODEL=your-model jorbenzhu/markpdfdown < input.pdf > output.md
```

## 開発セットアップ

### コード品質ツール

このプロジェクトでは、リンティングとフォーマットに`ruff`を、自動コード品質チェックに`pre-commit`を使用しています。

#### 開発依存関係のインストール

```bash
# uvを使用する場合
uv sync --group dev

# pipを使用する場合
pip install -e ".[dev]"
```

#### pre-commitフックのセットアップ

```bash
# pre-commitフックをインストール
pre-commit install

# すべてのファイルでpre-commitを実行（オプション）
pre-commit run --all-files
```

#### コードフォーマットとリンティング

```bash
# ruffでコードをフォーマット
ruff format

# リンティングチェックを実行
ruff check

# 自動修正可能な問題を修正
ruff check --fix
```

## 要件
- Python 3.9+
- [uv](https://astral.sh/uv/)（パッケージ管理に推奨）またはconda/pip
- `pyproject.toml`で指定された依存関係
- 指定されたマルチモーダルAIモデルへのアクセス

## 貢献
貢献を歓迎します！お気軽にプルリクエストを送信してください。

1. リポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 開発環境をセットアップ：
   ```bash
   uv sync --group dev
   pre-commit install
   ```
4. 変更を加えてコード品質を確保：
   ```bash
   ruff format
   ruff check --fix
   pre-commit run --all-files
   ```
5. 変更をコミット（`git commit -m 'feat: Add some amazing feature'`）
6. ブランチにプッシュ（`git push origin feature/amazing-feature`）
7. プルリクエストを開く

提出前にリンティングとフォーマットツールを実行して、プロジェクトのコーディング標準に従っていることを確認してください。

## ライセンス
このプロジェクトはApache License 2.0の下でライセンスされています。詳細はLICENSEファイルを参照してください。

## 謝辞
- このツールを支えるマルチモーダルAIモデルの開発者に感謝します
- より良いPDFからMarkdownへの変換ツールの必要性に触発されました

[hub_url]: https://hub.docker.com/r/jorbenzhu/markpdfdown/
[tag_url]: https://github.com/markpdfdown/markpdfdown/releases
[license_url]: https://github.com/markpdfdown/markpdfdown/blob/main/LICENSE

[Size]: https://img.shields.io/docker/image-size/jorbenzhu/markpdfdown/latest?color=066da5&label=size
[Pulls]: https://img.shields.io/docker/pulls/jorbenzhu/markpdfdown.svg?style=flat&label=pulls&logo=docker
[Tag]: https://img.shields.io/github/release/markpdfdown/markpdfdown.svg
[License]: https://img.shields.io/github/license/markpdfdown/markpdfdown