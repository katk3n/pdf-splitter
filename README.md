# pdf-splitter

pdf ファイルを目次情報を定義した csv ファイルに従って章ごとに分割します。

## Usage

```
pdf-splitter [path_to_pdf.pdf] [path_to_toc.csv] [path_to_output/]
```

- `path_to_pdf.pdf`: 分割元の pdf ファイルへのパス
- `path_to_toc.csv`: 目次情報が記載された csv ("csv format" を参照)
- `path_to_output/`: 分割されたファイルを出力するディレクトリへのパス

## csv format

```
Title,Page
__OFFSET_IN__,<number of pages before the first section>
__OFFSET_OUT__,<number of pages after the last section>
"<title of the section>",<starting page of the section>
"<title of the section>",<starting page of the section>
...
```

- `number of pages before the first section`: 最初に読み飛ばすページ数
- `number of pages after the last section`: 最後に読み飛ばすページ数
- `title of the section`: 章のタイトル
- `starting page of the section`: その章が始まる分割元の pdf におけるページ番号

参考: [examples/example-toc.csv](examples/example-toc.csv)
